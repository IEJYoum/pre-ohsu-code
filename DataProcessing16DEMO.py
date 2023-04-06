# -*- coding: utf-8 -*-
"""
Created on Mon Jan 18 17:59:17 2021

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


def main():
    data = np.loadtxt("data\RetractCurve.txt")
    data = np.append([data[:,0]],np.append([data[:,4]],np.append([data[:,6]],np.append([data[:,1]],[data[:,2]],axis=0),axis=0),axis=0),axis=0).T
    rollData = rollA(data,20) #######################
    shape = data.shape
    KF(data,rollData)
        


def KF(data,rollData):
    for i in range(data.shape[1]):
        dRow = data.T[i]
        rRow = rollData.T[i]
        fData = []
        p = .2  
        for j in range(len(dRow)):
            x,p = predict(rRow[j],p)
            z = dRow[j]
            x,p = mUpdate(x,p,z)
            fData.append(x)
        print("\n\n\nFiltered data in orange")
        plt.plot(dRow)
        plt.plot(fData)
        plt.show()
        plt.plot(rRow)
        plt.plot(fData)
        plt.show()

def predict(x,p):
    nx = x
    np = p + .1 #############
    return(nx,np)

def mUpdate(x,p,meas):
    H = 1
    R = .5                             ####################
    K = p * H / (H*p*H + R)
    X = x + K*(meas - H * x)
    I = 1
    P = (I - K * H) * p
    return(X,P)
         
        
def rollA(array,steps):
    newA = []
    shape = array.shape
    if array.ndim == 2:
        if shape[0] > shape[1]: 
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
    
    
main()