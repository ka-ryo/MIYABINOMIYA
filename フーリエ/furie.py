 # testwavemodule3.py
 # encoding: utf-8
 # http://nalab.mind.meiji.ac.jp/~mk/lecture/fourier-2017/testwavemodule3.py
# これは Python 3.x 用のプログラム
    
import wave
import numpy as np
import matplotlib.pyplot as plt
from joblib import Parallel,delayed
from scipy.stats import norm 
import pathlib
import os
import re


def furie(Wave_Filename):
    #ここの名前を変更
 
    wfile = wave.open( (Wave_Filename), 'r')


    numch = wfile.getnchannels()
    samplewidth = wfile.getsampwidth()
    samplerate = wfile.getframerate()
    numsamples = wfile.getnframes()

    """
    print("チャンネル数 = ", numch)
    print("サンプル幅 (バイト数) = ", samplewidth)
    print("サンプリングレート(Hz) =", samplerate)
    print("サンプル数 =", numsamples)
    print("録音時間 =", numsamples / samplerate)
    """
    # すべてのフレームを読み込む (bytesオブジェクトになる)
    buf = wfile.readframes(numsamples)
    wfile.close()

    # numpy の ndarray に変換する
    if samplewidth == 2:
        data = np.frombuffer(buf, dtype='int16')
        data = data / 32768.0
    elif samplewidth == 4:
        data = np.frombuffer(buf, dtype='int32')
        data = data / 2147483648.0

    # ステレオの場合は左チャンネルだけを取り出す
    # (0 から最後まで2つおきに、つまり 0,2,4,.. 番目を取り出す)
    if numch == 2:
        #l_channel = data[0::2]
        #r_channel = data[1::2]
        data = data[0::2]


    start = 0
    N = numsamples
    c = np.fft.fft(data[start:start+N:500])
    c = abs(c)
    N=c.shape[0]
    #np.savetxt("a.txt",c)
    """
    plt.title(Wave_Filename)
    freqList = np.fft.fftfreq(N, d=1.0/samplerate)
    plt.plot(freqList, c, linestyle='-')
    plt.show()
    """
    return c



if __name__ == "__main__":
    #生成する差分の最大
    N_SABUN = 500
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
            if(len(Original) != 0 and len(Practice)!= 0):
                for A_Original in Original:
                    Original_path=(os.path.dirname(A_Original))
                    os.chdir(Save_Path)
                    
                    Ori=furie(os.path.basename(A_Original))
                    Pra=furie(os.path.basename(A_Original).replace('original','practice'))

                    if Ori.shape[0] > Pra.shape[0]:
                        Zero_array = np.zeros((Ori.shape[0] - Pra.shape[0]))
                        Pra=np.append(Pra,Zero_array)
                    elif Ori.shape[0] < Pra.shape[0]:
                        Zero_array = np.zeros((Pra.shape[0] - Ori.shape[0]))
                        Ori=np.append(Ori,Zero_array)
                    
                    Sabun = Ori - Pra
                    #freqList = np.fft.fftfreq(N, d=1.0/samplerate)
                    if Sabun.shape[0] >N_SABUN:
                        Sabun =np.resize(Sabun,N_SABUN)
                    elif Sabun.shape[0] < N_SABUN:
                        Zero_array = np.zeros(N_SABUN - Sabun.shape[0])
                        Sabun = np.append(Sabun,Zero_array)
                    np.savetxt("Furie_Difference{}.txt".format(re.findall('_[0-9]',str(os.path.basename(A_Original)))[0]),Sabun)
                    
                    """
                    plt.title('sabun')
                    plt.plot(Sabun, linestyle='-')
                    plt.show()
                    """
                    os.chdir(first_dir)
   



