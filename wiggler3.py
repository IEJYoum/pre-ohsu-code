# -*- coding: utf-8 -*-
"""
Created on Tue Sep 29 01:04:46 2020

@author: Jalaa
"""

import random
import numpy as np
import time
import matplotlib.pyplot as plt 
import math
import statistics as stat
import copy



TANHTERMS = 3
MAXREPEATS = 200
GENSIZE = 10
SCOREF = [2]

class Node():
    def __init__ (self,name,tanhF):
        self.name = name
        self.tanhF = tanhF #2d to 2d

                
    def runSelf(self,array): #No answers        
        tanhA = []
        for i in range(array.shape[1]):
            newCol = runThF(self.tanhF[i,:],array[:,i])
            tanhA.append(newCol)
        tanhA = np.array(tanhA)
        nxs = np.sum(tanhA, axis=0)
        return(nxs)
    
    def spawnWiggles(self,n,magnitude):
        shape = self.tanhF.shape
        wiggles = [self]
        for i in range(n):
            newThF = np.zeros(shape)
            for j in range(shape[0]):
                for k in range(shape[1]):
                    newThF[j,k] = self.tanhF[j,k] * (1 + random.uniform(-1,1)*magnitude)
            newNode = Node(self.name+i+1,newThF)
            wiggles.append(newNode)
            return(wiggles)
            
            
        
        

def main(dataA):
    shape = dataA.shape
    predictions = []
    answered = 0 
    while answered < shape[1]:
        switch = 0
        X = np.zeros((shape[0],shape[1]-1))
        for i in range(shape[1]):
            if i == answered:
                Y = dataA[:,i]
                switch = 1
            else:
                X[:,i-switch] = dataA[:,i]
        newCol = predict(np.append(X,np.array([Y]).T,axis = 1))
        predictions.append(newCol)
        plt.scatter(newCol,Y)
        plt.plot(Y)
        plt.plot(newCol)
        plt.show()
        answered += 1
    return(np.array(predictions).T)


def predict(dataA):
    shape = dataA.shape
    bestNode = Node(0,np.ones((shape[1],TANHTERMS * 3)))
    bestName = bestNode.name
    repeats = 0
    totalRepeats = 0
    while repeats < MAXREPEATS:
        wiggles = bestNode.spawnWiggles(GENSIZE,10/(repeats + totalRepeats/10 + 1))
        #wiggles = bestNode.spawnWiggles(GENSIZE,10/(repeats/10 + totalRepeats/20 + 1))
        #print("mag:",10/(repeats + totalRepeats/10 + 1))
        bestNode = pickBestNode(wiggles,dataA,SCOREF)
        if bestNode.name == bestName:
            repeats += 1
            totalRepeats += 1
        else:
            repeats = 0
            bestName = bestNode.name
            nxs = bestNode.runSelf(dataA)
            plt.scatter(nxs,dataA[:,-1])
            plt.show()        
    return(nxs)

            
        
        


def pickBestNode(nodes,array,scoreF): #has answers besides last in fold
    scores = []
    inArray = array[:,:-1]
    answers = array[:,-1]
    for node in nodes:
        nxs = node.runSelf(inArray)
        scores.append(score(nxs,answers,scoreF))
    bestI = scores.index(max(scores))
    #print("bestScore:",max(scores))
    return(nodes[bestI])
                  
      

def runThF(F,xs):     
     nxs = []    
     for x in xs:
         nx = 0
         for i in range(0,len(F)-2,3):
             nx += F[i] * math.tanh(F[i+1] * (x - F[i+2]))
         nxs.append(nx)
     return(nxs)      

 

def score(Xs,Ys,scoreF):
    scores = [99,99,99]
    score = 1
    for com in scoreF:
        currentS = scores[com]
        if currentS == 99:
            if com == 0:
                acc = getAcc(Xs,Ys) ##################### used xs mostly not zxs here
                scores[0] = acc * 100
            elif com == 1:
                cov = getCov(zScoreL(Xs),zScoreL(Ys))
                scores[1] = cov  
            elif com == 2:
                cost = getCost(Xs,Ys)    
                scores[2] = 1000000 - cost                    
        
        score *= max(scores[com],0)       
    return(score)

def getCost(v1,v2):
    cost = 0
    if len(v1) != len(v2):
        print("error mismatched comparison list length")
    for i in range(len(v1)):
        cost += (v1[i] - v2[i]) ** 2
    return(cost)


def getCov(v1,v2):
    if len(v1) != len(v2):
        print("error mismatched comparison list length")
    score = 0
    for index in range(len(v1)):
        i = v1[index]
        j = v2[index]
        score += i * j
    return(score)
    
def getAcc(v1,v2):
    if len(v1) != len(v2):
        print("error mismatched comparison list length")
    total = 0
    correct = 0
    for index in range(len(v1)):
        i = v1[index]
        j = v2[index]
        if i > 0 and j > 0:
            correct += 1
        elif i < 0 and j <= 0:
            correct += 1
        total += 1        
    #print("acc:",correct/total)    
    return(correct/total) 


def zScoreL(lis):
    mean = stat.mean(lis)
    sd = stat.stdev(lis) 
    lLis = len(lis)
    nL = np.zeros(lLis).tolist()
    if sd == 0:
        return(nL)
    for i in range(lLis):
        nL[i] = (lis[i] - mean)/sd
    return(nL)  

def zScoreA(A): #goes across each collumn
    TA = A.T
    shape = TA.shape
    nA = np.zeros(shape)
    i = 0
    for row in TA:       
        mean = stat.mean(row)
        sd = stat.stdev(row)
        for j in range(shape[1]):
            nA[i,j] = (TA[i,j] - mean)/(sd + 0)
        i += 1
    nA = nA.T
    return(nA)

 
#main(np.loadtxt("data\RetractCurve.txt"))       