#ミリ秒を分割したcsv専用 plot
#筐体２つ分のrawデータの波形グラフを表示
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import datetime
import os

# CSVファイルからデータを読み込む
# filePath = 'csvTestData/LRturn2-cliped-analyzed.csv'
filePath = input("filePath: ").strip().strip('"')
original_data = pd.read_csv(filePath)
#original_data = pd.read_csv(filePath)
#不正確な行(NaNを含む行)を削除
original_data = original_data.dropna()

# データの最初の数行を表示して確認
print(original_data)

#ファイル名等設定
# ファイル名から拡張子を取り除く
file_name_without_extension, extension = os.path.splitext(os.path.basename(filePath))
# 新しいファイル名を生成（元のファイル名+αの形）
saveFileName = file_name_without_extension + '-plot.png'
saveDirectory = os.path.dirname(filePath)
saveFilePath = os.path.join(saveDirectory, saveFileName)

#OverflowError: Exceeded cell block limit (set 'agg.path.chunksize' rcparam) 対策?
plt.rcParams['agg.path.chunksize'] = 10000

x_data = original_data['ms']

# グラフの描画
fig = plt.figure(figsize=[150,20])
title = saveFileName + " Waveform Data"
fig.suptitle(title)

ax1 = fig.add_subplot(2, 1, 1)
ax2 = fig.add_subplot(2, 1, 2)
# x軸の範囲を明示的に指定して余白を最小限にする
ax1.set_xlim(original_data['ms'].min(), original_data['ms'].max())
ax2.set_xlim(original_data['ms'].min(), original_data['ms'].max())


#-折れ線グラフ
ax1.plot(x_data, original_data['value1-1'], label='inner value')
ax1.plot(x_data, original_data['value1-2'], label='outer value')
ax2.plot(x_data, original_data['value2-1'], label='inner value')
ax2.plot(x_data, original_data['value2-2'], label='outer value')

#-散布図
ax1.scatter(x_data, original_data['value1-1'], label='inner value', s=10)
ax1.scatter(x_data, original_data['value1-2'], label='outer value', s=10)
ax2.scatter(x_data, original_data['value2-1'], label='inner value', s=10)
ax2.scatter(x_data, original_data['value2-2'], label='outer value', s=10)


# グラフにタイトルや軸ラベルを追加することもできます
ax1.set_title("value1")
ax2.set_title("value2")
ax1.set_xlabel('Time')
ax1.set_ylabel('sensor analog value')
ax2.set_xlabel('Time')
ax2.set_ylabel('sensor analog value')

# 凡例を表示
ax1.legend()
ax2.legend()

#その他グラフの調整
# step_num = (original_data["millis"].max() - original_data["millis"].min())/30
# plt.xticks(np.arange(original_data['millis'].min(), original_data["millis"].max(), step = step_num))
ax1.minorticks_on()
ax1.grid(True) #グリッド線の表示
ax1.grid(which="minor", alpha = 0.7)
ax2.minorticks_on()
ax2.grid(True) #グリッド線の表示
ax2.grid(which="minor", alpha = 0.7)
fig.tight_layout(rect=[0,0,1,0.96]) # タイトルの被りを防ぐ??


# グラフを画像ファイルとして保存
plt.savefig(saveFilePath)
print(f"savefig: {saveFilePath}")