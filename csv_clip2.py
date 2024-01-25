#csvファイルから特定の範囲の行を抜き出すプログラム
#pandasを使わずヘッダーに頼らない、完全にそのまま切り出す
import csv
import os

# 元のCSVファイル読み込み
filePath = input("filePaht:").strip().strip('"')

with open (filePath, encoding='UTF-8') as file:
    csv_reader = csv.reader(file)
    csvContents = [oneline for oneline in csv_reader]

# 抽出したい行数の範囲を指定
start_row = input("start_row(1以上):")
end_row = input("end_row:")
# print(f"start row: {start_row}, end row: {end_row}")

# 特定の範囲の行を抜き出す
extracted_data = csvContents[int(start_row)-1:int(end_row)]
if start_row != "1":
    extracted_data.insert(0, csvContents[0])

# ファイル名から拡張子を取り除く
file_name_without_extension, extension = os.path.splitext(os.path.basename(filePath))
# 新しいファイル名を生成（元のファイル名+αの形）
saveFileName = file_name_without_extension + f'-cliped{start_row}-{end_row}.csv'
saveDirectory = os.path.dirname(filePath)
saveFilePath = os.path.join(saveDirectory, saveFileName)

# 正しい形に修正されたCSVファイルを保存
with open (saveFilePath, 'w', newline="") as file:
    writer = csv.writer(file)
    for element in extracted_data:
        writer.writerow(element)
print(f'File saved: {saveFilePath}')