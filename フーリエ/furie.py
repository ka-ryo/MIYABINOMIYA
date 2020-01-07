#coding:utf-8

import numpy as np
import wave
import matplotlib.pyplot as plt
from joblib import Parallel,delayed
from scipy.stats import norm 
import pathlib
import os
import re

def wave_load(filename):
    # open wave file
    wf = wave.open(filename,'r')
    channels = wf.getnchannels()

    # load wave data
    chunk_size = wf.getnframes()
    amp  = (2**8) ** wf.getsampwidth() / 2
    data = wf.readframes(chunk_size)   # バイナリ読み込み
    data = np.frombuffer(data,'int16') # intに変換
    data = data / amp                  # 振幅正規化
    data = data[::channels]

    return data

def furie(Wave_Filename):
    print(Wave_Filename)
    fs = 8000.0
    d = 1.0 / fs
    size = 200000
    wave1 = wave_load(os.path.basename(Wave_Filename))
    wave2 = wave_load(os.path.basename(Wave_Filename).replace('original','practice'))

    big_size = wave1.shape[0] if wave1.shape[0] < wave2.shape[0] else wave2.shape[0]

    size = size if size < big_size else big_size

    dt1 = np.fft.fft(wave1[0:0+size:2000])
    dt2 = np.fft.fft(wave2[0:0+size:2000])
    print(size)
    dt3 = dt2 - dt1
    frq = np.fft.fftfreq(size,d)

    """
    plt.subplot(1,1,1)
    plt.title("FFT - recorder_A4")
    plt.plot(frq,abs(dt3))
    plt.axis([0,fs/2,0,max(abs(dt3))])
    """

    Amp = np.abs(dt3/(size/2)) # 振幅

    """
    fig, ax = plt.subplots()
    ax.plot(dt3[1:int(size/2)], Amp[1:int(size/2)])
    ax.set_xlabel("Freqency [Hz]")
    ax.set_ylabel("Amplitude")
    ax.grid()
    #plt.show()
    """

    if dt2.shape[0] != (int)(200000/2000):
        X_0 = np.zeros(((int)(200000/2000)-dt2.shape[0]))
        np.savetxt("Furie_Difference{}.txt".format(re.findall('_[0-9]',str(Wave_Filename))[0]),np.append(dt3,X_0))
    else:
        np.savetxt("Furie_Difference{}.txt".format(re.findall('_[0-9]',str(Wave_Filename))[0]),dt3)
    
    """
    if size != 200000:
        X_0 = np.zeros((200000-size))
        np.savetxt("Furie_Difference{}.txt".format(re.findall('_[0-9]',str(Wave_Filename))[0]),np.append(dt3,X_0))
    else:
        np.savetxt("Furie_Difference{}.txt".format(re.findall('_[0-9]',str(Wave_Filename))[0]),dt3)
    """
    #plt.show()
if __name__ == "__main__":
    #originalとpracticeのパスを取得する
    first_dir = os.getcwd()
    music_name_path = pathlib.Path('Dataset').glob('*')
    for name1 in music_name_path:
        practice_number = pathlib.Path('Dataset/',name1.name).glob('*')
        for name2 in practice_number:
            Save_Path = 'Dataset/{}/{}/'.format(name1.name,name2.name)
            Original =  list(pathlib.Path('Dataset/{}/{}/'.format(name1.name,name2.name)).glob('original*[0-9]*wav'))
            Practice =  list(pathlib.Path('Dataset/{}/{}/'.format(name1.name,name2.name)).glob('practice*[0-9]*wav'))
            Do_check =  list(pathlib.Path('Dataset/{}/{}/'.format(name1.name,name2.name)).glob('Furie*'))
            if(len(Original) != 0 and len(Practice)):
                for A_Original in Original:
                    Original_path=(os.path.dirname(A_Original))
                    os.chdir(Save_Path)
                    furie(A_Original)    
                    os.chdir(first_dir)
    