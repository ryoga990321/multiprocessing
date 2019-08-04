import random

def create(num): #指定した数のデータ配列を作成する関数
    data=[]
    for i in range(num):
        data.append(random.randint(1,1001))
    return data

file_name = "./Parallel.txt" #データを書き込むファイル先のパス
data=create(1000000)

try:            #ファイル書き込み
    file = open(file_name, 'w')
    for i in data:
        file.write(str(i)+"\n")
except Exception as e:
    print(e)
finally:
    file.close()
