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



class Filter(): #make it write data to self so every node has an individual mind and contributes to a hive mind
    def __init__ (self,name,Cs,tuneF,scoreF):
        self.name = name
        self.Cs = Cs #[A,B,Q,H,R]        
        self.tuneF = tuneF
        self.scoreF = scoreF  #[array where index value is coeff for cost score for nth value in Kalman Filter output and mth arbitrary input list (first dims*dims should be filled with coeffs for kalman filter reading measurements)]

            
    def run(self,dataL):       
        nxs = []
        lData = len(dataL)
        x = dataL[0]
        p = 1       
        for i in range(lData):
            meas = dataL[i]
            x,p = self.predict(x,p)
            x,p = self.update(x,p,meas)
            nxs.append(x)
        nxs = nxs
        return(nxs)

    def predict(self,x,p):
        A = self.Cs[0] #1D
        B = self.Cs[1] #2x1
        Q = self.Cs[2]
        if Q < 0:
            Q = -Q
        X = A*x + B
        P = A*x*A + Q
        return(X,P)


    def update(self,x,p,meas):
        H = self.Cs[3] #2x2
        R = self.Cs[4] #2x2
        if R < 0:
            R = -R
        I = 1
        K1 = p*H
        K2 = H*p*H + R
        K = K1/K2
        X = x + K*(meas - H*x)
        P = (I - K*H)*p
        return(X,P)
        
    def showSelf(self,xs):
        nxs = self.run(xs)
        plt.plot(np.arange(len(nxs)),nxs)
        plt.show()
    


class Fitter():
    def __init__(self,name,tanhF,tuneF,scoreF):
        self.name = name
        self.tanhF = tanhF
        self.tuneF = tuneF #[nodes per loop, nRepeats, magnitude attenuation rate]
        self.scoreF = scoreF
    
    def run(self,times,measurements):
        eXs = runTrigF(self.tanhF,times)
        sco = score(eXs,measurements,self.scoreF)
        return(eXs,sco)
    


def tuneFilter(filt,xs,fitXs):
    repeats = 0
    totalRepeats = 0
    spawn = []
    bestFilt = filt
    loops = 0
    FsPer = filt.tuneF[0]
    maxRepeats = filt.tuneF[1]
    magS = filt.tuneF[2]
    while repeats < maxRepeats:
        spawn.clear()
        magnitude = 1000000/(loops*magS + (totalRepeats + repeats * 50) * magS**2 + 100000)
        for i in range(int(FsPer*(repeats+2)/2)):
            spawn.append(copy.deepcopy(bestFilt))
            spawn[i].name += i
            if i > 0:
                spawn[i].Cs = wibble(spawn[i].Cs,magnitude)
        bFilt = pickBestFilt(spawn,xs,fitXs)
        if int(bFilt.name) == int(bestFilt.name):
            print(repeats,magnitude)
            repeats += 1
            totalRepeats += 1
        else:
            repeats = 0
            bestFilt = bFilt
        loops += 1    
    return(bestFilt)
    

def pickBestFilt(filts,xs,fitXs): 
    scores = []
    times = np.arange(len(xs))
    for filt in filts:
        nxs = filt.run(xs)
        score = scoreFilt(nxs,xs,fitXs,filt.scoreF)
        scores.append(score)
    bestI = scores.index(max(scores))
    #time.sleep(.5)
    if random.randint(0,7) == 4:
        print("best score",max(scores))
        print("best Kalman filter run so far:")
        print(filts[bestI].Cs)
        filts[bestI].showSelf(xs)
        
    return(copy.deepcopy(filts[bestI]))


