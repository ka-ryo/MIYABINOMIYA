import os
import pathlib
import numpy as np
import pandas as pd
import urllib.request 
import matplotlib.pyplot as plt
import sklearn #機械学習のライブラリ
from sklearn import decomposition 
from sklearn.decomposition import PCA #主成分分析

def pdf_conv(path):
    print(path)
    Filter_np = np.loadtxt(path)
    
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

    


if __name__ == "__main__":
    music_folder_path = pathlib.Path('../').glob('[a-z]*')

    for i in music_folder_path:
        prctice_number_path= pathlib.Path('{}/'.format(i)).glob('*')
        for j in prctice_number_path:
            pdf_path = pathlib.Path('{}/500/'.format(j)).glob('Filter*')
            for k in pdf_path:
                pdf_conv(k)    