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
import statistics as stat
import copy
import wiggler3 as Fit
import normal as Norm



def getPredictions(data,weights):
    predictions = np.zeros(data.shape)
    if weights[0] != 0:
        predictions = predictions + rollA(data,int(len(data)/10)) * weights[0]
    if weights[1] != 0:
        predictions = predictions + Norm.getPredictions(data) * weights[1]
    if weights[2] != 0:
        predictions = predictions + Fit.main(data) * weights[2]
    return(predictions/sum(weights))
        
        



def KF(measurements,predictions):
    for i in range(data.shape[1]):
        dRow = data.T[i]
        rRow = rollData.T[i]
        fData = []
        for j in range(len(dRow)):
            x = rRow[j]
            p = .2                        ####################
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
