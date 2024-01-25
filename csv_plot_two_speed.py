#-speed専用(筐体両方のやつ) plot
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.dates as mdates

def main(csv_file_path):
    # CSVファイルを読み込む
    df = pd.read_csv(csv_file_path)

    #ファイル名等設定
    # ファイル名から拡張子を取り除く
    file_name_without_extension, extension = os.path.splitext(os.path.basename(csv_file_path))
    # 新しいファイル名を生成（元のファイル名+αの形）
    saveFileName = file_name_without_extension + '-plot.png'
    saveDirectory = os.path.dirname(csv_file_path)
    saveFilePath = os.path.join(saveDirectory, saveFileName)

    # dateとtimeを結合してdatetimeオブジェクトを作成
    df['datetime'] = pd.to_datetime(df['date'] + ' ' + df['time'])

    # odd_speedとeven_speedをy軸に設定
    datetime_values = df['datetime']
    odd_speed = df['odd_speed']
    even_speed = df['even_speed']

    # y軸の範囲を決定（余裕を持たせる）
    y_min = min(odd_speed.min(), even_speed.min())
    y_max = max(odd_speed.max(), even_speed.max())
    y_margin = (y_max - y_min) * 0.05  # 5%のマージン

    # グラフのサイズを指定（幅を大きくして横長に設定）
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(50, 6))

    #グラフ全体のタイトル設定
    title = file_name_without_extension + " - speed Data"
    fig.suptitle(title)

    # フォーマッタを設定
    formatter = mdates.DateFormatter('%Y-%m-%d %H:%M')

    # odd_speedの折れ線グラフ
    ax1.plot(datetime_values, odd_speed, linestyle='-', marker='o', markersize=1, linewidth=1, label='Odd Speed')
    ax1.set_xlabel('Datetime')
    ax1.set_ylabel('Odd Speed')
    ax1.set_title('Odd Speed over Time')
    ax1.legend()
    ax1.xaxis.set_major_locator(ticker.MaxNLocator(15))
    ax1.xaxis.set_major_formatter(formatter)
    ax1.set_xlim(datetime_values.min(), datetime_values.max())
    ax1.set_ylim(y_min - y_margin, y_max + y_margin)
    ax1.grid(True)  # グリッド線を表示
    ax1.minorticks_on()
    ax1.grid(which="minor", alpha = 0.7)

    # even_speedの折れ線グラフ
    ax2.plot(datetime_values, even_speed, linestyle='-', marker='o', markersize=1, linewidth=1, label='Even Speed')
    ax2.set_xlabel('Datetime')
    ax2.set_ylabel('Even Speed')
    ax2.set_title('Even Speed over Time')
    ax2.legend()
    ax2.xaxis.set_major_locator(ticker.MaxNLocator(15))
    ax2.xaxis.set_major_formatter(formatter)
    ax2.set_xlim(datetime_values.min(), datetime_values.max())
    ax2.set_ylim(y_min - y_margin, y_max + y_margin)
    ax2.grid(True)  # グリッド線を表示
    ax2.minorticks_on()
    ax2.grid(which="minor", alpha = 0.7)

    # グラフ全体のレイアウトを調整
    plt.tight_layout()

    # グラフを画像ファイルとして保存
    plt.savefig(saveFilePath, dpi=300)
    print(f"savefig: {saveFilePath}")

    # グラフを表示
    # plt.show()

if __name__ == "__main__":
    filePath = input("filePath: ").strip().strip('"')
    # filePath = "PC2_2023-11-20_12-19-22_rotationData/analyzed_data\PC22023-11-21_9-0-0-speed.csv"
    main(filePath)