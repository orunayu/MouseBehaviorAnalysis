#-analyzed_inner〇専用 plot
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import datetime
import os

def plot(filePath):
    original_data = pd.read_csv(filePath)
    #original_data = pd.read_csv(filePath)
    #不正確な行(NaNを含む行)を削除
    original_data = original_data.dropna()

    # print(original_data)

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

    # グラフの描画
    plt.figure(figsize=[200,10])

    # x軸の範囲を明示的に指定して余白を最小限にする
    plt.xlim(original_data['millis'].min(), original_data['millis'].max())
    #print("x_range= ", plt.xlim())

    x_data = original_data['millis']

    #-折れ線グラフ
    plt.plot(x_data, original_data['inner_value'], label='inner value')
    plt.plot(x_data, original_data['outer_value'], label='outer value')
    plt.plot(x_data, original_data["inner"], label = "inner", alpha = 0.5)
    plt.plot(x_data, original_data["outer"], label = "outer", alpha = 0.5)
    plt.plot(x_data, original_data["rotation"], label = "rotation", alpha = 0.5)

    #-散布図
    plt.scatter(x_data, original_data['inner_value'], label='inner value', s=10)
    plt.scatter(x_data, original_data['outer_value'], label='outer value', s=10)
    plt.scatter(x_data, original_data["inner"], label = "inner", s=10)
    plt.scatter(x_data, original_data["outer"], label = "outer",s=10)
    plt.scatter(x_data, original_data["rotation"], label = "rotation",s=10)


    # グラフにタイトルや軸ラベルを追加することもできます
    title = file_name_without_extension + " - Waveform Data"
    plt.title(title)
    plt.xlabel('Time')
    plt.ylabel('sensor analog value')

    # 凡例を表示
    plt.legend()

    #その他グラフの調整
    # step_num = (original_data["millis"].max() - original_data["millis"].min())/30
    # plt.xticks(np.arange(original_data['millis'].min(), original_data["millis"].max(), step = step_num))
    plt.minorticks_on()
    plt.grid(True) #グリッド線の表示
    plt.grid(which="minor", alpha = 0.7)
    plt.tight_layout() # タイトルの被りを防ぐ??


    # グラフを画像ファイルとして保存
    plt.savefig(saveFilePath)
    print(f"savefig: {saveFilePath}")

if __name__ == "__main__":
    # CSVファイルからデータを読み込む
    # filePath = 'csvTestData/LRturn2-cliped-analyzed.csv'
    filePath = input("filePath: ").strip().strip('"')
    plot(filePath)