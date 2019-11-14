#coding:utf-8

import numpy as np
#import cupy as cp
import random
import g_class as ga
from decimal import Decimal
import midi_scan
from joblib import Parallel,delayed

#Orignal
Original_data = np.random.randint(0,2,(1,4))
#Original_data = midi_scan.main("Original.mid")
Original_x = Original_data.shape[0]
Original_y = Original_data.shape[1]

#Practice
Practice_data = np.random.randint(0,2,(1,3))
#Practice_data = midi_scan.main("Practice.mid")
Pracrice_x = Practice_data.shape[0]
Practice_y = Practice_data.shape[1]


#フィルター
x = np.zeros(shape=(Original_y,Practice_y),dtype="float")

# 遺伝子情報の長さ
GENOM_LENGTH = Original_y
# 遺伝子集団の大きさ
MAX_GENOM_LIST = Original_y
# 遺伝子選択数
SELECT_GENOM =20
# 個体突然変異確率
INDIVIDUAL_MUTATION = 1
# 遺伝子突然変異確率
GENOM_MUTATION = 0.95
# 繰り返す世代数
MAX_GENERATION = 100000


def create_genom(length):
    """
    引数で指定された桁のランダムな遺伝子情報を生成、格納したgenomClassで返します。
    :param length: 遺伝子情報の長さ
    :return: 生成した個体集団genomClass
    """
    genome_list = []
    for i in range(length):
        genome_list.append(random.uniform(-1,1))
   
    return ga.genom(genome_list, 0)


def evaluation(ga,row_num):
    """
    :A*Filter
    :param ga: 評価を行うgenomClass
    :return: 評価処理をしたgenomClassを返す
    """
    filter_cpu = np.array(ga.getGenom())
    """
    filter_gpu = cp.asarray(filter_cpu)
    Original_Data_gpu =cp.asarray(Original_data)
    dot_gpu = cp.dot(Original_Data_gpu,filter_gpu)
    
    dot_gpu = dot_gpu.T -cp.asarray(Practice_data.T[row_num])
    dot_gpu = dot_gpu**2
    """
    left_dot = np.dot(Original_data,filter_cpu) 
    left_dot = left_dot.T - Practice_data.T[row_num] 
    left_dot = np.abs(left_dot)

    #return -1
    return -1*np.sum(left_dot)

def select(ga, elite_length):
    """選択関数です。エリート選択を行います
    評価が高い順番にソートを行った後、一定以上
    :param ga: 選択を行うgenomClassの配列
    :param elite_length: 選択するエリートの数
    :return: 選択処理をした一定のエリート、genomClassを返す
    """
    # 現行世代個体集団の評価を高い順番にソートする
    sort_result = sorted(ga, reverse=True, key=lambda u: u.evaluation)
    # 一定の上位を抽出する
    result = [sort_result.pop(0) for i in range(elite_length)]
    print(result[0].getGenom()[0])
    print(result[0].getGenom()[1])
    print(result[0].getGenom()[2])
    print(result[0].getGenom()[3])
    return result

def crossover(ga_one, ga_second):
    """交叉関数です。二点交叉を行います。
    :param ga: 交叉させるgenomClassの配列
    :param ga_one: 一つ目の個体
    :param ga_second: 二つ目の個体
    :return: 二つの子孫genomClassを格納したリスト返す
    """

    # 子孫を格納するリストを生成します
    genom_list = []

    child1 = ga_one.getGenom()
    child2 = ga_second.getGenom()
    for i in range(len(ga_one.getGenom())):
        if random.SystemRandom().random()<0.5:
            child1[i],child2[i] = child2[i],child1[i]
    genom_list.append(ga.genom(child1,0))
    genom_list.append(ga.genom(child2,0))

    """
    # 入れ替える二点の点を設定します→[10:25]→10から25まで
    cross_one = random.randint(0, GENOM_LENGTH)
    cross_second = random.randint(cross_one, GENOM_LENGTH)
    # 遺伝子を取り出します
    one = ga_one.getGenom()
    second = ga_second.getGenom()
    # 交叉させます
    progeny_one = one[:cross_one] + second[cross_one:cross_second] + one[cross_second:]
    progeny_second = second[:cross_one] + one[cross_one:cross_second] + second[cross_second:]
    # genomClassインスタンスを生成して子孫をリストに格納する
    genom_list.append(ga.genom(progeny_one, 0))
    genom_list.append(ga.genom(progeny_second, 0))
    """
    return genom_list

