import cupy as cp
import numpy as np

def Evaluation(Original,X,row_num):
    X_gpu = cp.asarray(X)
    Original_gpu = cp.asarray(Original)
    #Practice_gpu = cp.asarray(Practice)

    Dot_gpu = cp.dot(Original_gpu,X_gpu)
    #Dot_gpu = Dot_gpu.T-Practice_gpu.T[row_num]
    #Dot_gpu = cp.abs(Dot_gpu)

    Dot_cpu2 = Dot_gpu.get()
    

    #return -1*cp.sum(Dot_cpu2)

if __name__ == "__main__":
    X1 = np.random.rand(1,4)
    X2 = np.random.rand(4,1)
    X3 = np.random.rand(1,3)

    Evaluation(X1,X2,0)
