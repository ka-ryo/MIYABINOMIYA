#config:utf-8

import numpy as np
import random
import g_class as ga
from decimal import Decimal
import midi_scan
from joblib import Parallel,delayed
from scipy.stats import norm 
import pathlib
import os
import glob
#import cupy as cp 
import time
#import chainer

def create_genom(length):
    genom_list =[]
    for i in range(length):
        genom_list.append(random.uniform(-1,1))
    return ga.genom(genom_list)

def evaluation(ga,Original_data,Practice_data,Num):
    filter_cpu = 10*np.array(ga.getGenom())


    left_dot = np.dot(10*Original_data,filter_cpu)
    left_dot = left_dot.T - 10*Practice_data
    left_dot = np.abs(left_dot)
    Sum = np.sum(left_dot) + 3.5*np.sum(np.abs(filter_cpu))

    return Sum,Num

def select_parents(ga,Parents_Number):
    random.shuffle(ga)
    result = [ga.pop(0) for i in range(Parents_Number)]
    return result

def select_children(ga,Children_number):
    sort_result = sorted(ga, key=lambda u: u.evaluation)
    #抽出
    result = [sort_result.pop(0) for i in range (Children_number)]
    return result

def crossover(ga_parent,Parents_Number,Original_data,Practice_data,row_number):
    #生成する交叉の個体数を定義
    generate_child_num = int(10*Original_data.shape[0])
    #generate_child_num = int(10*Parents_Number)
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
    evaluation_result = []
    evaluation_result = Parallel(n_jobs=1)(delayed(evaluation)(children_list[i],Original_data,Practice_data.T[row_number],i)for i in range(generate_child_num))
    sort_result = sorted(evaluation_result,key=lambda u: u[1])
    for i in range(generate_child_num):
        children_list[i].setEvaluation(sort_result[i][0])
    #残す子供を決定
    return select_children(children_list,Parents_Number)
    

def Genetic(row_number,ANS,Original_data,Practice_data,MAX_GENOM_LIST,GENOM_LENGTH,MAX_GENERATION,Parents_Number,SELECT_GENOM):
    #１世代目の個体を生成
    current_generation_individual_group = []
    current_generation_individual_group_parallel =Parallel(n_jobs=1)(delayed(create_genom)(GENOM_LENGTH)for i in range(MAX_GENOM_LIST))
    for i in range(MAX_GENOM_LIST):
        current_generation_individual_group.append(current_generation_individual_group_parallel[i])
    best_genom = current_generation_individual_group[0]
    #現世代の集合を評価
    evaluation_result = []
    evaluation_result = Parallel(n_jobs=1)(delayed(evaluation)(current_generation_individual_group[i],Original_data,Practice_data.T[row_number],i)for i in range(MAX_GENOM_LIST))
    sort_result = sorted(evaluation_result,key=lambda u: u[1])
    for i in range(MAX_GENOM_LIST) :
        current_generation_individual_group[i].setEvaluation(evaluation_result[i][0]) 
    start_time = time.time()
    #current_generation_individual_group[i].setEvaluation(evaluation_result)
    for count_ in range(1,MAX_GENERATION+1):
        
        #親個体を選択
        parents_individual = select_parents(current_generation_individual_group,Parents_Number)
        #交叉を行う
        children_individual = crossover(parents_individual,Parents_Number,Original_data,Practice_data,row_number)
        for i in range(Parents_Number):
            current_generation_individual_group.append(children_individual[i])
        
        best_check = sorted(current_generation_individual_group,key=lambda u: u.evaluation)
        if best_check[0].getEvaluation() < best_genom.getEvaluation():
            best_genom = best_check[0]
        if count_ % 1000  == 0 and count_ != MAX_GENERATION:
            #print("{}====={}===={}".format(row_number,count_,best_genom.getEvaluation()))
            elapsed_time = time.time() - start_time
            #print ("elapsed_time:{0}".format(elapsed_time) + "[sec]")

            next_generation_individual_group = []
            for i in range(SELECT_GENOM):
                next_generation_individual_group.append(best_check[i])
            next_generation_individual_group_parallel =Parallel(n_jobs=1)(delayed(create_genom)(GENOM_LENGTH)for i in range(MAX_GENOM_LIST-SELECT_GENOM))
            for i in range(MAX_GENOM_LIST-SELECT_GENOM):
                next_generation_individual_group.append(next_generation_individual_group_parallel[i])
            evaluation_result = Parallel(n_jobs=1)(delayed(evaluation)(next_generation_individual_group[i],Original_data,Practice_data.T[row_number],i)for i in range(MAX_GENOM_LIST))
            sort_result = sorted(evaluation_result,key=lambda u: u[1])
            for i in range(MAX_GENOM_LIST) :
                next_generation_individual_group[i].setEvaluation(sort_result[i][0]) 
            current_generation_individual_group = next_generation_individual_group
            #現状での適応度を配列化
            #fits = [i.getEvaluation() for i in current_generation_individual_group]
            #min_ = min(fits)
            #print ("-----{}行目第{}世代の結果-----".format(row_number,count_))
            #print ("  Min:{}".format(min_))
            #file = open("Output.txt","a")
            #file.write("\n-----{}行目第{}世代の結果-----\n".format(row_number,count_))
            #np.set_printoptions(formatter={'float': '{:.4f}'.format})
            #file.write("{}\n".format(min_))
    print ("-----最終結果-----".format(row_number,count_))
    print ("  Min:{}".format(best_genom.getEvaluation()))        
    #sort_result = sorted(current_generation_individual_group,key=lambda u: u.evaluation)
    return np.array(best_genom.getGenom()),row_number