def next_generation_gene_create(ga, ga_elite, ga_progeny):
    """
    世代交代処理を行います
    :param ga: 現行世代個体集団
    :param ga_elite: 現行世代エリート集団
    :param ga_progeny: 現行世代子孫集団
    :return: 次世代個体集団
    """
    # 現行世代個体集団の評価を低い順番にソートする
    next_generation_geno = sorted(ga, reverse=False, key=lambda u: u.evaluation)
    # 追加するエリート集団と子孫集団の合計ぶんを取り除く
    for i in range(0, len(ga_progeny)):
        next_generation_geno.pop(0)
    # エリート集団と子孫集団を次世代集団を次世代へ追加します
    #next_generation_geno.extend(ga_elite)
    next_generation_geno.extend(ga_progeny)
    return next_generation_geno

def mutation(ga, individual_mutation, genom_mutation):
    """突然変異関数です。
    :param ga: 突然変異をさせるgenomClass
    :param individual_mutation: 固定に対する突然変異確率
    :param genom_mutation: 遺伝子一つ一つに対する突然変異確率
    :return: 突然変異処理をしたgenomClassを返す"""
    ga = sorted(ga, reverse=True, key=lambda u: u.evaluation)
    ga_list = []
    flag1 = 0
    flag2 = 0
    for i in ga:
        if i.getEvaluation()!=0 and flag2==0:
            flag1 = 1
            flag2 = 1
        if flag1 == 0:
            # 個体に対して一定の確率で突然変異が起きる
            if individual_mutation > (random.randint(0, 100) / Decimal(100)):
                genom_list = i.getGenom()
                change_point = random.randint(0,GENOM_LENGTH-1)
                genom_list[change_point] = random.uniform(-1,1)
                i.setGenom(genom_list)
                """
                for i_ in i.getGenom():
                    # 個体の遺伝子情報一つ一つに対して突然変異がおこる
                    if genom_mutation > (random.randint(0, 100) / Decimal(100)):
                        genom_list.append(random.uniform(-1,1))
                    else:
                        genom_list.append(i_)
                i.setGenom(genom_list)
                """
                ga_list.append(i)
            else:
                ga_list.append(i)
        else:
            ga_list.append(i)
        flag1=0
    return ga_list


def Genetic(Roop_Num,ANS):
    # 一番最初の現行世代個体集団を生成します。
    current_generation_individual_group = []
    for i in range(MAX_GENOM_LIST):
        current_generation_individual_group.append(create_genom(GENOM_LENGTH))

    for count_ in range(1, MAX_GENERATION + 1):
        # 現行世代個体集団の遺伝子を評価し、genomClassに代入します
        for i in range(MAX_GENOM_LIST):
            evaluation_result = evaluation(current_generation_individual_group[i],Roop_Num)
            current_generation_individual_group[i].setEvaluation(evaluation_result)
        # エリート個体を選択します
        elite_genes = select(current_generation_individual_group,SELECT_GENOM)
        Keep_genes = elite_genes[0]
        #--------------Test---------------------------------------------------------------------
        #次世代の配列を作成
        progeny_gene =[]
        #選ばれた前世代のなかで交叉を行う
        while len(progeny_gene) <MAX_GENOM_LIST - SELECT_GENOM:
            parent1= random.SystemRandom().randint(0,SELECT_GENOM-1)
            parent2= random.SystemRandom().randint(0,SELECT_GENOM-1)
            progeny_gene.extend(crossover(elite_genes[parent1],elite_genes[parent2]))

        
        """
        # エリート遺伝子を交叉させ、リストに格納します
        progeny_gene = []
        for i in range(0, SELECT_GENOM):
            progeny_gene.extend(crossover(elite_genes[i - 1], elite_genes[i]))
        """
        # 次世代個体集団を現行世代、エリート集団、子孫集団から作成します
        next_generation_individual_group = next_generation_gene_create(current_generation_individual_group,elite_genes, progeny_gene)
        # 次世代個体集団全ての個体に突然変異を施します。
        next_generation_individual_group = mutation(next_generation_individual_group,INDIVIDUAL_MUTATION,GENOM_MUTATION)
        next_generation_individual_group[0] =Keep_genes
        # 1世代の進化的計算終了。評価に移ります

        # 各個体適用度を配列化します。
        fits = [i.getEvaluation() for i in current_generation_individual_group]
        print(fits)
        # 進化結果を評価します
        min_ = min(fits)
        max_ = max(fits)
        avg_ = sum(fits) / (len(fits))
        if count_%1 == 0:
            """
            file = open("Output.txt","a")
            file.write("\n-----{}行目第{}世代の結果-----\n".format(Roop_Num,count_))
            np.set_printoptions(formatter={'float': '{:.4f}'.format})
            #file.write("  Min:{}\n".format(min_))
            #file.write("  Max:{}\n".format(max_))
            #file.write("  Avg:{}\n".format(avg_))
            file.close()
            with open('Output.txt', 'a') as f_handle:
                np.savetxt(f_handle,np.array(elite_genes[0].getGenom()),fmt='%4.3f')
            
            file = open("Output.txt","a")
            file.write("\n-----Original * Filter-----\n".format(count_))
            file.close()
            with open('Output.txt', 'a') as f_handle:
                np.savetxt(f_handle,np.dot(Original_data,np.array(elite_genes[0].getGenom())),fmt='%4.3f')
            """
            # 現行世代の進化結果を出力します
            print ("-----{}行目第{}世代の結果-----".format(Roop_Num,count_))
            #print ("  Min:{}".format(min_))
            print ("  Max:{}".format(max_))
            #print ("  Avg:{}".format(avg_))
            #print(elite_genes[0].getGenom())
            #input()
            file = open("Output.txt","a")
            file.write("{}\n".format(max_))
            file.close()

            
        if count_ % MAX_GENERATION != 0:
            # 現行世代と次世代を入れ替えます
            current_generation_individual_group = next_generation_individual_group
        
    #ANS[Roop_Num]=np.array(elite_genes[0].getGenom())
    return np.array(elite_genes[0].getGenom()),Roop_Num


