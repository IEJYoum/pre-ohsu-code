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
import wBotObjDEMO as bot







def main():
    startTime = time.time()
    data = np.loadtxt("data\RetractCurve.txt")
    rollData = rollA(data,10)
    shape = data.shape
    #bot0 = loadBot("bot0/Tensor.txt")
    bot0 = spawnBlankBot(shape)
    print(bot0.tensor[0],"\n\n",bot0.wiggler[0],"\n\n",bot0.memory[0],"\n")
    bot0 = trainBot(bot0,rollData)
    print(bot0.tensor[0],"\n\n",bot0.wiggler[0],"\n\n",bot0.memory[0],"\n")
    print("RUNTIME:",(time.time()-startTime)/60)
    np.savetxt("bot0\Tensor.txt",bot0.tensor[0])
    


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
    w = copy.deepcopy(t)
    m = copy.deepcopy(t) * .5
    t = np.array([np.identity(shape[1])])
    Bot = bot.Bot(0,t,w,m)
    return(Bot)


def trainBot(bot0,data):  
    bestBot = bot0
    bScore = -9999999999999
    repeats = 0
    nextGen = bestBot.spawn(100)
    means = []
    for i in range(data.shape[1]):
        means.append(stat.mean(data[:,i]))
    print(means,"means")
    while bScore < 10:      
        scores = []
        wiggles = nextGen
        for egg in wiggles:
            t = egg.tensor
            outData = runTensor(t,data)
            scores.append(score(data,means,outData,t))
        bestI = scores.index(max(scores))
        bestBot = wiggles[bestI]
        bScore = scores[bestI]
            
        if bestI == 0:
            nextGen = bestBot.spawn(40)
            repeats += 1  
        else:   
            nextGen = bestBot.spawn(20)                
            print("new best!",bScore)
            '''
            print("tensor\n",bestBot.tensor[0][0])
            print("wiggler\n",bestBot.wiggler[0][0])
            print("\nmemory\n",bestBot.memory[0][0],"\n\n")
            '''
            repeats = 0
            if random.randint(0,20)==4:
                bestOut = runTensor(bestBot.tensor,data)
                plt.plot(data[:,2])
                plt.plot(bestOut[:,2])
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
    guesses = np.matmul(data,t[0]) 
    return(guesses)
        
def score(dataA,means,guessA,tensor):
    score = 0
    cost = 0
    shape = dataA.shape
    if guessA.shape != dataA.shape:
        print("error,mismatched array shapes",guessA.shape,dataA.shape)
    for i in range(shape[1]):
        score += min((1-tensor[0,i,i])**2,1)*10
        mn = means[i]
        for j in range(shape[0]-1):      
            cost += ((dataA[j+1,i] - guessA[j,i])/mn)**2
        
    return(score/cost)    

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

    plt.plot(dataL)
    plt.plot(newL)
    plt.show()
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