#coding:utf-8

import numpy as np
import wave
import matplotlib.pyplot as plt
from joblib import Parallel,delayed
from scipy.stats import norm 
import pathlib
import os
import re
from sklearn.cluster import KMeans
import shutil


if __name__ == "__main__":
    #曲の配列 拡張子なし
    Music_name=[]
    #曲の配列　拡張子有
    Music_Name_Path = []
    #練習曲のFurieの配列
    Furie_Array=[]
    #originalとpracticeのパスを取得する
    first_dir = os.getcwd()
    music_name_path = pathlib.Path('Dataset').glob('*')
    Result_Path =  list(((pathlib.Path('').resolve().glob('Result'))))
    
    print(Result_Path)
    for name1 in music_name_path:
        practice_number = pathlib.Path('Dataset/',name1.name).glob('*')
        for name2 in practice_number:
            Save_Path = 'Dataset/{}/{}/'.format(name1.name,name2.name)
            Original =  list(pathlib.Path('Dataset/{}/{}/'.format(name1.name,name2.name)).glob('original*[0-9]*wav'))
            #print(name2)
            if(len(Original) != 0 ):
                for A_Original in Original:
                    Music_Name_Path.append(A_Original.resolve())
                    Music_name.append( os.path.splitext(A_Original.resolve())[0])
                    os.chdir(Save_Path)
                    #print("Furie_Difference{}.txt".format(re.findall('_[0-9]',str(A_Original))[0]))
                    Furie_Array.append((np.loadtxt("Furie_Difference{}.txt".format(re.findall('_[0-9]',str(A_Original))[0]))))
                    os.chdir(first_dir)
    
    pred = KMeans(n_clusters=8, max_iter=1000).fit_predict(Furie_Array)
    
    """
    for i in range(len(Music_name)):
        if pred[i]%5 == 0:
            print(Music_name[i],"\t",pred[i])

    print(pred)
    """

    counter = 0
    for class_number in pred:
        print(class_number)
        Music_Path=os.path.dirname(Music_name[counter])
        print(Music_Path)
        print('{}\\{}'.format(Result_Path[0],class_number))
        print( os.path.split(os.path.split(Music_name[counter])[0])[1])
        print( os.path.split(os.path.split(os.path.split(Music_name[counter])[0])[0])[1])
        shutil.copytree(Music_Path, '{}\\{}\\{}\\{}'.format(Result_Path[0],class_number, os.path.split(os.path.split(os.path.split(Music_name[counter])[0])[0])[1],os.path.split(os.path.split(Music_name[counter])[0])[1]))
        
        #print(Save_Path.index("\\{}".format(str(class_number))))
        counter+= 1

    #class数を表示
    counter = np.zeros((max(pred)+1))
    for i in pred:
        counter[i]+=1
    print(counter)

    #print(Music_name)