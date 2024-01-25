import csv
import os
import math
#一旦渡す用, csv分割をかけてmsを分割+datetime追加したやつを前提とする
#使い回せるように関数をちょっといじる
#出力されるspeedを改良、回転数も吐き出すようにする
#これ単体でも使えるようにする

def load_csv(filePath, column_sizse = 10, upper_index = 3):
    with open (filePath, encoding='UTF-8') as file:
        csv_reader = csv.reader(file)
        #if文で 空行、長さ10以外、upper(oneline[3])が4500じゃ無いもの は読み込まないようにしている
        csvContents = [oneline for oneline in csv_reader if oneline and len(oneline) == column_sizse and (oneline[upper_index] == "4500" or oneline[upper_index] == "4500.0")]
    return csvContents

def save_csv(filePath, add_string, csvContents):
    '''
    もともとのファイル名+add_stringの名前で与えられたcsvContentsの内容をcsvファイルとして保存する
    '''
    # ファイル名から拡張子を取り除く
    file_name_without_extension, extension = os.path.splitext(os.path.basename(filePath))
    # 新しいファイル名を生成（元のファイル名+αの形）
    saveFileName = file_name_without_extension + add_string + ".csv"
    saveDirectory = os.path.dirname(filePath)
    saveFilePath = os.path.join(saveDirectory, saveFileName)

    with open (saveFilePath, 'w', newline="") as file:
        writer = csv.writer(file)
        for element in csvContents:
            writer.writerow(element)
    print(f"save csv: {saveFilePath}")

    return saveFilePath

def compare_index(first_value, second_value):
    '''
    2つのindex(=時刻情報)を受取り、firstが早ければ(値が小さければ)Trueを、firstが遅ければ(値が大きければ)Falseを返す(値が同じ場合は考慮しない)
    '''
    if first_value < second_value:
        return True
    elif first_value > second_value:
        return False
    else:
        print("indexが一致")

def get_speed_per_second(oneSixCount, circumference):
    '''
    1秒間の回転数(スリット通過数)と直径から速度(m/s)を求める
    '''
    return oneSixCount*(circumference/6)/1000

