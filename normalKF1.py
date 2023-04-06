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
import statistics as stat
import copy



def main():   
    rawData = np.loadtxt("data\RetractCurve.txt")
    rawData = np.append(rawData,np.array([np.ones(rawData.shape[0])]).T,axis = 1)
    shape = rawData.shape   
    means = getMeans(rawData)
    X = scaleData(rawData,means)
    Y = rollA(X,10)
    ansIndex = 2
    Z = Y[:,ansIndex]
    A = normalEqn(X,Z)
    #plt.plot(X[:,ansIndex])
    plt.plot(Y[:,ansIndex])
    transdata = np.matmul(A,X.T)
    transdata = np.array(transdata)
    plt.plot(transdata)
    plt.show()
    
    
    fdata = KalmanFilter(X,A)
    for i in range(shape[1]):
        plt.plot(X[:,i])
        plt.plot(Y[:,i])
        plt.plot(fdata[:,i])
        plt.show()
    
    
        
def KalmanFilter(X,A):
    shape = X.shape
    x = X[0,:]
    p = np.ones((A.shape[0],A.shape[0]))
    outdata = []
    print("\n\n\n initial \nX:",x,"\nP:",p)
    for i in range(2):        
        measurement = X[i,:]
        x,p = predict(x,p,A,1)
        print("\n\n\n out of predict \nX:",x,"\nP:",p)
        x,p = mUpdate(x,p,measurement,1)
        print("\n out of mupdate \nX:",x,"\nP:",p)
        outdata.append(x)
    return(np.array(outdata))
        
        
def mUpdate(x,p,z,noise):
    H = np.identity(p.shape[0])
    R = np.ones(p.shape) * noise
    I = np.identity(p.shape[0])
    K1 = np.matmul(p,H.T)
    K2 = np.matmul(np.matmul(H,p),H.T)+R
    K2 = np.linalg.pinv(K2)
    K = np.matmul(K1,K2)
    newX = x + np.matmul(K,(z - np.matmul(H,x)))
    newP = np.matmul((I - np.matmul(K,H)),p)    
    return(newX,newP)

def predict(x,p,A,noise):
    Q = np.ones(p.shape) * noise
    newx = np.matmul(A,x)
    newp = np.matmul(np.matmul(A,p),A.T) + Q
    return(newx,newp)




def normalEqn(X,Y):
    try:
        X2i = np.linalg.inv(np.matmul(X.T,X))
    except:
        print("pseudoinverse")
        X2i = np.linalg.pinv(np.matmul(X.T,X))
    A = np.matmul(np.matmul(X2i,X.T),Y)
    return(A)



def rollA(array,steps):
    newA = []
    shape = array.shape
    if array.ndim == 2:
        if shape[0] > shape[1]: #data goes down collumn
            array = array.T
            for row in array:
                newA.append(rollRow(row,steps))
            return(np.array(newA).T)
        else:
            for row in array:
                newA.append(rollRow(row,steps))
            return(np.array(newA))
            
            
def rollRow(dataL,steps):
    newL = []
    LdL = len(dataL)
    cursor = 0
    while cursor < LdL:
        near = []
        for j in range(cursor-steps,cursor+steps):
            if j >=0 and j < LdL:
                near.append(dataL[j])
            else:
                near.append(dataL[cursor])

        newL.append(stat.mean(near))
        cursor += 1
    return(newL)



def scaleData(data,means):
    shape = data.shape
    newData = []
    for col in range(shape[1]):
        newCol = data[:,col]/means[col]
        newData.append(newCol)
    return(np.array(newData).T)



def getMeans(data):
    means = []
    shape = data.shape
    for col in range(shape[1]):
        m = sum(data[:,col])/shape[0]
        means.append(m)
    return(means)


    
main()