def scoreFilt(nxs,xs,fitXs,scoreF):
    xsCost = 1
    fitXsCost = 1
    if len(nxs) != len(xs) or len(nxs) != len(fitXs):
        print("error, mismatched lenght in score Filt")
        time.sleep(1)
    #znxs = zScoreL(nxs)
    znxs = nxs
    zxs = xs
    zfxs = fitXs
    for i in range(len(nxs)):
        nx = znxs[i]
        x = zxs[i]
        fx = zfxs[i]
        xsCost += ((nx - x)**2)**.5
        fitXsCost += ((nx - fx)**2)**.5
    
    score = 1/(scoreF[0]*xsCost + scoreF[1]*fitXsCost + 1)
    return(score)
        
    


 
def tuneFitt(fitter,xs):
    repeats = 0
    totalRepeats = 0
    spawn = []
    bestFitt = fitter
    loops = 0
    maxRepeats = fitter.tuneF[1]
    magS = fitter.tuneF[2]
    FsPer = fitter.tuneF[0]
    while repeats < maxRepeats:
        spawn.clear()
        magnitude = 1000000/(loops*magS + (totalRepeats + repeats * 50) * magS**2 + 100000)
        for i in range(int(FsPer*(repeats+2)/2)):
            spawn.append(copy.deepcopy(bestFitt))
            spawn[i].name += i
            if i > 0:
                spawn[i].tanhF = wibble(spawn[i].tanhF,magnitude)
        
        bFitt = pickBestFitter(spawn,xs)
        if int(bFitt.name) == int(bestFitt.name):
            if random.randint(0,10)==4:
                print(repeats,magnitude)
            repeats += 1
            totalRepeats += 1
        else:
            repeats = 0
            bestFitt = bFitt
        loops += 1
    
    return(bestFitt)



def pickBestFitter(fitters,xs): 
    scores = []
    times = np.arange(len(xs))
    for fitt in fitters:
        nxs,score = fitt.run(times,xs)
        scores.append(score)
    bestI = scores.index(max(scores))
    if random.randint(0,7) == 4:
        print("best score",max(scores))
        print("best fitter so far")
        showTrigF(fitters[bestI].tanhF,0,100)
    #print("best score",max(scores))
    #time.sleep(.5)
    return(copy.deepcopy(fitters[bestI]))
            

        

def wibble(lis,mag):
    newL = []
    for el in lis:
        newEl = el + el * random.randint(0,1) * mag - random.uniform(0,el) * (mag + .5)
        newL.append(newEl)
    return(newL)

            

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
     for x in xs:
         nx = 0
         for i in range(0,len(F)-2,3):
             nx += F[i] * math.tanh(F[i+1] * (x - F[i+2]))
         nxs.append(nx)
     #zScoreL(nxs)
     return(nxs)  

def runTrigF1(F,xs):
     nxs = []
     for x in xs:
         nx = 0
         for i in range(0,len(F)-5,6):
             nx += F[i] * math.tanh(F[i+1] * (x - F[i+2])) + F[i+3]/100 * math.sin(F[i+4] * (x - F[i+5])/1000)
         nxs.append(nx)
     return(nxs) 


def score(Xs,Ys,scoreF):
    '''
    Ys = zScoreL(Ys)
    meanX = stat.mean(Xs) 
    stdX = stat.stdev(Xs)
    if stdX == 0:
        return(0)
    zXs = []
    for x in Xs:
        zXs.append((x-meanX)/stdX) #if using xs get big speed boost by skipping
    '''
    zXs = Xs
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
                cov = getCov(zScoreL(zXs),zScoreL(Ys))
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
        cost += ((v1[i]-v2[i])**4)
    return(cost)

def showThF(F,mn,mx): #rng = (min,max)
    demoXs = []
    step = (mx-mn)/100
    current = mn
    for i in range(100):
        demoXs.append(current)
        current += step
    nxs = runThF(F,demoXs) 
    plt.scatter(demoXs,nxs)
    plt.show()

def showTrigF(F,mn,mx): #rng = (min,max)
    nxs = runTrigF(F,np.arange(100)) 
    #nxs = zScoreL(nxs)
    plt.scatter(np.arange(100),nxs)
    plt.show()


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

        