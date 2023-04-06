# -*- coding: utf-8 -*-
"""
Created on Tue Jul 21 18:02:23 2020

@author: Jalaa
"""

import random
import numpy as np
import time
import matplotlib.pyplot as plt 
import math
import statistics as stat


class Node():
    def __init__(self,coordinates,function,nextCoords):
        self.coordinates = coordinates
        self.function = function
        self.nextCoords = nextCoords 
    
PROBLEMS = []
SOLUTIONS = []



NODES = []
MAXnODES = 10    
MAXgUESSES = 100
MAXtESTS = 20




#MAKE THINKER PROCESS DATA TO RUN THROUGH CLUSTERING/LINREG ALGORITHM (needs 2d projection) AND RETURN THE RESULT WITH THE HIGHEST CORRELATION
def main(dataArray,routineL):
    problems = []
    solutions = []
    for i in dataArray:
        problems.append(i[:-1])
        solutions.append(i[-1])      
    nextCoords = np.array(problems)
    if routineL[0] == 0:
        NODES.clear()
        lNODES = len(NODES)
        while lNODES < MAXnODES:
            nextCoords = makeNode(nextCoords,problems)
            lNODES = len(NODES) + random.randint(0,MAXnODES) #* MAXnODES
           
        i = 0
        datapoints = []
        while i < len(nextCoords):
            datapoints.append(np.append(nextCoords[i],solutions[i]))
            i += 1
        
        Fs = getFunctions()   
        return(np.array(datapoints),Fs)
    
    elif routineL[0] == 1:
        Fs = routineL[1]
        for function in Fs:
            nextCoords = calculateNextCoords(function,nextCoords)
            #print(nextCoords)
        i = 0
        data2D = []
        while i < len(nextCoords):
            data2D.append((np.sum(nextCoords[i]),solutions[i]))
            i += 1                       
        return(data2D)
        
    elif routineL[0] == 2:
        #dataArray = data2D and is a list
        weights = routineL[1]
        return(weigh(dataArray,weights))
        
        
                    


 

def weigh(data2D,weights):
    #print(data2D)
    xs = []
    ys = []
    for i in data2D:
        xs.append(i[0])
        ys.append(i[1])
    
    Mxs = max(xs)
    msx = min(xs)
    
    extremePoint = max([Mxs**2,msx**2])**.5
    i = 0
    lxs = len(xs)
    while i < lxs:
        xs[i] = xs[i]/extremePoint
        i += 1
    
    
    step = weights[-1]
    if step > .5:
        step = .01
    i = -1
    weightData2D = []
    while i < 1:
        nearX = []
        nearY = []
        j = 0
        while j < lxs:
            x = xs[j]
            y = ys[j]            
            if x >= i and x < i + step:
                nearX.append(x)
                nearY.append(y)
            j += 1
        
        if len(nearY) > 1:
            score = weightScore(nearY,weights)         
            weightData2D.append((i,score))
        
        i += step 
    
    plt.scatter(xs,ys)
    plt.show()
    plot(weightData2D)
    return(weightData2D)




def weightScore(nearY,weights):
    meanY = stat.mean(nearY)
    devY = stat.stdev(nearY)
    score = (meanY ** weights[0]) * ((1/devY ** weights[1]) + len(nearY) ** weights[2])
    return(score)



def getFunctions():
    functionsList = []
    for node in NODES:
        functionsList.append(node.function)
    return(functionsList)

 
                
        

        

        

def makeNode(coords,problems):
    if coords.ndim == 1:
        newCoords = []
        i = 0
        lCoords = len(coords)
        while i < lCoords:
            problemBucket = problems[i].tolist()
            problemBucket.append(coords[i])

            newCoords.append(problemBucket) 
            i += 1
        coords = np.array(newCoords)   
    

    functionT = random.randint(0,8)
    if functionT < 7:
        function = generateRandomF(coords,functionT)
                
    else:
        function = random.randint(0,4)        

    nextCoords = calculateNextCoords(function,coords)
    node = Node(coords,function,nextCoords) 
    NODES.append(node)
    #print(nextCoords)
    return(nextCoords)


def generateRandomF(coords,functionT): #make it so coords can interact with themselves e.g. multiply
    if functionT == 0:
        functionL = generateMultF(coords)
        return(functionL)
    elif functionT == 1:
        functionL = generateMagMultF(coords)
        return(functionL)
    else:
        functionL = genTrigF(coords)
        return(functionL)

