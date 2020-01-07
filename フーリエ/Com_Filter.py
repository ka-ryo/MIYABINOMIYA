import os
import pathlib
import numpy as np
import pandas as pd
import urllib.request 
import matplotlib.pyplot as plt
import sklearn #機械学習のライブラリ
from sklearn import decomposition 

def main(path):
    print(path)
    Filter_np = np.loadtxt(path,np.complex128)
    
    #Practice Number
    Practice_Number = path.parents[1].stem
    #print(Practice_Number)

    #Original music name
    Music_name = path.parents[2].stem
    #print(Music_name)

    Do_Check =list(pathlib.Path('./').glob('{}_{}*'.format(Music_name,Practice_Number)))

    if len(Do_Check) == 0:
        model = decomposition.PCA(n_components=2)
        model.fit(Filter_np)
        Compression_Filter = model.transform(Filter_np)

        Filter_Dim2 = np.sum(Compression_Filter,axis=0)
        Filter_Dim2  = Filter_Dim2 /Compression_Filter.shape[0]

        np.savetxt("./{}_{}.txt".format(Music_name,Practice_Number),Filter_Dim2)
        input()

    
if __name__ == "__main__":
    #originalとpracticeのパスを取得する
    first_dir = os.getcwd()
    music_name_path = pathlib.Path('Dataset').glob('*')
    for name1 in music_name_path:
        practice_number = pathlib.Path('Dataset/',name1.name).glob('*')
        for name2 in practice_number:
            Save_Path = 'Dataset/{}/{}/'.format(name1.name,name2.name)
            Furie_Array =  list(pathlib.Path('Dataset/{}/{}/'.format(name1.name,name2.name)).glob('Furie*'))
            if(len(Furie_Array) != 0 ):
                for A_Furie in Furie_Array:
                    Original_path=(os.path.dirname(A_Furie))
                    #os.chdir(Save_Path)
                    #main(A_Furie)    
                    #os.chdir(first_dir)

