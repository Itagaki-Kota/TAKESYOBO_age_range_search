import requests
import xml.etree.ElementTree as ET
import requests
import time
from bs4 import BeautifulSoup
import re
import csv

def calc_age_at_the_time(birth_date, release_date):
    # 生年月日と発売日から、発売当時の年齢を返す。
    birth_date = birth_date.replace("年", "/")
    birth_date = birth_date.replace("月", "/")
    birth_date = birth_date.replace("日", "")
    
    release_date = release_date.replace("年", "/")
    release_date = release_date.replace("月", "/")
    release_date = release_date.replace("日", "")

    birth_year, birth_month, birth_day = map(int, birth_date.split("/"))
    release_year, release_month, release_day = map(int, release_date.split("/"))

    # 何歳になる年か
    age = release_year - birth_year

    # その年の誕生日を迎えていない場合、1引く
    if release_month < birth_month:
        age -= 1
    elif release_month == birth_month:
        if release_day < birth_day:
            age -= 1
    
    return age




# URLを指定
url = "https://idol-gakuen.jp/item-sitemap2.xml"

try:
    # GETリクエストを送信
    response = requests.get(url)

    # ステータスコードが200（成功）であるか確認
    if response.status_code == 200:
        # ページ内容（XMLのソースコード）を取得
        xml_data = response.text
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
except Exception as e:
    print(f"An error occurred: {e}")


# 名前空間を設定（XML内の`xmlns`に対応）
namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}

# XMLを解析
root = ET.fromstring(xml_data)

# <loc>タグ内のURLを取得
urls = [url.text for url in root.findall('.//ns:loc', namespace)]

# 過度なリクエストを防止するためのインターバル (sec)
interval = 3

with open("output.csv", "a", newline="") as f:
    writer = csv.writer(f)

    # URLリストを表示
    for i in range(len(urls)):
        time.sleep(interval)
        url = urls[i]

        # 各URLにアクセスしてHTMLを取得
        try:
            # URLにアクセス
            response = requests.get(url)
            
            # ステータスコードが200であれば成功
            if response.status_code == 200:
                # ページのHTMLを取得
                html_content = response.text
                
                # BeautifulSoupでHTMLを解析
                soup = BeautifulSoup(html_content, "html.parser")
                
                # 出演者を取得
                cast = soup.find("div", class_="actor")
                cast_name = cast.text.strip() if cast else "出演者情報が見つかりません"

                # プロフィールを取得
                profile = soup.find("div", class_="profile-text")
                profile_text = profile.text.strip() if profile else "生年月日情報が見つかりません"

                # 正規表現パターン
                pattern = r"\d{4}年\d{1,2}月\d{1,2}日"

                # 正規表現で生年月日を抽出
                birthday = (re.findall(pattern, profile_text))
                if birthday:
                    birthday = birthday[0]  # リスト内から文字列として取り出す
                else:
                    # 生年月日情報が無かった場合
                    continue

                # 発売日情報を取得
                release_date = soup.find("td", class_="left", string="発売日").find_next_sibling("td").text.strip()

                # 発売当時の年齢を計算
                age_at_the_time = calc_age_at_the_time(birthday, release_date)

                # csvに追記
                writer.writerow([url, cast_name, birthday, release_date, age_at_the_time])

                # 中間ログ
                print(i, [url, cast_name, birthday, release_date, age_at_the_time])

                

        except Exception as e:
            print(f"An error occurred while accessing {url}: {e}")


