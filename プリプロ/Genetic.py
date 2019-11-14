#config:utf-8

import numpy as np
import random
import g_class as ga
from decimal import Decimal
import midi_scan
from joblib import Parallel,delayed
from scipy.stats import norm 
import cupy as cp 
#import chainer

def create_genom(length):
    genom_list =[]
    for i in range(length):
        genom_list.append(random.uniform(-1,1))
    return ga.genom(genom_list)

def evaluation(ga,Original_data,Practice_data,Num):
    filter_cpu = np.array(ga.getGenom())

    #GPUで使えるデータの形にする
    filter_gpu = cp.asarray(filter_cpu)
    Original_data_gpu = cp.asarray(Original_data)
    Practice_data_gpu = cp.asarray(Practice_data)

    #オリジナルとフィルターの積を出す
    left_dot_gpu = cp.dot(Original_data_gpu,filter_gpu)

    left_dot = np.dot(Original_data,filter_cpu)
    left_dot = left_dot.T - Practice_data
    left_dot = np.abs(left_dot)

    return np.sum(left_dot),Num

def select_parents(ga,Parents_Number):
    random.shuffle(ga)
    result = [ga.pop(0) for i in range(Parents_Number)]
    return result

def select_children(ga,Children_number):
    sort_result = sorted(ga, key=lambda u: u.evaluation)
    #抽出
    result = [sort_result.pop(0) for i in range (Children_number)]
    return result

def crossover(ga_parent,Parents_Number,n,Original_data,Practice_data,row_number):
    #生成する交叉の個体数を定義
    generate_child_num = int(10*Original_data.shape[0])
    #生成した子供を保存
    children_list = []
    #重心を求める
    Sum = np.array(ga_parent[0].getGenom())
    for i in range(1,Parents_Number):
        Sum+= np.array(ga_parent[i].getGenom())
    Center_of_gravity = np.array(Sum) / Parents_Number
    #確立変数を宣言
    random_variable = norm.rvs(loc=0,scale=(1/generate_child_num),size=generate_child_num)
    #子供の生成
    for i in range(generate_child_num):
        children_list.append(ga.genom(Center_of_gravity+random_variable[i]))
    #子供を評価
    for i in range(generate_child_num):
        evaluation_result = evaluation(children_list[i],Original_data,Practice_data.T[row_number])
        children_list[i].setEvaluation(evaluation_result)
    #残す子供を決定
    return select_children(children_list,Parents_Number)
    

def Genetic(row_number,ANS,Original_data,Practice_data,MAX_GENOM_LIST,GENOM_LENGTH,MAX_GENERATION,Parents_Number):
    #１世代目の個体を生成
    current_generation_individual_group = []
    for i in range(MAX_GENOM_LIST):
        current_generation_individual_group.append(create_genom(GENOM_LENGTH))
    #現世代の集合を評価
    evaluation_result = []
    evaluation_result = Parallel(n_jobs=-1)(delayed(evaluation)(current_generation_individual_group[i],Original_data,Practice_data.T[row_number],i)for i in range(MAX_GENOM_LIST))
    sort_result = sorted(evaluation_result,key=lambda u: u[1])
    for i in range(MAX_GENOM_LIST) :
        current_generation_individual_group[i].setEvaluation(evaluation_result[i][0]) 
    #current_generation_individual_group[i].setEvaluation(evaluation_result)
    for count_ in range(1,MAX_GENERATION+1):  
        
        #親個体を選択
        parents_individual = select_parents(current_generation_individual_group,Parents_Number)
        #交叉を行う
        children_individual = crossover(parents_individual,Parents_Number,Original_data.shape[1],Original_data,Practice_data,row_number)
        for i in range(Parents_Number):
            current_generation_individual_group.append(children_individual[i])
        #突然変異
        if count_ % MAX_GENERATION == 10000:
            #現状での適応度を配列化
            fits = [i.getEvaluation() for i in current_generation_individual_group]
            min_ = min(fits)
            print ("-----{}行目第{}世代の結果-----".format(row_number,count_))
            print ("  Min:{}".format(min_))
    sort_result = sorted(current_generation_individual_group,key=lambda u: u.evaluation)
    return np.array(sort_result[0].getGenom()),row_number
def main():
    #Orignal
    #Original_data = np.random.randint(0,2,(30,25))
    Original_data = midi_scan.main("Original.mid")
    Original_x = Original_data.shape[0]
    Original_y = Original_data.shape[1]

    #Practice
    #Practice_data = np.random.randint(0,2,(30,41))
    Practice_data = midi_scan.main("Practice.mid")
    Pracrice_x = Practice_data.shape[0]
    Practice_y = Practice_data.shape[1]

    #結果を保存する配列
    ANS = np.empty((Practice_y,Original_y))
    ANS.flags.writeable = True

    print("============Original==============")
    print(Original_data.shape)
    print("============Practice==============")
    print(Practice_data.shape)

    # 遺伝子情報の長さ
    GENOM_LENGTH = Original_y
    # 遺伝子集団の大きさ
    MAX_GENOM_LIST = Practice_y*50
    # 遺伝子選択数
    SELECT_GENOM = int(Original_y*0.3)
   
    # 繰り返す世代数
    MAX_GENERATION = 10
    #親世代の数
    Parents_Number = 100
    cp.cuda.set_allocator(cp.cuda.MemoryPool().malloc)
    Tmp=Parallel(n_jobs=-1)(delayed(Genetic)(i,ANS,Original_data,Practice_data,MAX_GENOM_LIST,GENOM_LENGTH,MAX_GENERATION,Parents_Number) for i in range(Practice_y))
    Genetic(0,ANS,Original_data,Practice_data,MAX_GENOM_LIST,GENOM_LENGTH,MAX_GENERATION,Parents_Number)
    for i in range(Practice_y):
        ANS[Tmp[i][1]]=Tmp[i][0]

    with open('TestTexr.txt', 'a') as f_handle:
        np.savetxt(f_handle,ANS.T,fmt='%4.3f')

if __name__ == "__main__":
    main()