# -*- coding: utf-8 -*-
"""
Created on Thu Aug  6 02:20:33 2020

@author: Jalaa
"""

import random
import numpy as np
import time
import matplotlib.pyplot as plt 
import math
import statistics as stat
import linReg as lr

#actionList = [thinkerT,gWeights,FWeights,axis,TPSweep]

FtYPES = 5

#TRAINf = "2018BMY_data.csv"
#TRAINf = "aTRuner9 functions indep pd 400 NP.csv"
#TRAINf = "generatedDataNp.csv"
TRAINf = "2016 2017ABC_data.csv"
#TRAINf = "2018ABC_data.csv"
#TRAINf = "xorNP.csv"
#TRAINf = "parsedirisDataCopy.csv"

trainingArray = np.loadtxt(TRAINf)

#maxTime = 2

#initialCl = [[0],[1],[1],[1],[2,[0,[0,1],[1,1],[0]]],[99,99]]  #last index is maxTime
#[2 axisW = points/daysBack, axes, coeffs, axesFunctionList]
#initialCl = [[0],[2,[0,[0,1],[1,1],[0]]],[3,1,[10,10,-1,2,-2,2],[3,0,0, 1,0,0],[0]],[99,99]] 
#initialCl = [[0],[1],[2,[0,[0,1],[1,1],[0]]],[3,10,[10,10,-1,2,-2,2],[1]],[99,99]] 
#[3, function run+evaltime,generatingW,scoreFunctionL]
initialCl = [[2,[0,[0,1],[1,1],[0]]],  [3,1,[10,50,-1,2,-2,2],[1]],  [2.1],  [3,10,[10,50,-1,2,-2,2],[1]],  [4],  [99,99]] 


# 3 gWeights = [10,10,-1,2,-2,2]
# 3 FWeights = [3,0,0, 1,0,0]


XS = []
ANSWERS = []
AXISw = [] #these are static: one set of axis weights for all Fs in run
BFS = []
FaCCS = []


def main(trainingArray,initialCL):  #feed test data in with training while testing (for context)
    maxT = initialCL[-1][-1]
    commandLists = initialCL
    halfRows = round(trainingArray.shape[0]/2)
    array0 = trainingArray[:halfRows,]
    array1 = trainingArray[halfRows:,]
    updateAnswers(array0)
    
    startTime = time.time()
    i = 0 
    while i < len(commandLists):
        if time.time() < startTime + maxT and commandLists[i][0] != 99:
            returnsL = runCommands(array0,array1,commandLists[i])
            #print("returnsL:",returnsL)
            if len(returnsL) != 0:
                updateGlob(returnsL)        
        i += 1
        
    #plt.scatter(XS,ANSWERS)
    #plt.show()

def updateAnswers(array):
    ANSWERS.clear()
    for point in array:
        ANSWERS.append(point[-1])


def runCommands(array0,array1,commandL):
    global AXISw
    '''
    if commandL[0] == 0:     #FIND EXTREMES
        extremes = findExtremes(array)
        return(array,[0,extremes])
    elif commandL[0] == 1:    #SCALE ARRAY BY EXTREMES
        array = scaleByExtr(array)   #array changed here
        return(array,[])
    '''
    if commandL[0] == 2:    #COMPOUND AXES
        AXISw = commandL[1]
        compXs = genAxis(array0,AXISw)
        return([2,compXs])
    elif commandL[0] == 2.1:
        compXs = genAxis(array0,AXISw)
        return([2,compXs])        
        
    elif commandL[0] == 3:  #RUN and score FUNCTION FOR TIME, update global BESTf
        maxTime = commandL[1]
        genW = commandL[2]
        scoreF = commandL[3]
        xs = XS
        ys = ANSWERS
        Bscore = -99
        startTime = time.time()                
        while inTime(maxTime,startTime):
            function = genF(xs,genW)
            nxs = runF(xs,function)
            score = Score(nxs,ys,scoreF)
            if score > Bscore:
                Bscore = score
                #Bnxs = nxs
                Bfunction = function
                print(score)
        showF(Bfunction,[min(xs),max(xs)])        
        return([3,Bfunction])
    
    elif commandL[0] == 4: #check accuracy of each function in BFS on array 1
        accuracies = []
        for function in BFS:
            testCXs = genAxis(array1,AXISw) #updates ANSWERS
            tXs = []
            for x in testCXs:
                nx = runF([x],function)[0]
                tXs.append(nx)
            
            meanXS = stat.mean(XS)
            meanA = stat.mean(ANSWERS)
            correct = 0
            i = 0
            ltXs = len(tXs)
            while i < ltXs:
                nx = tXs[i]
                answer = ANSWERS[i]
                if nx > meanXS and answer > meanA:
                    correct += 1
                elif nx <= meanXS and answer <= meanA:
                    correct += 1
                i += 1
            
            accuracies.append(correct/ltXs)
            print("function:", function,"\n accuracy:",correct/ltXs,"\n Data after transformation:")            
            plt.scatter(tXs,ANSWERS)
            plt.show()            
        return([4,accuracies])
            

    
    return([])

        