def main():
    
    #Orignal
    #Original_data = np.random.randint(0,2,(30,25))
    Original_data = midi_scan.main("original.mid")
    Original_x = Original_data.shape[0]
    Original_y = Original_data.shape[1]

    #Practice
    #Practice_data = np.random.randint(0,2,(30,41))
    Practice_data = midi_scan.main("practice.mid")
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
    MAX_GENOM_LIST = Original_y*50
    # 遺伝子選択数
    SELECT_GENOM = int(Original_y*0.2)
   
    # 繰り返す世代数
    MAX_GENERATION = 5000
    #親世代の数
    #Parents_Number = int(MAX_GENOM_LIST*0.3)
    Parents_Number = Original_x
    start = time.time()
    #cp.cuda.set_allocator(cp.cuda.MemoryPool().malloc)
    Tmp=Parallel(n_jobs=10)(delayed(Genetic)(i,ANS,Original_data,Practice_data,MAX_GENOM_LIST,GENOM_LENGTH,MAX_GENERATION,Parents_Number,SELECT_GENOM) for i in range(Practice_y))
    #Genetic(0,ANS,Original_data,Practice_data,MAX_GENOM_LIST,GENOM_LENGTH,MAX_GENERATION,Parents_Number)
    
    elapsed_time = time.time() - start
   
    for i in range(Practice_y):
        ANS[Tmp[i][1]]=Tmp[i][0]

    with open('Filter.txt', 'w') as f_handle:
        np.savetxt(f_handle,ANS.T)
   
if __name__ == "__main__":
    #originalとpracticeのパスを取得する
    first_dir = os.getcwd()
    #print(first_dir)
    music_name_path = pathlib.Path('Dataset').glob('*')
    for name1 in music_name_path:
        practice_number = pathlib.Path('Dataset/',name1.name).glob('*')
        for name2 in practice_number:
            Save_Path = 'Dataset/{}/{}/500'.format(name1.name,name2.name)
            Original =  list(pathlib.Path('Dataset/{}/{}/500/'.format(name1.name,name2.name)).glob('original.*'))
            Practice =  list(pathlib.Path('Dataset/{}/{}/500/'.format(name1.name,name2.name)).glob('Practice.*'))
            Do_check =  list(pathlib.Path('Dataset/{}/{}/500/'.format(name1.name,name2.name)).glob('Filter.*'))
            
            if(len(Original) != 0 and len(Practice) != 0 ):
            
                print("{}/{}".format(name1.name,name2.name))
                Original_path=Original[0].resolve()
                Practice_path=Practice[0].resolve()
                os.chdir(Save_Path)    
                main()
                os.chdir(first_dir)
                