# -*- coding: utf-8 -*-
"""
Created on Sat Jan 23 19:58:23 2021

@author: Jalaa
"""

import math
import matplotlib.pyplot as plt
import random
import pandas as pd
import numpy as np
import time
import math
import DataObjects4 as obj
import statistics as stat
import copy


rawData = np.loadtxt("data\RetractCurve.txt")
def main():   
    shape = rawData.shape   
    lrate = .001
    means = getMeans(rawData)
    data = scaleData(rawData,means)
    Y = np.append([data[:,1]],[data[:,2]],axis = 0).T
    X = np.append([data[:,0]],data[:,3:].T,axis = 0)
    X = np.append(X,[np.ones(shape[0])],axis = 0).T
    A = np.ones((Y.shape[1],X.shape[1]))
    print(Y.shape,X.shape)
    for i in range(1000):
        delta,outData = getDelta(A,X,Y)
        A = np.add(A,lrate*delta)
        #print(A,"\n\n\n")
    plt.plot(Y[:,1])
    #print(outData)
    plt.plot(outData[:,1])
    plt.show()
    print("A:\n",A)
        


def getDelta(A,X,Y):
    shape = A.shape #Ycols, Xcols
    m = X.shape[0]
    delta = np.zeros(shape)  
    outData = np.zeros(Y.shape)
    for i in range(m):
        guess = np.zeros(shape[0])
        guess = np.matmul(A,X[i])
        outData[i] = guess
        for j in range(shape[0]):
            for k in range(shape[1]):
                delta[j,k] += (Y[i,j] - guess[j])*X[i,k]

    return(delta,outData)         
            



def scaleData(data,means):
    shape = data.shape
    newData = []
    for col in range(shape[1]):
        newCol = data[:,col]/means[col]
        newData.append(newCol)
    print(np.array(newData))
    return(np.array(newData).T)



def getMeans(data):
    means = []
    shape = data.shape
    for col in range(shape[1]):
        m = sum(data[:,col])/shape[0]
        means.append(m)
    return(means)
        
        
  
    
    return()
    
main()