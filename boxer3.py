# -*- coding: utf-8 -*-
"""
Created on Wed Jul 22 03:58:19 2020

@author: Jalaa
"""

import parametric9 as parametric
import thinker11 as thinker
import copyTxtToCsv
import parseUpDownKaggleStockData as parse
import copy
import time
import numpy as np


INfILE = "agq stock prices small.txt"
#INfILE = "irisData.txt"
#INfILE = "xorData.txt"

#gotta manually update answers[] in testfunctions when using different file


MAXtIME = 5

def main(file):
    dataArray = parse.main(INfILE)
    #print(dataArray)
    #time.sleep(10)
    overlapFraction = 9999
    startTime = time.time()
    #bestFunctions = []
    #bestRanges = []
    leastOverlap = 30
    while time.time() - startTime < MAXtIME:
        returns = thinker.main(dataArray)
        transformedData = returns[0]
        functions = returns[1]
        data2D = parametric.parseData(transformedData)
        returns2 = parametric.assessOverlap(data2D)
        overlapFraction = returns2[0]
        ranges = returns2[1]
        if overlapFraction < leastOverlap:
            bestFunctions = functions
            bestRanges  = ranges
            leastOverlap = overlapFraction
            bestData = data2D
    
    testFunctions(dataArray,bestFunctions,bestRanges)

    parametric.plot(bestData) #this plot function plots the last data and not the best data
    print("functions",bestFunctions)
    #print(data)
    

def testFunctions(dataArray,functions,ranges):
    nCorrect = 0
    problems = []
    solutions = []
    for i in dataArray:
        problems.append(i[:-1])
        solutions.append(i[-1])
    i = 0
    while i < len(problems):
        x = problems[i]
        x = transform(functions,x,problems,i) #returns single value like thinker would
        cluster = pickCluster(x,ranges)
        #answers = [1,0,15]
        answers = [1,0,15]
        answer = answers[cluster]
        if answer == solutions[i]:
            nCorrect += 1
        else:
            print("WRONG ANSWER:",answer,solutions[i])            
        i += 1
    print("FRACTION CORRECT:",nCorrect/len(problems))
        
        

def pickCluster(x,ranges):
    candidates = []
    for rng in ranges:
        if x >= rng[0] and x <= rng[1]:
            candidates.append(rng)
    if len(candidates) == 1:   
        return(ranges.index(candidates[0]))
    elif len(candidates) == 0:
        print("ERROR, DATA FALLS OUTSIDE EVERY CLUSTER, implement nearest cluster alg")
        return(-1)
   
    else:
        medians = []
        for candidate in candidates:
            medians.append((candidate[0]+candidate[1])/2)
        distances = []
        for median in medians:
            distance = (median - x)**2
            distances.append(distance)
        shortestDistanceCandidateIndex = distances.index(min(distances))
        #print("!!!",distances)
        #print(shortestDistanceCandidateIndex)
        return(ranges.index(candidates[shortestDistanceCandidateIndex]))






def transform(functions,x,problems,i):
    #print(x)
    '''
    if coords.ndim == 1:
        newCoords = []
        i = 0
        lCoords = len(coords)
        while i < lCoords:
            problemBucket = problems[i].tolist()
            problemBucket.append(coords[i])
            #print(problemBucket)
            newCoords.append(problemBucket) 
            i += 1
        coords = np.array(newCoords) 
    '''
    
    
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
    
    



main("arrayShaped.csv")    