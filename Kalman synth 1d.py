# -*- coding: utf-8 -*-
"""
Created on Sun Dec  6 18:10:10 2020

@author: Jalaa
"""

import random
import numpy as np
import time
import matplotlib.pyplot as plt 
import math
import statistics as stat
import copy

def main():
    data = generateData()
    t = np.arange(100)
    plt.plot(t,data)
    #plt.show()
    fData = []
    x = data[0]
    p = 1
    for meas in data:
        x,p = predict(x,p)
        x,p = mUpdate(x,p,meas)
        fData.append(x)
    print(x,"\n",p,"\n\n")
    plt.plot(t,fData)
    plt.show()
        
    
def mUpdate(x,p,meas):
    H = .9
    R = .2
    K = p * H / (H*p*H + R)
    X = x + K*(meas - H * x)
    I = 1
    P = (I - K * H) * p
    print("P out of measurement update",P)
    return(X,P)
    


def predict(x,p):
    A = 1
    B = 1
    Q = .1
    X = A * x + B
    P = A**2 * p + Q
    print("P out of predict",P)
    return(X,P)
    
    
    

    
    
    
def generateData():
    data = []
    shift = random.uniform(.5,2)
    for i in range(100):
        data.append(100+i**2/100+random.uniform(0,i**2/100) + shift * i)
    return(data)

    
main()