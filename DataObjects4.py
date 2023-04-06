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
import mpmath


np.seterr("warn")

#dataL = np.loadtxt("data/F data.csv")[:,1]

def main(dataL):
    fitter = Fitter(0,np.ones(6*3),np.ones(6*3),[50,20,1],[3])
    tuneFit(fitter,dataL)
    


class Fitter():
    def __init__(self,name,wiggler,trigF,tuneF,scoreF):
        self.name = name
        self.wiggler = wiggler
        self.trigF = trigF
        self.tuneF = tuneF #[nodes per loop, mRepeats, magnitudeAttenuationRate]
        self.scoreF = scoreF
    
    def run(self,answers):
        eXs = runTrigF(self.trigF,np.arange(len(answers)))
        sco = score(eXs,answers,self.scoreF)
        return(eXs,sco)
    
    
    
 
def tuneFit(fitter,dataL):
    repeats = 0
    totalRepeats = 0
    perLoop = fitter.tuneF[0]
    mRepeats = fitter.tuneF[1]
    magAtten = fitter.tuneF[2]
    bestName = fitter.name
    bestFit = fitter
    while repeats < mRepeats:
        spawn = []
        magnitude = 20 * 1.1**(-(totalRepeats/4+repeats*2) * magAtten)
        print("magnitude:",magnitude)
        for i in range(perLoop*int((repeats+1)**.5)):
            spawn.append(copy.deepcopy(bestFit))
            spawn[i].name += i
            if i > 0:
                spawn[i].trigF,spawn[i].wiggler = wiggle(spawn[i].trigF,spawn[i].wiggler,magnitude)
        #for j in spawn:
         #   print(j.name)
        bestFit = pickBestFitter(dataL,spawn)  
        if bestFit.name == bestName:            
            repeats += 1
            totalRepeats+=1

        else:
            repeats = 0
            bestName = bestFit.name   
            plt.plot(dataL)
            showTrigF(bestFit.trigF)
            xs,sco = bestFit.run(dataL)
            print('best score:',sco,"\n")
            print(bestFit.name,bestFit.trigF,bestFit.wiggler,"\n\n\n")
    return(bestFit)
           
        

def wiggle(lis,wiggler,magnitude):  #magnitude is value multiplied by wiggler (to scale down with generations or not?)
    lLis = len(lis)
    nLis = []
    nWig = []
    for i in range(lLis):
        ran = random.uniform(-1,1) * random.uniform(0,1)
        w = wiggler[i]
        newI = lis[i] + lis[i] * (w**2 * ran) * magnitude 
        newW = w + (w**2)**.5 * ran
        nLis.append(newI)
        nWig.append(newW)
    return(nLis,nWig)

def pickBestFitter(xs,fitters): 
    scores = []
    for fitt in fitters:
        nxs,score = fitt.run(xs)
        scores.append(score)
    bestI = scores.index(max(scores))
    print(max(scores))
    return(copy.deepcopy(fitters[bestI]))


def runThF(F,xs):     
     nxs = []
     for x in xs:
         nx = 0
         for i in range(0,len(F)-2,3):
             nx += F[i] * math.tanh(F[i+1] * (x - F[i+2]))
         nxs.append(nx)
     return(nxs)      

def runTrigF(F,xs):
    
    nxs = []
    for x in range(len(xs)):
        nx = 0
        for i in range(0,len(F)-5,6):
            #nx += F[i] * math.tanh(1/(F[i+1]+1) * (x - F[i+2])) + F[i+3] * float(mpmath.sech(1/(F[i+4]+1)) * (x - F[i+5]))
            #nx += F[i] * math.tanh(1/(F[i+1]+1) * (x - F[i+2])) + F[i+3] * math.tanh(1/(F[i+4]+1)) * (x - F[i+5])
            nx += F[i] * math.tanh(1/(F[i+1]+1) * (x - F[i+2])) + F[i+3] * (x - F[i+5]) ** F[i+4]
        nxs.append(nx)
    return(nxs)

def showTrigF(F):
    xs = np.arange(100)
    ys = runTrigF(F,xs)
    plt.plot(ys)
    plt.show()



def score(Xs,Ys,scoreF):
    zXs = Xs
    scores = [99,99,99,99]
    score = 1
    nScore = 1
    for com in scoreF:
        currentS = scores[com]
        if currentS == 99:
            if com == 0:
                acc = getAcc(zXs,Ys) ##################### used xs mostly not zxs here
                scores[0] = (acc-.5) * 100
            elif com == 1:
                try:
                    cov = getCov(zScoreL(zXs),zScoreL(Ys)) * len(Xs)
                except:
                    print("Error with zscore")
                    cov = 0
                scores[1] = cov                          
            elif com == 2:
                cost = getCost(zXs,Ys)
                scores[2] = -cost
            elif com == 3:
                cost = getCostSquared(zXs,Ys)
                scores[3] = -cost

        
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

def getCost(v1,v2):
    if len(v1) != len(v2):
        print("error mismatched comparison list length")
    cost = 0
    for i in range(len(v1)):
        cost += ((v1[i]-v2[i])**2)**.5
    return(cost)

def getCostSquared(v1,v2):
    if len(v1) != len(v2):
        print("error mismatched comparison list length")
    cost = 0
    for i in range(len(v1)):
        cost += ((v1[i]-v2[i])**2)
    return(cost)


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

#main()