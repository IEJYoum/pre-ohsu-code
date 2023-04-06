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





'''
class Datapoint():
    def __init__ (self,coords,iVars,answer):
        pass
'''



class Node(): #make it write data to self so every node has an individual mind and contributes to a hive mind
    def __init__ (self,name,timeF,linF,tanhF,scoreF,age,pScore):
        self.name = name
        self.timeF = timeF #2D to 2D
        self.linF = linF   # 2D to 1D
        self.tanhF = tanhF # 1D to 1D     make this a list that gets packed
        self.scoreF = scoreF
        self.age = age
        self.pScore = pScore #[trials,sucesses,pScore]

                
    def runSelf(self,array): #No answers        
        if TIMEdATA != 0:
            array = runTimeF(self.timeF,array)
        else:
            pass
            #array = zScoreA(array)
        cxs = runLinF(self.linF,array)
        nxs = runThF(self.tanhF,cxs)
        return(nxs)

        
        
            
        
        


def pickBestNode(nodes,array,scoreF): #has answers besides last in fold
    scores = []
    inArray = array[:,:-1]
    answers = array[:,-1]
    for node in nodes:
        nxs = node.runSelf(inArray)
        scores.append(score(nxs,answers,scoreF))
    bestI = scores.index(max(scores))
    return(nodes[bestI])
            
   

def wibble(lis,mag):
    newL = []
    for el in lis:
        newEl = el + el * mag * random.uniform(-1,1)
        newL.append(newEl)
    return(newL)
        
      


def runLinF(F,A): #horizontal
    shape = A.shape
    while len(F) < shape[1]:
        print("linF shorter than terms in array")
        F.append(0)
    outXs = []
    for row in A:
        outRow = []
        i = 0
        for elem in row:
            outRow.append(elem * F[i])
            i += 1
        outXs.append(sum(outRow))
    return(outXs)
            
        


def runThF(F,xs):     
     nxs = []
     for x in xs:
         nx = 0
         for i in range(0,len(F)-2,3):
             nx += F[i] * math.tanh(F[i+1] * (x - F[i+2]))
         nxs.append(nx)
     return(nxs)      

 

def score(Xs,Ys,scoreF):
    meanX = stat.mean(Xs) 
    stdX = stat.stdev(Xs)
    if stdX == 0:
        return(0)
    zXs = []
    for x in Xs:
        zXs.append((x-meanX)/stdX) #if using xs get big speed boost by skipping
    scores = [99,99,99,99,stat.stdev(zXs)]
    score = 1
    nScore = 1
    for com in scoreF:
        currentS = scores[com]
        if currentS == 99:
            if com == 0:
                acc = getAcc(zXs,Ys) ##################### used xs mostly not zxs here
                scores[0] = (acc-.5) * 100
            elif com == 1:
                cov = getCov(zXs,Ys)
                scores[1] = cov                          
            elif com == 2:
                net = getNet(zXs,Ys)
                scores[2] = net  
            elif com == 3:   ####selection function to decide whether to vote or abstain is key
                net = getNet(Ys,zXs)
                scores[3] = net
        
        score *= max(scores[com],1)
        nScore *= min(scores[com],-1) * -1
    #print("score, nScore", score, nScore)       
    return(score-nScore)

def getNet(v1,v2): #v2 is answers
    if len(v1) != len(v2):
        print("error mismatched comparison list length")
    score = 0
    for index in range(len(v1)):
        i = v1[index]
        j = v2[index]
        if i > 0:
            score += j
        elif i < 0:
            score -= j
    return(score)

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

        