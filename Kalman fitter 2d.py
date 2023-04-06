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
    positions = []
    for pos in data:
        positions.append(pos[0])
    t = np.arange(100)
    plt.plot(t,positions)
    plt.show()
    fData = []
    x = np.array([[0],[0]])
    p = np.array([[1,1],[1,1]])
    for meas in data:
        fData.append(x[0])
        x,p = predict(x,p)
        x,p = mUpdate(x,p,meas)
        print(x,"\n",p,"\n\n")   
    plt.plot(t,positions)
    plt.plot(t,fData)
    plt.show()
        
    
def mUpdate(x,p,meas):
    H = np.array([[1,1],[1,1]])
    R = np.array([[10,10],[2,10]])
    I = np.array([[1,0],[0,1]])
    K1 = np.matmul(p,H.T)
    K2 = np.matmul(np.matmul(H,p),H.T)+R
    K2 = np.linalg.pinv(K2)
    K = np.dot(K1,K2)
    X = x + np.matmul(K,(meas - np.matmul(H,x)))
    P = np.matmul((I - np.matmul(K,H)),p)
    return(X,P)
    


def predict(x,p):
    #print(x.shape)
    A = np.array([[1,.005],[0,1]])
    B = np.array([[.05],[.1]])
    Q = np.array([[.1],[.1]])
    X = np.matmul(A,x) + B
    P = np.matmul(np.matmul(A,p),A.T) + Q
    return(X,P)
    
      
    
def generateData():
    data = []
    pos = 0
    vel = 0
    for i in range(100):
        data.append(np.array([[pos,vel]]).T)
        vel += .1 + random.uniform(-.1,.1)
        pos = pos + vel * .01 / 2 + random.uniform(-.1,.1)
        #print(np.array([[pos,vel]]).T)
    print(data[0].shape)
    return(data)

    
main()