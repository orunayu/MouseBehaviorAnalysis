import pandas as pd
import os
#先生作のプログラム2つを合体させた
#csvの時間の部分を 時:分:秒 と ミリ秒 に分けるプログラム + csvファイルを１時間毎に切り分けるプログラム

def extract_and_move_milliseconds(input_file_path):
    '''
    csvファイルのtime列を "時:分:秒" と"ミリ秒" に分割する
    '''
    # CSVファイルを読み込む
    column_names = ["date", "time", "upper", "lower", "value1-1", "value1-2", "value2-1", "value2-2"]
    df = pd.read_csv(input_file_path, skiprows=20, header=None, names=column_names) #注意：先頭20行はスルー(削除)している

    # time列を時:分:秒とミリ秒に分割
    time_split = df['time'].str.split(':', expand=True)
    df['ms'] = time_split[3]
    df['time'] = time_split[0] + ':' + time_split[1] + ':' + time_split[2]

    # ms列をtime列の隣（3列目）に挿入
    df.insert(2, 'ms', df.pop('ms'))

    # 元のファイル名に接尾辞を追加して新しい出力ファイル名を生成
    dir_name, file_name = os.path.split(input_file_path)
    new_file_name = 'Postprocess_' + os.path.splitext(file_name)[0] + '.csv'
    output_file_path = os.path.join(dir_name, new_file_name)

    # 変更を新しいファイルに保存
    df.to_csv(output_file_path, index=False)
    print(f'File saved: {output_file_path}')

    return output_file_path

def split_csv_by_hour(input_file_path, output_dir, chunksize=100000):
    '''
    csvファイルのタイムスタンプを見て、一時間ごとに切り分けて保存する。
    保存されるファイル名にはその時刻の日付が追加される。
    '''
    file_name_without_extension, extension = os.path.splitext(os.path.basename(input_file_path))

    # CSVファイルをチャンクで読み込む
    for chunk in pd.read_csv(input_file_path, chunksize=chunksize):
        # 日付と時間の列を結合してdatetimeオブジェクトに変換
        chunk['datetime'] = pd.to_datetime(chunk['date'] + ' ' + chunk['time'])

        # 日付と時間ごとにデータを分割
        for _, group in chunk.groupby([chunk['datetime'].dt.date, chunk['datetime'].dt.hour]):
            date_str = group['datetime'].dt.date.iloc[0].strftime('%Y-%m-%d')
            hour = group['datetime'].dt.hour.iloc[0]
            
            # 新しいファイル名を生成して保存
            file_name_head = file_name_without_extension.split("_")[1]
            new_file_name = f'{file_name_head}_rotationData_{date_str}_hour-{hour}.csv'
            new_file_path = os.path.join(output_dir, new_file_name)
            group.to_csv(new_file_path, mode='a', header=not os.path.exists(new_file_path), index=False)

            num_rows = len(group)
            print(f'File saved: {new_file_path} with {num_rows} rows')


def main():
    # ユーザーから入力ファイルパスを取得
    input_file_path = input("Enter the path of the input CSV file: ").strip().strip('"')

    #出力ディレクトリ確認(存在しなければ作成)
    file_name_without_extension, extension = os.path.splitext(os.path.basename(input_file_path))
    output_dir = file_name_without_extension
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    postprocess_file_path = extract_and_move_milliseconds(input_file_path)
    split_csv_by_hour(postprocess_file_path, output_dir)


if __name__ == "__main__":
    main()