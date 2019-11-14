import midi_scan
import numpy as np
#import pyomo.environ as pyo
import pulp
from pyomo.opt import SolverFactory
import random
from scipy.stats import norm 


#a=midi_scan.main()
#print(a)
#print("a")
#array = np.full((10,20),solver.NumVar(-solver.infinity(), solver.infinity(),'X')

l= [0,1,2,3,4,5]
def syaffulu(l):
    l.pop(0)
syaffulu(l)
print(l)
random_variable = norm.rvs(loc=0,scale=1/10,size=10)
print(random_variable)
#Orignal
Original_data = np.random.randint(0,10,(3,4))
Original_x = Original_data.shape[0]
Original_y = Original_data.shape[1]
print("Original_x:{},Original_y;{}".format(Original_x,Original_y))

#Practice
Practice_data = np.random.randint(0,10,(3,3))
Pracrice_x = Practice_data.shape[0]
Practice_y = Practice_data.shape[1]


print("============Original==============")
print(Original_data)
print("============Practice==============")
print(Practice_data)
#フィルター
x = np.zeros(shape=(Original_y,Practice_y),dtype="float")

I = [i for i in range(Practice_y)]

print("===========変数ｘ=================")
print(I)
