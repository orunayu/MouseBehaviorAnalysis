import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import numpy as np
import pandas as pd
import os

def plot(csv_file_path, output_file_path):
    # CSVファイルを読み込む
    df = pd.read_csv(csv_file_path)

    # 日付時刻をdatetimeオブジェクトに変換
    df['datetime'] = pd.to_datetime(df['datetime'])

    # x軸の値の位置を設定
    x = np.arange(len(df))

    # サブプロットを作成
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(20, 8))

    # ファイル名から拡張子を取り除く
    file_name_without_extension, extension = os.path.splitext(os.path.basename(csv_file_path))
    # 新しいファイル名を生成（元のファイル名+αの形）
    saveFileName = file_name_without_extension + '-plot.png'
    saveDirectory = os.path.dirname(csv_file_path)
    saveFilePath = os.path.join(saveDirectory, saveFileName)
    #グラフ全体のタイトル設定
    title = file_name_without_extension + " - rotation and mileage Data"
    fig.suptitle(title)


    # 棒グラフの幅
    width = 0.25

    #y軸の範囲決定(回転)
    rotation_min = 0
    rotation_max = max(df['odd_CWrotation'].max(), df["odd_CCWrotation"].max(), df["even_CWrotation"].max(), df["even_CCWrotation"].max())

    #y軸の範囲決定(走行距離)
    mileage_min = 0
    mileage_max = max(df['odd_mileage'].max(), df['even_mileage'].max())

    # print(f"Rmax{rotation_max}, Mmax{mileage_max}")

    # Oddデータ用の棒グラフ
    ax1.bar(x - width, df['odd_CWrotation'], width, label='Odd CW Rotation')
    ax1.bar(x, df['odd_CCWrotation'], width, label='Odd CCW Rotation')
    ax1.set_ylabel("rotation count")
    ax1.set_xticks(x)
    ax1.set_xticklabels(df['datetime'].dt.strftime('%Y-%m-%d %H:%M'))
    ax1.set_title('Odd Rotations over Time')
    ax1.set_ylim(rotation_min, rotation_max)
    #oddの走行距離
    ax1_2 = ax1.twinx()
    ax1_2.bar(x + width + width/8, df['odd_mileage'], width, label="Odd mileage", color = '#696969')
    ax1_2.set_ylabel("milage (m)")
    ax1_2.set_ylim(mileage_min, mileage_max)
    #凡例
    h1_1, l1_1 = ax1.get_legend_handles_labels()
    h1_2, l1_2 = ax1_2.get_legend_handles_labels()
    ax1.legend(h1_1+h1_2, l1_1+l1_2, loc='best')

    # Evenデータ用の棒グラフ
    ax2.bar(x - width, df['even_CWrotation'], width, label='Even CW Rotation')
    ax2.bar(x, df['even_CCWrotation'], width, label='Even CCW Rotation')
    ax2.set_ylabel("rotation count")
    ax2.set_xticks(x)
    ax2.set_xticklabels(df['datetime'].dt.strftime('%Y-%m-%d %H:%M'))
    ax2.set_title('Even Rotations over Time')
    ax2.set_ylim(rotation_min, rotation_max)
    #evenの走行距離
    ax2_2 = ax2.twinx()
    ax2_2.bar(x + width+ width/8, df['even_mileage'], width, label="Even mileage", color = '#696969')
    ax2_2.set_ylabel("milage (m)")
    ax2_2.set_ylim(mileage_min, mileage_max)
    #凡例
    h2_1, l2_1 = ax2.get_legend_handles_labels()
    h2_2, l2_2 = ax2_2.get_legend_handles_labels()
    ax2.legend(h2_1+h2_2, l2_1+l2_2, loc='best')

    # グラフ全体のタイトルと軸ラベルを設定
    plt.xlabel('Datetime')
    plt.gcf().autofmt_xdate()  # 日付のラベルを読みやすく回転
    plt.tight_layout()

    # グラフを画像ファイルとして保存（必要に応じてファイル名を変更してください）
    fig.savefig(output_file_path, dpi = 300)
    print(f'save fig: {output_file_path}')


if __name__ == "__main__":
    filePath = input("filePath: ").strip().strip('"')
    output_file_dir = input("ouput file dir: ").strip().strip('"')
    file_name_without_extension, extension = os.path.splitext(os.path.basename(filePath))
    output_file_name = file_name_without_extension + "-plot.png"
    output_file_path = os.path.join(output_file_dir, output_file_name)
    # filePath = r"PC2_2023-11-20_12-19-22_rotationData\analyzed_data\PC2_2023-11-20_12-19-22_rotationData-bundled.csv"
    # output_file_path = r"PC2_2023-11-20_12-19-22_rotationData\analyzed_data\PC2_2023-11-20_12-19-22_rotationData-barPlot.png"
    plot(filePath, output_file_path)