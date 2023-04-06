# -*- coding: utf-8 -*-
"""
Created on Tue Jul 21 18:02:23 2020

@author: Jalaa
"""

import random
import numpy as np
import time


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
        
        functionsList = getFunctions()   
        return(np.array(datapoints),functionsList)
    
    elif routineL[0] == 1:
        functions = routineL[1]
        for function in functions:
            nextCoords = calculateNextCoords(function,nextCoords)
            #print(nextCoords)
        i = 0
        data2D = []
        while i < len(nextCoords):
            data2D.append((np.sum(nextCoords[i]),solutions[i]))
            i += 1                       
        return(data2D)
                    
 
def getFunctions():
    functionsList = []
    for node in NODES:
        functionsList.append(node.function)
    return(functionsList)


def loadFile(file):
    file = open(file,"r")
    for line in file:
        entries = line.split(",")
        datapoint = []
        i = 0
        while i < len(entries)-1:
            datapoint.append(float(entries[i]))
            i += 1
        PROBLEMS.append(datapoint)
        SOLUTIONS.append(entries[i])

    file.close()
    


def guess(datapoint,solution):
    nextCoords = datapoint
    while len(NODES) < MAXnODES:
        nextCoords = makeNode(nextCoords)
        if np.array_equal(nextCoords,solution):
            if testNodes(): 
                return(MAXgUESSES) 
    return(1)                 
        
    
def testNodes():
    functionList = []
    for node in NODES:
        functionList.append(node.function)
    test = 0
    lPROBLEMS = len(PROBLEMS)
    while test < MAXtESTS:
        index = random.randint(0,lPROBLEMS)
        nextCoords = getArray(index)
        solution = getSolution(index)        
        for function in functionList:
            nextCoords = calculateNextCoords(function,nextCoords)
        
        if np.array_equal(nextCoords,solution):
            pass
        
        else:
            return(False)
        test += 1
    
    #int("\n\nvalid transformations:")
    #for function in functionList:
        #int(function)        
    
    return(True)
        

        

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
    

    functionT = random.randint(0,2)
    if functionT < 2:
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
    else:
        functionL = generateMagMultF(coords)
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
        exponent = (random.random() - .5) * 10        
        arrayL.append(10 ** exponent)
        i += 1
    #print(arrayL)
    functionL = [1,np.array(arrayL)]
    return(functionL)    



def runRandomF(row,function):
    if function[0] < 2:
        pointA = runMultFunction(row,function)
        return(pointA)
#    elif function[0] == 1:
        
        

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
            


#def funListFunction(row,function):
    



def getArray(data,i):    
    array = data[i][:-1]
    return(array)
  
  
    
    
#main(np.array([[1,1],[2,2],[0,1]]))   