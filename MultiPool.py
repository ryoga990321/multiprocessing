import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from multiprocessing import Pool
import multiprocessing as multi
import time

def merge_sort(array): #マージソートを行う関数
    mid = len(array)
    if mid > 1:
        left = merge_sort(array[:(mid//2)])
        right = merge_sort(array[(mid//2):])
        result=merge(left,right)
        return result
    else:
        return array

def merge(left, right): #マージを行う関数
    sorted_list = []
    left_index = 0
    right_index = 0

    while left_index < len(left) and right_index < len(right):
        if left[left_index] <= right[right_index]:
            sorted_list.append(left[left_index])
            left_index += 1
        else:
            sorted_list.append(right[right_index])
            right_index += 1

    if left:
        sorted_list.extend(left[left_index:])
    if right:
        sorted_list.extend(right[right_index:])

    return sorted_list

def n_merge(num,array3): #2分割になるまでmerge
    array4=[]
    for i in range(num//2):
        sample=[]
        sample.append(array3[2*i])
        sample.append(array3[2*i+1])
        array4.append(sample)
    p = Pool(processes=num//2) #マージの並列化
    array3=p.map(wrapper, array4)
    p.close()
    if num//2>=4:
        return n_merge(num//2,array3)

    return array3


def wrapper(args): #ラッパー関数
    return merge(*args)

def main():
    file_name = "./Parallel.txt" #データを読み込むファイル先のパス
    data=[]                      #マージソートのデータ用リスト
    data_num=1000000             #データ数
    x=[]                         #グラフのx軸のデータ
    y=[]                         #グラフのy軸のデータ
    for i in range(1,6):
        pro=2**(i-1)             #プロセス数
        pro_num=data_num//pro

        try:                           #ファイル読み込み
            file = open(file_name)
            lines = file.readlines()
            for i in range(data_num):
                data.append(int(lines[i].rstrip("\n")))
        except Exception as e:
            print(e)
        finally:
            file.close()

        pro_data=[]           #プロセス数分割
        for i in range(pro):
            pro_data.append(data[i*pro_num:(i+1)*pro_num])

        start = time.time()        #並列化を始めた時間
        p = Pool(processes=pro)    #マージソートの並列化
        futures=p.map(merge_sort, pro_data)
        p.close()

        if pro>=2:
            if pro>=4:
                futures=n_merge(pro,futures)
            futures=merge(futures[0],futures[1])
        else:
            futures=futures[0]

        end1 = time.time() - start     #並列化を終えた時間
        print("並列実行時間："+str(end1)+"秒")
        x.append(pro)
        y.append(end1)

    x=np.array(x)                      #グラフ設定
    y=np.array(y)
    plt.plot(x, y)
    plt.title("process-time relation")
    plt.xlabel("process")
    plt.ylabel("time(seconds)")
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main()
