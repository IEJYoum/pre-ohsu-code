# -*- coding: utf-8 -*-
"""
Created on Mon Aug  3 03:14:50 2020

@author: Jalaa
"""

import aThinker7 as thinker #athinker5 should also work
import numpy as np
import matplotlib.pyplot as plt 
import statistics as stat
import time
import random

#INfILE = "generatedDataLongNp.csv"
#INfILE = "kaggleSnp/testing/2018ABT_data.csv"

#TRAINf = "COTYnp.csv"
#TESTf = "COTYnp.csv"



TRAINf = "2016 2017BMY_data.csv"
#TESTf = "2018BMY_data.csv"
TESTf =  "2BMY 1 line.csv"


#TRAINf = "generatedDataNp.csv"
#TESTf = "generatedDataNp.csv"


sweeps = 3


def main(trainf,testf): #first get better pints and data representation coming out
    trainingA = np.loadtxt(trainf)

    if len(trainingA.shape) == 1:
        print("error, cannot train on single datapoint")
        time.sleep(10)
    
    nInd = len(trainingA[0,]) - 1
    sweepDA = []
    sweep = 0
    while sweep < sweeps: 
        #actionL = [1,[20,5,-2,1],[3,0,0,10**10,1,100],axis]
        actionL = genActionL(nInd)
        bestFs,exX,exY,means,scores = runAxes(trainf,actionL)                        
        fraCorrect = tally(guess(testf,actionL[3],bestFs,exX,exY,means))
        performanceData = makePerformanceData(actionL,(fraCorrect - .5)*2)
        sweepDA.append(performanceData)
        print("sweep number",sweep)
        sweep += 1
    
    print(sweepDA)
    performanceA = np.array(sweepDA)    
    np.savetxt("aTRuner7 performance data NP 2.csv",performanceA)
    
    scatterMultiple(performanceA)
    #scatterMultiple1("aTRuner7 performance data NP 1.csv")
    

def scatterMultiple(array):
    i = 0
    print(array.shape)
    time.sleep(10)
    while i < array.shape[1] - 1:
        j = 0
        xs = []
        ys = []
        while j < array.shape[0]:
            xs.append(array[j,i])
            ys.append(array[j,-1])
            j += 1
        print(i,"th attribute vs performance")
        plt.scatter(xs,ys)
        plt.show()
        i += 1

def scatterMultiple1(filePath):
    array = np.loadtxt(filePath)
    i = 0
    while i < array.shape[1] - 1:
        j = 0
        xs = []
        ys = []
        while j < array.shape[0]:
            xs.append(array[j,i])
            ys.append(array[j,-1])
            j += 1
        print(i,"th attribute vs performance")
        plt.scatter(xs,ys)
        plt.show()
        i += 1




            

def makePerformanceData(actionL,performance):
    datapoint = []
    datapoint.append(actionL[0]) #time per each function generation
    
    datapoint.append(actionL[1][0])
    datapoint.append(actionL[1][1])
    datapoint.append(actionL[1][2])
    datapoint.append(actionL[1][3]) #function generating weights
    datapoint.append(actionL[1][4])
    datapoint.append(actionL[1][5])
    
    datapoint.append(actionL[2][0])
    datapoint.append(actionL[2][1])
    datapoint.append(actionL[2][2])
    datapoint.append(actionL[2][3])
    datapoint.append(actionL[2][4])
    datapoint.append(actionL[2][5]) #function scoring weights
    
    datapoint.append(actionL[3]) #axis
    datapoint.append(actionL[4]) #time per sweep
    datapoint.append(performance)    
    return(datapoint)

def genActionL(nInd):
    thinkerT = 10**random.uniform(-1,1)
    
    
    maxFLength = random.randint(1,20)
    earlyEndChance = random.randint(1,100)
    m = random.uniform(-2,0)
    M = random.uniform(0,2)
    c = random.uniform(-1,0)
    C = random.uniform(0,1)

    gWeights = [maxFLength,earlyEndChance,m,M,c,C]      #f = [random.randint(0,FtYPES-1),10**random.uniform(m,M),random.uniform(c,C)] c picks bound of possible coefficients    
                                                        #function.append(f)
    
    covWeight = random.randint(0,4)
    xSDWeight = random.randint(-2,0)
    ySDWeight = random.randint(-2,0)
    covOverallW = 10**random.uniform(0,10)
    linOverallW = 10**random.uniform(-5,0)
    pstdevOverallW = 10**random.uniform(-2,2)
    FWeights = [covWeight,xSDWeight,ySDWeight,covOverallW,linOverallW,pstdevOverallW]
    
    axis = random.randint(0,nInd - 1)
    
    TPSweep = random.randint(1,7)
    
    actionList = [thinkerT,gWeights,FWeights,axis,TPSweep]
    
    return(actionList)
    


def runAxes(trainf,actionL):
    if type(actionL[3]) == int: 
        return(runSingleAxis(trainf,actionL))

        

def runSingleAxis(trainf,actionL):
    trainingA = np.loadtxt(trainf)
    thinkerTime = actionL[0]
    gWeights = actionL[1]
    FWeights = actionL[2]
    xI = actionL[3]
    TPSweep = actionL[4]
    bestFs = []
    means = []
    scores = []
    startTime = time.time()
    while time.time() < startTime + TPSweep:                
        F,score,xs,ys,exX,exY,meanX = thinker.main(trainingA,gWeights,FWeights,thinkerTime,xI)
        bestFs.append(F)
        means.append(meanX)
        scores.append(score)
    
    return(bestFs,exX,exY,means,scores) 
    



def scatter2D(data):    
    xs = []
    ys = []
    for i in data:
        xs.append(i[0])
        ys.append(i[1])
    plt.scatter(xs,ys)
    
def tally(votes): 
    #print("tallying")
    correct = 0
    for vote in votes:
        #print(vote,"vote")
        guess = vote[0]
        point = vote[1]
        if guess == 1:
            if point[-1] > 0:
                correct += 1
        elif guess == 0:
            if point[-1] <= 0:
                correct += 1
    print("Fraction correct:", correct/len(votes))
    
    return(correct/len(votes))
            
        


def guess(testf,xI,bestFs,exX,exY,means): #(guess(testf,actionL[-1],bestFs,exX,exY,means))
    print("guessing")    
    testA = np.loadtxt(testf)
    if len(testA.shape) == 1:
        print("guessing on single datapoint")
        time.sleep(1)
        testA = np.array([testA,np.zeros(testA.shape)])
        print(testA)
    if xI == -1 or xI == len(testA[0,]) - 1:
        print("error,accessing answer")
        time.sleep(10)
        return(0)
    votes = []
    for point in testA:
        x = point[xI]/exX
        i = 0
        lBestFs = len(bestFs)
        
        vote = 0
        while i < lBestFs:
            function = bestFs[i]
            mean = means[i]            
            newX = thinker.runF1(x,function)
            i += 1
            if newX > mean:
                vote += 1
            else:
                vote -= 1               
                
        if vote > 0:
            votes.append([1,point])
        else:
            votes.append([0,point])

    return(votes)

        

    

def scoreDistribution(distribution,weights):
    
    xs = []
    ys = []
    for i in distribution:
        xs.append(i[0])
        ys.append(i[1])
    
    score = len(distribution)**weights[0] * stat.mean(ys)**weights[1] * (stat.stdev(ys))**weights[2]
    return(score)


    



main(TRAINf,TESTf)