def genTrigF(coords):
    indexL = []
    i = 0
    #print(coords[0,])
    #time.sleep(.5)
    lArray = len(coords[0,])
    while i < lArray:
        indexL.append(random.randint(0,5*lArray))
        
        i += 1    
    #print(indexL)
    functionL = [2,indexL]
    return(functionL)


def generateMultF(coords):
    arrayL = []
    i = 0
    lArray = len(coords[0,])
    while i < lArray:
        arrayL.append(random.random() - .5)
        i += 1
    #print(arrayL)
    functionL = [0,np.array(arrayL)]
    return(functionL)




def generateMagMultF(coords):
    arrayL = []
    i = 0
    lArray = len(coords[0,])
    while i < lArray:
        exponent = (random.random() - .5) * 5        
        arrayL.append(10 ** exponent)
        i += 1
    #print(arrayL)
    functionL = [1,np.array(arrayL)]
    return(functionL)    



def runRandomF(row,functionL):
    if functionL[0] < 2:
        newRow = runMultFunction(row,functionL)
        return(newRow)
    elif functionL[0] == 2:
        newRow = runTrigF(row,functionL)
        return(newRow)
        

def runTrigF(row,functionL):
    try:
        indexL = functionL[1]
        i = 0
        lRow = len(row)
        while i < lRow:
            command = indexL[i]
            if command == 0:
                row[i] = math.cos(row[i])
            elif command == 1:
                row[i] = math.sin(row[i])
            elif command == 2:
                pass
                #row[i] = math.cosh(row[i])            
            elif command == 3:
                row[i] = math.sinh(row[i])
            i += 1
        return(row)
    except:
        print("error running trig function, returning 1s")
        zeRow = []
        for i in row:
            zeRow.append(1)        
        return(zeRow)


def runMultFunction(row,function):
    matrix = function[1]
    return(np.multiply(row,matrix))


def runEleMultFunction(row,function):
    matrix = function[1]
    functionL = matrix.tolist()
    i = 0
    newRow = []
    lRow = len(row)
    while i < lRow:
        newRow.append(row[i] * functionL[i])
        i += 1
    return(newRow)
    

def runIntFunction(row,function):
    lRow = len(row)
    if function == 0: #subtract all elements from first element and returns one value
        i = 1
        newRow = []
        returnValue = row[0]
        while i < lRow:
            returnValue -= row[i]
            i += 1
        for element in row:
            element = returnValue
            newRow.append(element)
        return([newRow])            
    elif function == 1: #square all elements
        newRow = []
        for element in row:
            element = element ** 2
            newRow.append(element)
        return(newRow)
    elif function == 2:
        newRow = []
        maxInRow = max(row)
        for element in row:
            element = maxInRow
            newRow.append(element)
        return(newRow)        
    elif function == 3:
        newRow = []
        minInRow = min(row)
        for element in row:
            element = minInRow
            newRow.append(element)
        return(newRow)
    
    elif function == 4:
        newRow = []
        rowSum = sum(row)
        for element in row:
            element = rowSum
            newRow.append(element)
        return(newRow)



def calculateNextCoords(function,coords):
    if type(function) == np.ndarray:
        newCoords = []        
        for coord in coords:
            try:
                newCoords.append(np.matmul(np.transpose(function),coord))
            except:
                print("ERROR \n function:", function)
                print(coords)
                time.sleep(5)
                newCoords.append(np.array([1,1,1,1]))
        return(np.array(newCoords))
    
    else:
        nRows = coords.shape[0]
        i = 0
        rows = []
        if type(function) == int:
            while i < nRows:
                row = coords[i,0:]
                newRow = runIntFunction(row,function)
                rows.append(newRow)
                i += 1
        elif type(function) == list:
            while i < nRows:
                row = coords[i,0:] 
                rows.append(runRandomF(row,function))
                i += 1
        
        return(np.array(rows))       
            


def getArray(data,i):    
    array = data[i][:-1]
    return(array)
  
 
    
def plot(data2D):
    xs = []
    ys = []
    for point in data2D:
        xs.append(point[0])
        ys.append(point[1])
    plt.scatter(xs,ys)
    plt.show()    
    
    
    
#main(np.array([[1,1],[2,2],[0,1]]))   