if __name__ == "__main__":
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

    print("============Original==============")
    print(Original_data.shape)
    print("============Practice==============")
    print(Practice_data.shape)

    file = open("TestTexr.txt","w")
    file.write("\n-----Original_Data-----\n")
    file.close()

    with open('TestTexr.txt', 'a') as f_handle:
        np.savetxt(f_handle,Original_data,fmt='%4.3f')

    file = open("TestTexr.txt","a")
    file.write("\n-----Practice_Data-----\n")
    file.close()

    with open('TestTexr.txt', 'a') as f_handle:
        np.savetxt(f_handle,Practice_data,fmt='%4.3f')

    x = np.zeros(shape=(Original_y,Practice_y),dtype="float")
    ANS = np.empty((Practice_y,Original_y))
    ANS.flags.writeable = True


    # 遺伝子情報の長さ
    GENOM_LENGTH = Original_y
    # 遺伝子集団の大きさ
    MAX_GENOM_LIST = Original_y
    # 遺伝子選択数
    SELECT_GENOM = int(Original_y*0.3)
    
    #print(Genetic(0,ANS))
    #Tmp=Parallel(n_jobs=3)(delayed(Genetic)(i,ANS) for i in range(Practice_y))
    Tmp=Parallel(n_jobs=3)(delayed(Genetic)(i,ANS) for i in range(1))
    #for i in range(Practice_y):
        #ANS[Tmp[i][1]]=Tmp[i][0]
    print(Tmp)

    # 最終結果出力
    #Ans = (np.array(elite_genes[0].getGenom()).reshape([Original_y,Practice_y]))
    #print(ANS.T)
    file = open("TestTexr.txt","a")
    file.write("\n-----Filter-----\n")
    file.close()

    with open('TestTexr.txt', 'a') as f_handle:
        np.savetxt(f_handle,ANS.T,fmt='%4.3f')

    file = open("TestTexr.txt","a")
    file.write("\n-----Original*Filter-----\n")
    file.close()

    with open('TestTexr.txt', 'a') as f_handle:
        np.savetxt(f_handle,np.dot(Original_data,ANS.T),fmt='%4.3f')


    """np.set_printoptions(formatter={'float': '{:.4f}'.format})
    file = open("Output.txt","a")
    file.write ("--------------ANS--------------\n")
    file.write(ANS)
    file.write("\n------------Original * ANS------\n ")
    file.write(np.dot(Original_data,ANS))
    """
    pass