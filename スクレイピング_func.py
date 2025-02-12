import csv
import matplotlib.pyplot as plt
import numpy as np
import codecs

### 一作品に複数モデルが登場している作品は除外して、新たにcsvファイルに書き出す。
# new_csv_data = []

# with open("output.csv", newline = "", encoding = "cp932") as f:
#     reader = csv.reader(f)
#     for row in reader:
        
#         DVD_url, cast_name, birth_date, release_date, age_at_release = row

#         if "／" not in cast_name:
#             new_csv_data.append(row)


# with open("output2.csv", "w", newline = "") as f:
#     writer = csv.writer(f)
#     for row in new_csv_data:
#         writer.writerow(row)


### データ分析
# age_list = []

# with open("output2.csv", newline = "", encoding = "cp932") as f:
#     reader = csv.reader(f)
    
#     for row in reader:
        
#         DVD_url, cast_name, birth_date, release_date, age_at_release = row

#         age_at_release = int(age_at_release)
#         age_list.append(age_at_release)

# plt.boxplot(age_list, whis = 100)
# plt.hist(age_list, bins = len(set(age_list)))
# plt.show()


# 文字エンコーディングを変換
with codecs.open('output2.csv', 'r', encoding='cp932') as infile:
    content = infile.read()

with codecs.open('output4.csv', 'w', encoding='utf-8') as outfile:
    outfile.write(content)

