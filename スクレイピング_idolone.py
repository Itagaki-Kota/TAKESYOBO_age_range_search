import requests
import time
from bs4 import BeautifulSoup
import csv

def cleansing_release_date(release_date):
    # 末尾の 発売予定 などの文字を削除し、Y年M月D日 の文字列だけで抽出する
    release_date = release_date.replace("年", "/")
    release_date = release_date.replace("月", "/")
    release_date = release_date.replace("日", "/")

    release_year, release_month, release_day, garbage = release_date.split("/")
    release_year, release_month, release_day = release_year.strip(), release_month.strip(), release_day.strip()
    
    return f"{release_year}年{release_month}月{release_day}日"

def get_birth_date(profile_link):
    # プロフィール情報のリンク先にアクセスし、生年月日情報を取得する。不詳なら空文字列。
    url = f"https://www.i-one-net.com{profile_link}"

    # 各URLにアクセスしてHTMLを取得
    try:
        # URLにアクセス
        time.sleep(interval)
        response = requests.get(url)
        
        # ステータスコードが200であれば成功
        if response.status_code == 200:
            # ページのHTMLを取得
            html_content = response.text
            
            # BeautifulSoupでHTMLを解析
            soup = BeautifulSoup(html_content, "html.parser")
            
            # 生年月日情報を取得
            birth_date = soup.find("th", string="生年月日").find_next_sibling("td").text.strip()
            
            if "年" not in birth_date or "月" not in birth_date or "日" not in birth_date:
                birth_date = ""
            
            return birth_date

    except Exception as e:
        print(f"An error occurred while accessing {url}: {e}")


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


# 過度なリクエストを防止するためのインターバル (sec)
interval = 3

# DVD(orBD)のidの範囲
min_item_id = 1766
max_item_id = 1875

with open("output_idolone.csv", "a", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)

    # URLリストを表示
    for item_id in range(min_item_id, max_item_id + 1):
        time.sleep(interval)
        item_url = f"https://www.i-one-net.com/item/{item_id}"

        # 各URLにアクセスしてHTMLを取得
        try:
            # URLにアクセス
            response = requests.get(item_url)
            
            # ステータスコードが200であれば成功
            if response.status_code == 200:
                # ページのHTMLを取得
                html_content = response.text
                
                # BeautifulSoupでHTMLを解析
                soup = BeautifulSoup(html_content, "html.parser")
                
                # 「プロフィールを見る」のボタンのリンク先URLを取得
                a_tag = soup.find('a', string="プロフィールを見る")
                # href 属性を取得
                if a_tag:
                    profile_link = a_tag.get('href')
                    birth_date = get_birth_date(profile_link)
                    if not birth_date:
                        continue
                else:
                    continue
                
                # 発売日情報を取得
                release_date_raw = soup.find("th", string="発売日").find_next_sibling("td").text.strip()
                release_date = cleansing_release_date(release_date_raw)

                # 発売当時の年齢を計算
                age_at_the_time = calc_age_at_the_time(birth_date, release_date)

                # csvに追記 (cast_name は未取得)
                writer.writerow([item_url, "",  birth_date, release_date, age_at_the_time])

                # 中間ログ
                print(item_id, [item_url, "", birth_date, release_date, age_at_the_time])
                

        except Exception as e:
            print(f"An error occurred while accessing {item_url}: {e}")