def Score(xs,ys,scoreF):
    if scoreF[0] == 0:
        plt.scatter(xs,ys)
        plt.show()
        return(-99)
    elif scoreF[0] == 1:
        array = np.array([xs,ys])
        extremes = findExtremes(array)
        scArray = scaleByExtr(array,extremes)
        covMat = np.cov(scArray)
        covariance = covMat[1,0]
        return(covariance)


def updateGlob(returns):
    global XS
    #global EXTREMES
    global BFS
    global FaCCS
    #if returns[0] == 0:
        #EXTREMES = returns[1]
    
    if returns[0] == 2:
        XS = returns[1]
        
    elif returns[0] == 3:        
        BF = returns[1]
        XS = runF(XS,BF)
        BFS.append(BF)
    elif returns[0] == 4:
        FaCCS = returns[1]
        print(FaCCS)
        

    
    


'''
'''

def runF(xs,function):
    lX = len(xs)
    nxs = []
    i = 0
    while i < lX:
        x = xs[i]
        newX = 0    
        for f in function:
            if f[0] == 0:
                newX += math.cos(x/f[1]) * f[2]
            elif f[0] == 1:
                newX += math.sin(x/f[1]) * f[2] 
            elif f[0] == 2:
                newX += x * f[2]                
            elif f[0] == 3:
                newX += math.atan(x/f[1]) * f[2]
            elif f[0] == 4:
                newX += x ** f[1] * f[2]
        #print("x:",x,"newX:",newX)
        #time.sleep(1)
        nxs.append(newX)
        i += 1 
    return(nxs)

    


def genF(xs,gWeights):
    maxL = gWeights[0]
    endChance = gWeights[1]
    m = gWeights[2]
    M = gWeights[3]
    c = gWeights[4]
    C = gWeights[5]
    function = []
    while len(function) < maxL:
        if len(function) > 0:
            if random.randint(0,endChance) == 1:
                break
            
        f = [random.randint(0,FtYPES-1),10**random.uniform(m,M),random.uniform(c,C)]    
        function.append(f)    
    return(function)


def genAxis(array,aWeights):   #updates ANSWERS
    pointsBack = aWeights[0]
    axesL = aWeights[1]
    coeffs = aWeights[2]
    aFL = aWeights[3]
    compXs = []

    i = 0
    lArray = len(array)
    backArray = []    
    while i < lArray:
        newPoint = []
        j = 0
        skip = 0
        while j <= pointsBack:
            if i - j < 0:
                skip = 1
                break
            point = array[i - j]
            k = 0
            lPoint = len(point)
            while k < lPoint - 1:
                if k >= len(newPoint):
                    newPoint.append(point[k])
                else:
                    newPoint[k] += point[k]                                                
                k += 1
            newPoint.append(point[-1])
            j += 1
        if skip == 0:
            backArray.append(newPoint)
        i += 1
    #print("original array:",array,"\n\n\n\n\n backArray:",backArray)
    lArray = len(backArray)
    i = 0
    while i < lArray:
        datapoint = backArray[i]
        iVars = []
        j = 0
        lAxesL = len(axesL)
        while j < lAxesL:
            axis = axesL[j]
            coeff = coeffs[j]
            iVars.append(datapoint[axis]*coeff)
            j += 1                
        for f in aFL:
            if f == 0:
                compXs.append(sum(iVars))        
        i += 1  
    updateAnswers(backArray)
    #compXs = scaleLBySelf(compXs)
    print("compXs vs ansers:")
    plt.scatter(compXs,ANSWERS)
    plt.show()
    #time.sleep(10)
    return(compXs)
    






def findExtremes(array):
    extremes = []
    maxs = np.amax(array,axis = 0)
    mins = np.amin(array,axis = 0)
    i = 0
    lMaxs = len(maxs)
    while i < lMaxs:
        mx = maxs[i]
        mn = mins[i]
        extremes.append(max([mx**2,mn**2])**.5)
        i += 1    
    return(extremes)
    
    
def scaleByExtr(array,extremes):
    nAxes = len(array[0])
    i = 0
    newArray = []
    while i < nAxes:
        newAxis = []
        ext = extremes[i]
        for var in array[:,i]:
            newAxis.append(var/ext)
            
        newArray.append(newAxis)
        i += 1    
    return(np.transpose(newArray))

def scaleLBySelf(lis):
    extreme = max([max(lis)**2,min(lis)**2])**.5
    #print(lis)
    for i in range (len(lis)):
        lis[i] = lis[i]/extreme
    #print(lis,"\n\n")
    return(lis)


def showF(bestF,rangeL):
    xs = []
    i = rangeL[0]
    rng = rangeL[1] - rangeL[0]
    while i <= rangeL[1]:
        xs.append(i)
        i += .01 * rng
    nxs = runF(xs,bestF)
    print("BEST FUNCTION\n",bestF)
    plt.scatter(xs,nxs)
    plt.show()    


def inTime(maxTime,startTime):
    if time.time() < startTime + maxTime:
        return(True)
    else:
        return(False)    

main(trainingArray,initialCl)    
    