# -*- coding: utf-8 -*-
"""
Created on Wed Jul 22 03:58:19 2020

@author: Jalaa
"""

import parametric9 as parametric
import thinker18 as thinker
import parseKaggle as parse
import time
import numpy as np



INfILE = "agq stock prices small.txt"
#INfILE = "irisData.txt"
#INfILE = "xorData.txt"



#gotta manually update answers[] in testfunctions when using different file


a = "ding!"
    

def main(inFile,weights,maxTime):
    dataArray = parse.main(inFile)
    maxScore = 0
    bestCov = np.array([0])
    bestFunctions = []
    bestData = []

    startTime = time.time()
    while time.time() - startTime < maxTime:
        returns = thinker.main(dataArray,[0])
        data2D = returns[0] #array
        functions = returns[1]     
        covMatrix = np.cov(data2D,rowvar = False)
        score = findScore(covMatrix,weights) #takes 3 weights
        if score > maxScore:
            maxScore = score
            bestCov = covMatrix
            bestFunctions = functions
            bestData = (data2D)
    return(bestFunctions)
        


def findScore(covMatrix,weights):
    xVar = covMatrix[0,0]
    cov = covMatrix[1,0]        
    score = (cov ** weights[0] / (xVar + 1) ** weights[1]) ** weights[2] 
    return(score)
    
    



def makeNx2Array(transformedData):
    #print(transformedData)
    dataList = []
    for point in transformedData:
        newPoint = []
        bucket = point[:-1]
        bucket = bucket.tolist()
        newPoint.append(sum(bucket))
        newPoint.append(point[-1])
        dataList.append(newPoint)
    return(np.array(dataList))




def transform(functions,x,problems,i):    
    
    for function in functions:
        if type(x) == np.float64:
            newX = problems[i].tolist()
            newX.append(x)
            x = np.array(newX)
        
        if type(function) == np.ndarray:
            x = np.matmul(np.transpose(function),x)
        elif type(function) == int:
            x = np.array(thinker.runIntFunction(x,function))
    
    return(x.sum())
    
    



#main(INfILE)    