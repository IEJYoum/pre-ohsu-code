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


TIMEfMAXrECALL = 20


class Node():
    def __init__ (self,name,timeF,linF,thF,infoA):
        self.name = name
        self.timeF = timeF #weights function for weighted Zscore. Make flexible so 1st point in array always gets 0, then second can only consider first, etc. 
        self.linF = linF #vec, horzF
        self.thF = thF #always 1D to 1D (list to list)
        self.infoA = infoA #[]
    
    def runSelf(self,inpOb,ans,scoreF):
        #shape = inpOb.shape
        if type(self.timeF) == int:  #this lets node see the future from each datapoint
            timeA = inpOb
        else:
            timeA = np.array(runTimeF(self.timeF,inpOb)).T
        linOut = runLinF(self.linF,timeA)
        out1D = runThF(self.thF,linOut)
        sco = score(out1D,ans,scoreF) #[mean,var,acc,cov[0,0],cov[0,1],cov[1,0]]
        #self.infoA.clear()
        #self.infoA.append(scoreL) 
        return(out1D,sco)   
    
    def runSelf1(self,inpOb): #inpOb should not have answers
        #shape = inpOb.shape
        if type(self.timeF) == int:  #this lets node see the future from each datapoint
            timeA = inpOb
        else:
            timeA = np.array(runTimeF(self.timeF,inpOb)).T
        linOut = runLinF(self.linF,timeA)
        out1D = runThF(self.thF,linOut) 
        return(out1D) 

    def showSelf(self):
        print("\n\nNode name:",self.name)
        if type(self.timeF) == list:    
            weights = unpackTimeF(self.timeF)
            tix = np.arange(len(weights))
            plt.scatter(tix,weights)
            plt.show()
            print(self.timeF,"timeF\n")
        plt.scatter(np.arange(len(self.linF)),self.linF)
        plt.show()
        print(self.linF,"linF\n")
        showThF1(self.thF,2)
        showThF1(self.thF,10)
        print(self.thF,"tanhF\n")
        


class Gate():
    def __init__ (self,name,scoreF,selectionF):
        self.name = name
        self.scoreF = scoreF
        self.selectionF = selectionF

    
    def pickNodes(self,nodes,array):
        outA = []
        scores = []
        for node in nodes:
            out1D,score = node.runSelf(array[:,:-1],array[:,-1],self.scoreF)
            outA.append(out1D)
            scores.append(score)        
        goodNodes = []
        goodnxs = []        
        if type(self.selectionF) == int:
            if self.selectionF == 0:
                goodNodes = nodes
                goodnxs = outA
            elif self.selectionF == 1:
                goodInd = scores.index(max(scores))
                goodNodes.append(nodes[goodInd])
                goodnxs.append(outA[goodInd])
            elif self.selectionF == 2:
                meanS = stat.mean(scores)
                for i in range(len(scores)):
                    if scores[i] > meanS:
                        goodNodes.append(nodes[i])
                        goodnxs.append(outA[i])
            elif self.selectionF == 3:
                #print("Node net scores for selecting:", scores)
                for i in range(len(scores)):
                    if scores[i] > 0:
                        goodNodes.append(nodes[i])
                        goodnxs.append(outA[i])
            
        return(goodNodes,goodnxs)
        


def runTimeF(F,A):
    shape = A.shape
    newA = []
    weights = unpackTimeF(F)
    for index in range(shape[1]):
        col = A[:,index].tolist()
        newCol = []
        for i in range(len(col)):
            recXs = []
            for j in range(TIMEfMAXrECALL):
                if i - j > -1:
                    recXs.append(col[i-j]) #most recent will be first
            if len(recXs) < 2:
                newCol.append(0)
            else:
                total = 0
                weightSum = 0
                for k in range(len(recXs)):
                    total += recXs[k] * weights[k]
                    weightSum += weights[k]
                
                wMean = total / weightSum
                xDiff = recXs[0] - wMean
                newCol.append(xDiff)        
        newA.append(newCol)
    return(newA)
                    
                    
                    
def unpackTimeF(F): #f is 1D
    weights = []
    for i in range(TIMEfMAXrECALL):
        weight = 0
        j = 0
        for term in F:
            weight += term**2 * ((TIMEfMAXrECALL-i)/TIMEfMAXrECALL)**(j/2)
            j += 1

        weights.append(weight)
    return(weights)                  
        


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
         for term in F:
             nx += term[0] * math.tanh(term[1] * (x - term[2]))
         nxs.append(nx)
     #nxs = zScoreL(nxs) 
     return(nxs)      

 

def score(Xs,Ys,scoreF):
    meanX = stat.mean(Xs) 
    stdX = stat.stdev(Xs)
    if stdX == 0:
        return(0)
    zXs = []
    for x in Xs:
        zXs.append((x-meanX)/stdX)
    scores = [99,99,99,99,stdX]
    acc = 99
    cov = 99
    netXY = 99
    netYX = 99
    score = 1
    for com in scoreF:
        currentS = scores[com]
        if currentS == 99:
            if com == 0:
                acc = max(getAcc(zXs,Ys),0)
                scores[0] = acc
                score *= acc
            elif com == 1:
                cov = max(getCov(zXs,Ys),0)
                scores[1] = cov
                score *= cov           
            elif com == 2:
                net = max(getNet(zXs,Ys),0)
                scores[1] = net
                score *= net         
            elif com == 3:
                net = max(getNet(Ys,zXs),0)
                scores[1] = net
                score *= net 
        else:
            score *= scores[com]
    return(score)

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
        
    return(correct/total - .5) 

def showThF(F):
    demoXs = []
    for i in range(-100,100):
        demoXs.append(i/30)
    nxs = runThF(F,demoXs) 
    plt.scatter(demoXs,nxs)
    plt.show()    


def showThF1(F,rnge):
    demoXs = []
    for i in range(-100*rnge,100*rnge,2):
        demoXs.append(i/100)
    nxs = runThF(F,demoXs) 
    plt.scatter(demoXs,nxs)
    plt.show()     