def count_rotation(csvContents, up_threshold, down_threshold, inner_index, column_sizse = 10, upper_index = 3):
    # up_threshold = int(input("立ち上がり閾値を入力:"))
    # down_threshold = int(input("立ち下がり閾値を入力:"))
    # inner_index = 0
    # outer_index = 0
    # inner_index = int(input("inner_index: "))
    outer_index = inner_index + 1

    inner_old_value = 0
    outer_old_value = 0
    inner_digital = 0 #digitalとは言ったものの、0 or 4000
    outer_digital = 0
    for element in csvContents:
        #変な行の除外
        if len(element) != column_sizse: continue
        if element[upper_index] == "4500" or element[upper_index] == "4500.0": 
            pass
        else:
            continue
        #old_valuの代入
        inner_old_value = int(float(element[inner_index]))
        outer_old_value = int(float(element[outer_index]))
        if inner_old_value >= up_threshold:
            inner_digital = 4000
        else:
            inner_digital = 0
        if outer_old_value >= up_threshold:
            outer_digital = 4000
        else:
            outer_digital = 0
        break

    inner_rising_flag = False
    outer_rising_flag = False
    inner_rising_index = 0
    outer_rising_index = 0
    inner_maximul_index = 0 #極大値を取ったときのindex(=時刻)
    inner_minimum_index = 0 #極小値を取ったときのindex(=時刻)
    outer_maximul_index = 0
    outer_minimum_index = 0
    inner_falling_flag = False
    outer_falling_flag = False
    inner_falling_index = 0
    outer_falling_index = 0
    rising_or_falling = True #立ち上がりのときはTrue, 立ち下がりの時はFalse

    oneSixCount = 0 #6スリットなので
    clockwise_oneSixCount = 0
    counterclockwise_oneSixCount = 0
    rotationCount = 0
    clockwise_rotationCount = 0 #時計回り(右回り)
    counterclockwise_rotationCount = 0 #反時計周り(左回り)
    clockwise_rotation_flag = False
    counterclockwise_rotation_flag = False
    CW_or_CCW = True
    rotationData = [["date", "time", "millis", "inner_value", "outer_value", "inner", "outer", "rotation"]] #header

    #速度等用
    diameter = 100 #直径(mm)
    circumference = diameter*math.pi #円周の長さ(mm)
    current_time_second = 0 #秒
    next_time = 0
    oneSixCount = 0 #スリット通過数、回転方向は無視
    speed_list = []
    mileage = 0 #単位はm

    saveData = [inner_digital, outer_digital, 4000] #in, out, rotation_judge

    for i, element in enumerate(csvContents):
        #変な行の除外
        if len(element) != column_sizse: 
            print("continue")
            continue
        if element[upper_index] == "4500" or element[upper_index] == "4500.0": 
            pass
        else:
            print("continue")
            continue
        #準備
        saveData[2] = 4000
        innner_current_value =int(float(element[inner_index]))
        outer_current_value = int(float(element[outer_index]))
        current_time_second = element[1].split(":")[2]
        current_time_milli = element[2]
        if i  >= len(csvContents)-1: #末尾のとき
            inner_next_value = innner_current_value
            outer_next_value = outer_current_value
            next_time = current_time_second
        else: #それ以外(通常時)
            # print(i)
            inner_next_value = int(float(csvContents[i+1][inner_index]))
            outer_next_value = int(float(csvContents[i+1][outer_index]))
            next_time = csvContents[i+1][1].split(":")[2]#秒
        #吐き出すcsvに書き込む用
        date = element[0]
        time = element[1]
        #立ち上がりチェック
        if inner_old_value < up_threshold and innner_current_value >= up_threshold: #inner
            if  inner_digital != 4000 and not(inner_rising_flag and inner_falling_flag): #前に立ちがっていない(立ち上がり→立ち上がり判定"ではない"とき)
                inner_rising_index = i #indexを更新
            inner_rising_flag = True
            saveData[0] = 4000
            rising_or_falling = True
        if outer_old_value < up_threshold and outer_current_value >= up_threshold: #outer
            if outer_digital != 4000 and not(outer_rising_flag and outer_rising_flag):
                outer_rising_index = i
            outer_rising_flag = True
            saveData[1] = 4000
            rising_or_falling = True
        #立ち下がりチェック
        if inner_old_value > down_threshold and innner_current_value <= down_threshold:
            if inner_digital != 0 and not(inner_rising_flag and inner_falling_flag):
                inner_falling_index = i
            inner_falling_flag = True
            saveData[0] = 0
            rising_or_falling = False
        if outer_old_value > down_threshold and outer_current_value <= down_threshold:
            if outer_digital != 0 and not(outer_rising_flag and outer_falling_flag):
                outer_falling_index = i
            outer_falling_flag = True
            saveData[1] = 0
            rising_or_falling = False
        #極大、極小チェック
        #inner 極大, 極小
        if inner_old_value <= innner_current_value and innner_current_value >= inner_next_value and innner_current_value > up_threshold: inner_maximul_index = i
        if inner_old_value >= innner_current_value and innner_current_value <= inner_next_value and innner_current_value < down_threshold: inner_minimum_index = i
        #outer 極大, 極小
        if outer_old_value <= outer_current_value and outer_current_value >= outer_next_value and outer_current_value > up_threshold: outer_maximul_index = i
        if outer_old_value >= outer_current_value and outer_current_value <= outer_next_value and outer_current_value < down_threshold: outer_minimum_index = i
        #回転判定
        if inner_rising_flag and outer_rising_flag and inner_falling_flag and outer_falling_flag:
            inner_rising_flag = False
            outer_rising_flag = False
            inner_falling_flag = False
            outer_falling_flag = False
            oneSixCount += 1
            #この時点(全フラグが立った)でup,downの時刻が早い方(今立った方では無い方)の組を見て回転方向を判定(indexが一致していた場合は他見る)
            if not rising_or_falling:
                # print(f"maximul rising, time:{element[1]} i={i}, {inner_maximul_index} {outer_maximul_index}, {inner_rising_index} {outer_rising_index}", end=': ')
                if (inner_rising_index != outer_rising_index) and not (inner_rising_index == i or outer_rising_index == i):
                        CW_or_CCW = compare_index(inner_rising_index, outer_rising_index)
                        # print("rising", end=": ")
                elif (inner_maximul_index != outer_maximul_index) and not (inner_maximul_index == i or outer_maximul_index == i):
                        CW_or_CCW = compare_index(inner_maximul_index, outer_maximul_index)
                        # print("maximul", end=": ")
                else: pass #つまり前回の判定結果をそのまま使う
            if rising_or_falling:
                # print(f"minimu falling, time:{element[1]} i={i}, {inner_minimum_index} {outer_minimum_index} {inner_falling_index} {outer_falling_index}", end=': ')
                if (inner_falling_index != outer_falling_index) and not (inner_falling_index == i or outer_falling_index == i):
                        CW_or_CCW = compare_index(inner_falling_index, outer_falling_index)
                        # print("falling", end=": ")
                elif (inner_minimum_index != outer_minimum_index) and not (inner_minimum_index == i or outer_minimum_index == i):
                        CW_or_CCW = compare_index(inner_minimum_index, outer_minimum_index)
                        # print("minimum", end=": ")
                else: pass
            # print(CW_or_CCW)
            if CW_or_CCW: #CW_or_CCW= Trueなら時計回り,Falseなら反時計回り
                clockwise_oneSixCount += 1
                saveData[2] = 4100
            else:
                counterclockwise_oneSixCount += 1
                saveData[2] = 3900
        #速度算出
        if current_time_second != next_time: #一秒経過
            speed = get_speed_per_second(oneSixCount, circumference)
            speed_list.append([date, time, current_time_milli, speed, oneSixCount]) #["date", "time", "millis", "speed"]
            oneSixCount = 0
            mileage = mileage + speed
        #old_elementに値をいれる
        inner_old_value = int(float(element[inner_index]))
        outer_old_value = int(float(element[outer_index]))
        inner_digital = saveData[0]
        outer_digital = saveData[1]
        #ファイルに解析結果を保存
        #["date", "time", "millis", "inner_value", "outer_value", "inner", "outer", "rotation"]
        rotationData.append([date, time, current_time_milli, innner_current_value, outer_current_value, saveData[0], saveData[1], saveData[2]])

    rotationCountDict = {
        'clockwise_rising':clockwise_oneSixCount,
        'clockwise_rotation':int(clockwise_oneSixCount/6), #intにキャストしなければそれれで小数点まで出る感じになる(お好みで)
        'counterclockwise_rising':counterclockwise_oneSixCount,
        'counterclockwise_rotation':int(counterclockwise_oneSixCount/6),
    }
    return rotationCountDict, rotationData, speed_list, mileage

