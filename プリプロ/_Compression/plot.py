import os
import pathlib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

txtpath= list(pathlib.Path('./').glob('*.txt'))


zahyou=[]

for i in txtpath:
    print(i)
    print(np.loadtxt(i))
    zahyou.append(np.loadtxt(i))



for i in range(len(txtpath)):
    plt.plot(zahyou[i][0],zahyou[i][1],'ro')
plt.show()

