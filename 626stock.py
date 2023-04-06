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
import seaborn as sns
import scipy
#from tiingo import Market
#import parseTiingo1 as parse

COLS = ["open","high","low","close", "volume","range","net","nnet"]

TRAINf ="M20 jul jun.csv"
TESTf ="M20 jun sep.csv"
DATA = np.loadtxt("data/"+TRAINf)
testDATA = np.loadtxt("data/"+TESTf)

#market = Market('GME')
#DATA = parse.main(market.getPrices('2021-1-1','2021-6-8'))

#DATA = np.array([[0,0],[1,0],[0,10],[1,1]])

SHAPE = DATA.shape
startTime = time.time()

def main():
    #bollbands()
    data = zScoreA(DATA)
    da = distA(data)
    df = pd.DataFrame(data=data,columns=COLS)
    while menu(df.copy(),np.copy(da)):
        pass

 
    
def menu(df,da):
    options = ["exit","start over with raw data","heatmap","crop dataset","bollinger bands","display gaussian"]
    while True:
        for i,op in enumerate(options):
            print(i,op)
        ch=int(input("Which number?"))
        if ch == 0:
            return(False)
        if ch == 1:
            return(True)
        if ch == 2:
            sns.heatmap(df)
            plt.show()
            sns.heatmap(da)
            plt.show()
        if ch == 3:
            print(df,type(df))
            df,da = crop(df,da)
        if ch == 4:
            bollbands(df.values)
        if ch == 5:
            gaussians(df)
        if ch == 6:
            df.values = zScoreA(df.values)
        if ch==7:
            boxPlot(df)


def boxPlot(df):
    for i,op in enumerate(df.columns):
        print(i,op)
    ch = int(input("number:"))
    

def gaussians(df):
    for i,op in enumerate(df.columns):
        print(i,op)
    ch = int(input("which number"))
    col = list(df[df.columns[ch]])
    ws = int(input("window size:"))
    for i in range(df.shape[0]):
        nears = []
        for j in range(-ws,ws):            
            if i+j>=0 and i+j<len(col):
                nears.append(col[i+j])
        mean = np.mean(nears)
        std = stat.stdev(nears)
        pseudogauss = []
        for i in range(50000):
            pseudogauss.append(np.random.normal(loc=mean, scale=std))
        plt.hist(pseudogauss,bins=50)
        plt.show()
            #'''
            #thi=scipy.stats.norm.rvs(loc=mean, scale=std, size=1000)
            #plt.hist(thi)
                
            
        
    


def crop(df,da):
    options = ["done cropping","dates","stock information"]
    while True:
        for i,op in enumerate(options):
            print(i,op)
        ch = int(input("Which number?"))
        if ch == 0:
            return(df,da)
        if ch == 1:
            for i,val in enumerate(df.index):
                print(i,val)
            start = int(input("start number"))
            end = int(input("end number"))
            df = df.iloc[start:end,:]
            da = da[start:end,start:end]
        if ch == 2:
            for i,val in enumerate(df.columns):
                print(i,val)
            ch = int(input("remove which number?"))  
            df = df.drop(df.columns[ch],axis=1)        
            
            
        
    

    
    
def distA(data):
    dA = np.ones((SHAPE[0],SHAPE[0])) * 9
    for i in range(SHAPE[0]):
        point = data[i,:]
        for j in range(SHAPE[0]):
            if j < i:
                other = data[j,:]
                dA[i,j] = euclidian(point,other)
                dA[j,i] = dA[i,j]
    return(dA)
            
    
def euclidian(v,l):
    val= np.sum(np.square(v-l))  
    return(val)

def zScoreA(a):#zscores vertically (so each column is distributed around 0)
    shape=a.shape
    newA = np.zeros(shape)
    for i in range(shape[1]):
        col = a[:,i]
        mean = np.mean(col)
        std = np.std(col)
        if std == 0:
            std = 1
        col = (col-mean)/std
        newA[:,i] = col
    return(newA)
    
def bollbands():    
    for i in range(SHAPE[1]):
        if i == 3:
            row = DATA[:,i]
            rRow,sds = roll(row,10)
            grads(rRow)
            upper,lower = boll(rRow,sds)
            plt.plot(row)
            plt.plot(upper)
            plt.plot(lower)           
            plt.show()  

def grads(row):
    nextRow = np.append(row[1:],[0])
    prevRow = np.append([0],row[:-1])
    gradRow = np.subtract(nextRow,prevRow)
    mean = stat.mean(gradRow[1:-1])
    gradRow[0] = mean
    gradRow[-1] = mean
    plt.plot(gradRow)
    plt.show()
    return(gradRow)

def boll(rRow,sds):
    upper = []
    lower = []
    for i in range(len(rRow)):
        upper.append(rRow[i] + sds[i])
        lower.append(rRow[i] - sds[i])

    return(upper,lower)

def roll(row,rang):
    rRow = []
    sds = []
    for i in range(len(row)):
        nears = [row[i]]
        
        for j in range(rang):
            if i-j > 0:
                nears.append(row[i-j])
                
        #weights = (np.arange(len(nears))+1)
        nears = np.array(nears) #/weights
        #print("weights",weights,"nears",nears)
        
        try:
            sds.append(stat.stdev(nears))
            rRow.append(stat.mean(nears))            
        except:
            rRow.append(row[i])
            sds.append(0)
    return(rRow,sds)
        
        
        
    
main()