#これが実質main関数
def csv_analysis():
    filePath = input("csvFilePath: ").strip().strip('"')
    # filePath = "csvTestData/LRturn3.csv"
    csvContents = load_csv(filePath)
    # print(csvContents[:3])

    inner_index = 0
    one_or_two = int(input("1 or 2(1なら前半データ(奇数番目筐体)、2なら後半データ(偶数番目筐体)を解析): "))
    if one_or_two == 1:
        inner_index = 5
    elif one_or_two == 2:
        inner_index = 7
    else:
        print("1か2だけを入力してください")
        exit()
    # print(f"inner_index = {inner_index}")

    # up_threshold = 2500
    up_threshold = int(input("立ち上がり閾値を入力(半角整数で): "))
    # down_threshold = 2000
    down_threshold = int(input("立ち下がり閾値を入力(半角整数で): "))

    rotation_count, rotationData, speed_list, mailaege = count_rotation(csvContents, up_threshold, down_threshold, inner_index)

    file_name = os.path.basename(filePath)
    save_dir = os.path.dirname(filePath)
    save_dir = os.path.join(save_dir, "analyzed_data")
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    save_file_path = os.path.join(save_dir, file_name)
    save_csv(save_file_path, f'-analyzed_innner{inner_index}', rotationData)
    save_csv(save_file_path, f'-speed_innner{inner_index}', speed_list)

    print(f"時計回り= {rotation_count['clockwise_rotation']}+{rotation_count['clockwise_rising']%6}/6, 反時計回り= {rotation_count['counterclockwise_rotation']}+{rotation_count['counterclockwise_rising']%6}/6, 合計回転数= {rotation_count['clockwise_rotation'] + rotation_count['counterclockwise_rotation']}")
    print(f"時計立ち上がり{rotation_count['clockwise_rising']}, 反時計立ち上がり{rotation_count['counterclockwise_rising']}")
    input("Enterキーを押すと終了します")
        

if __name__ == "__main__":
    csv_analysis()