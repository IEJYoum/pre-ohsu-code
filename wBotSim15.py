# -*- coding: utf-8 -*-
"""
Created on Mon Jan 11 04:24:15 2021

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
import wBot15 as bot




#implement scoring routine based on normalization line from datP file



def main(): #make load and saveBot routines
    startTime = time.time()
    data = np.loadtxt("data\RetractCurve.txt")
    data = np.append([data[:,0]],np.append([data[:,4]],np.append([data[:,6]],np.append([data[:,1]],[data[:,2]],axis=0),axis=0),axis=0),axis=0).T
    rollData = rollA(data,10)
    plt.plot(data.T[2])
    plt.plot(rollData.T[2])
    plt.show()
    shape = data.shape
    #bot0 = loadBot("bot1/Tensor.txt")
    bot0 = spawnBlankBot(shape)
    print(bot0.tensor[0],"starting tensor[0]\n\n",bot0.wiggler[0],"starting wiggler[0]\n\n",bot0.memory[0],"\n STARTING MEMORY[0]\n\n\n\n\n\n")
    bot0 = trainBot(bot0,data,rollData,10)########################@@@@@@@@@@@@@@@@@@@
    print(bot0.tensor[0],"\n\n",bot0.wiggler[0],"\n\n",bot0.memory[0],"\n")
    print("RUNTIME:",(time.time()-startTime)/60)
    np.savetxt("bot1\Tensor.txt",bot0.tensor[0])
    


def loadBot(location):
    t = np.array([np.loadtxt(location)])
    sh = t.shape
    w = np.ones(sh) * .1
    m = copy.deepcopy(w) * .5
    Bot = bot.Bot(0,t,w,m)
    return(Bot)


def spawnBlankBot(shape):
    #t = np.ones([1,shape[0],shape[1]])
    t = np.ones([1,shape[1],shape[1]])    #[A,B,Q,H,R]             
    #t = np.add(np.array([np.identity(shape[1])]),t*.1)
    t= np.array([np.identity(shape[1])])
    w = np.ones(t.shape) * 2
    for row in range(shape[1]):
        for col in range(shape[1]):
            if row > col:            
                t[0,row,col] = 0
                w[0,row,col] = 0
    
    m = copy.deepcopy(w) * 5
    Bot = bot.Bot(0,t,w,m)
    return(Bot)

def getKey(shape):
    key = np.ones((shape[1],shape[1])) 
    for n in range(shape[1]):
        for m in range(shape[1]):
            if m == 0 and n == 0:
                key[0,0] = 2
            elif n == 0:
                key[n,m] = 0
            elif m == 0:
                key[n,m] = 0
                
    print(key)      
    return(key)



def trainBot(bot0,data,rollData,minScore):  
    bestBot = bot0
    bScore = -9999999999999
    repeats = 0
    nextGen = bestBot.spawn(1000)
    means = []
    for i in range(data.shape[1]):
        means.append(stat.mean(data[:,i]))
    print(means,"means")
    while bScore < minScore:      
        scores = []
        wiggles = nextGen
        for egg in wiggles:
            t = egg.tensor
            outData = runTensor(t,data)
            scores.append(score(rollData,means,outData,t))
        if repeats < 10:
            scores[0] = scores[0]
        bestI = scores.index(max(scores))
        bestBot = wiggles[bestI]
        bScore = scores[bestI]
            
        if bestI == 0:
            nextGen = bestBot.spawn(100)
            if random.randint(1,100) == 4:
                print(repeats, "repeats")
                print("wiggler\n",bestBot.wiggler[0])
            repeats += 1  
        else:   
            nextGen = bestBot.spawn(100)                            
           
        
            repeats = 0
            if random.randint(1,4) == 4: 
                print(repeats, "repeats")              
                print("new best!",bScore)
                #print("new best!",bScore)
                print("tensor\n",bestBot.tensor[0])
                print("wiggler\n",bestBot.wiggler[0])
                print("\nmemory\n",bestBot.memory[0],"\n\n")                
                viewI = random.randint(0,data.shape[1]-1)
                #viewI = 0
                bestOut = runTensor(bestBot.tensor,data)
                plt.plot(data[:,viewI])
                plt.plot(rollData[:,viewI])
                plt.plot(bestOut[:,viewI])
                plt.show()

    print("final score:", bScore)
    bestOut = runTensor(bestBot.tensor,data)
    plt.plot(data[:,2])
    plt.plot(bestOut[:,2])
    plt.show()
    return(bestBot)


def runTensor1(t,data):
    return(t[0])

def runTensor(t,data):
    #A = copy.deepcopy(t)[0]
    A = t[0]
    #A[0,0] = 1.001
    guesses = np.matmul(data,A) 
    return(guesses)



def score(dataA,means,guessA,tensor):
    scores = []
    for coli in range(dataA.shape[1]):
        datCol = dataA[1:,coli]
        guessCol = guessA[:-1,coli]
        diffsA = np.absolute(np.subtract(datCol,guessCol))
        scores.append(np.sum(diffsA)/means[coli])    
    scores= np.array(scores)    
    return(-np.sum(scores))
        
        
        
def score1(dataA,means,guessA,tensor):
    #score1 = .001/((1-tensor[0,0,0])**2 + .00001)
    #score = score1 
    cost = 0
    shape = dataA.shape
    #if guessA.shape != dataA.shape:
        #print("error,mismatched array shapes",guessA.shape,dataA.shape)
    for i in range(shape[1]):
        #score -= .001/((1-tensor[0,i,i])**2 + .00001)
        mn = means[i]
        for j in range(shape[0]-1):      
            cost += ((dataA[j+1,i] - guessA[j,i])/mn)**2
        
    return(-cost)

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

    #plt.plot(dataL)
    #plt.plot(newL)
    #plt.show()
    return(newL)
'''
def randomW(w):
    shape = w.shape
    w = np.ones(shape)
    for i in range(shape[0]):
        for j in range(shape[1]):
            for k in range(shape[2]):
                if random.uniform(-.01,1.01) < w[i,j,k]:
                    w[i,j,k] = random.uniform(0,1)
                else:
                    w[i,j,k] = 0
    return(w)
'''        

main()