# -*- coding: utf-8 -*-
"""
Created on Thu Aug  6 02:20:33 2020

@author: Jalaa
"""

import random
import numpy as np
import time
import matplotlib.pyplot as plt 
import math
import statistics as stat
import copy


import parseTiingo as parse
from tiingo import Market

#TRAINf = "diabetes out.csv"
#TESTf = "diabetes 2.csv"
#TRAINf = "wine out.csv"
#TESTf = "wine out.csv"
#TRAINf = "abalone out.csv"
#TESTf = "abalone out.csv"


#TRAINf = "aTRuner9 700.csv"
#TESTf = "aTRuner9 100.csv"

#TRAINf = "xorNP.csv"
#TESTf = "xorNP.csv"

#TRAINf = "A data.csv" #ten layers, some noise some linear some hard
#TESTf = "A data.csv"

#TRAINf = "B data.csv"
#TESTf = "B data.csv"

#TRAINf = "C data.csv" 
#TESTf = "C data.csv" 

#TRAINf = "D data.csv" #noise
#TESTf = "D data.csv"

#TRAINf = "E data.csv"
#TESTf = "E data.csv"


#TRAINf = "F data.csv" #hard
#TESTf = "F data.csv"

#TRAINf = "2016 2017ABC_data.csv"  
#TESTf = "2018ABC_data.csv"   #all of this set is about one month of data

#TRAINf = "AMG18 20.csv"
#TESTf = "AMGpresent.csv" # 85 to 68

#TRAINf = "NKE18 20.csv"
#TESTf = "NKEpresent.csv" #goes from 101 to 96
#TESTf = "NKE18 20.csv"
#TRAINf = "NKEpresent.csv"

#TRAINf = "O18 20.csv" 
#TESTf = "O20 1 8.csv" #goes from 73 to 60
#TRAINf = "O20 1 8.csv" 

#TRAINf = "2016 2017GILD_data.csv"
#TESTf = "2018GILD_data.csv" #very short, 72 to 79
#TRAINf = "2018GILD_data.csv"
#TRAINf = "2016 2017GIS_data.csv"
#TESTf = "2018GIS_data.csv"
#TRAINf = "2016 2017GLW_data.csv" #3.2 to 2.9
#TESTf = "2018GLW_data.csv"
#TRAINf = "2016 2017GM_data.csv"
#TESTf = "2018GM_data.csv"
#TRAINf = "2016 2017GOOG_data.csv"
#TESTf = "2018GOOG_data.csv"   #108 to 104

#TRAINf = "APPL 18 20.csv"
#TESTf = "APPL 18 20.csv"
#GAMEf = "APPL20 1 8.csv"
#TRAINf = "APPL20 1 8.csv"
#TESTf = "APPL20 1 8.csv"

TRAINf = "parsedirisDataCopy.csv"
TESTf = "parsedirisDataGame.csv"
#GAMEf = "parsedirisDataGame.csv"

#TRAINf = "NYT19 jun20.csv"
#TESTf = "NYT20 jun sep.csv"
#TRAINf = "GOOG19 jun20.csv"
#TESTf = "GOOG20 jun sep.csv"
#TRAINf = "GOOG20 jul jun.csv"
#TESTf = "GOOG20 jun sep.csv"
#TRAINf = "M20 jul jun.csv"
#TESTf = "M20 jun sep.csv"
#TRAINf = "AGQ20 aug20.csv"
#TESTf = "AGQ aug sep.csv"
#TRAINf = "TCEHY20 aug20.csv"
#TESTf = "TCEHY aug sep.csv"
#TRAINf = "TCEHY april19 april20.csv"
#TESTf = "TCEHY april sep.csv"
#TRAINf = "NYT april19 april20.csv"
#TESTf = "NYT april sep.csv"

trainingA = np.loadtxt(TRAINf)
testA = np.loadtxt(TESTf)

'''
TRAINf = "NYT april19 april20.csv"
TESTf = "NYT april sep.csv"
market = Market('NYT')
trainingA = parse.main(market.getPrices('2019-4-1','2020-4-1'))
testA = parse.main(market.getPrices('2020-4-2','2020-9-22'))
np.savetxt(TRAINf,trainingA)
np.savetxt(TESTf,testA)
'''

minBD = 2 #must be 2 or higher
maxBD = 3
BACKsTEP = 1
TUNElOOPS = 0   #include gap between nx and tuneloops. was finding huge profit when NX was 2 and ans wasn't adjusted to correct size in print functions (spefically buy low nike)
GAMEdAYS = 30
MINaCC = .09

PIClOOPS = 0

def main(trainingA):
    global testA
    global minBD
    global maxBD
    startT = time.time()
    if maxBD > trainingA.shape[0] or minBD > trainingA.shape[0]:
        minBD = -1
        maxBD = -1
    ans = trainingA[:,-1]          
    #zAns = ans
    tA = trainingA[:,:-1]
    TtA = tA.transpose()
    TzSA = zScoreA(TtA)
    TzSA = zeroOutliersA(TzSA,2.5) #anything outside n sds will = 0
    FsA,nxsA,Finfo = findColFs(TzSA,ans,7,5,100,TUNElOOPS,[0,1,3],-1) #findColFs(TzSA,zAns,terms,strtRng,tuneSteps,tunleLoops,scoreL,backDays):
    FsA = np.array(FsA)
    nxsA = np.array(nxsA)
    FinfoA = np.array(Finfo)
    for i in range(PIClOOPS):
        cFA,nxA,Finfo = findColFs(TzSA,ans,7,5,100,TUNElOOPS,[random.randint(0,3),random.randint(0,3)],-1)
        cFA = np.array(cFA)
        nxA = np.array(nxA)
        FsA = np.append(FsA,cFA,axis = 0)
        nxsA = np.append(nxsA,nxA,axis = 0)
        FinfoA = np.append(FinfoA,Finfo,axis = 0)
        
    for i in range(minBD,maxBD,BACKsTEP):
        cFA,nxA,Finfo = findColFs(TzSA,ans,7,5,50,TUNElOOPS,[1],i)
        cFA = np.array(cFA)
        nxA = np.array(nxA)
        FsA = np.append(FsA,cFA,axis = 0)
        padding = np.zeros((nxA.shape[0],i))
        nxA = np.append(padding,nxA,axis = 1)
        nxsA = np.append(nxsA,nxA,axis = 0)
        FinfoA = np.append(FinfoA,Finfo,axis = 0)

    ans = zScoreL(ans)
    s0 = scorenxsA(nxsA,ans,[0]) #gets acc for each bestF
    print("s0",s0)
    s1 = scorenxsA(nxsA,ans,[1])
    s2 = scorenxsA(nxsA,ans,[2])
    s3 = scorenxsA(nxsA,ans,[3])
    s4 = scorenxsA(nxsA,ans,[4]) 
    #scoreT = np.array([s0,s1,s2,s3,s4])
    print(len(testA))
    gameA = testA[-GAMEdAYS:]
    testA = testA[:-GAMEdAYS]
    print("gameA",len(gameA))
    print("testA",len(testA),"\nlengths above !")
    guessesA,FAccs = getGuesses(FsA,FinfoA,TtA,testA)
        
    scoreT = np.array([s0,s1,s2,s3,s4,FAccs])
    weights = makeFWeights(scoreT,[1,5])   #!!!!!!!!!!!!
    print("\n FWeights:",weights)
    netG = superposition1(np.array(guessesA),weights)
    print("net guesses:\n",netG,"\nnet g zsco:\n",zScoreL(netG),len(netG))
    testAns = testA.T[-1].tolist()
    print("answers:",testA.T[-1],len(testAns))
    guesses = netG
    print("net:",net(guesses,testA.T[-1]))
    print("acc:",acc(guesses,zScoreL(testA.T[-1]))/2+.5)  
    plt.scatter(netG,testA.T[-1])
    plt.show()
    grades = []
    for i in range(len(testAns)):
        an = testAns[i]
        guess = netG[i]
        if an * guess > 0:
            grades.append("X")
        elif an * guess == 0:
            grades.append("0")
        else:
            grades.append(" ")
    print("grades X correct:",grades)
    
    print("individual F accs:", FAccs,"sum:",sum(FAccs),"avg:",sum(FAccs)/len(FAccs))
    
    print("np.append(trainingA,testA).T[:-1]",np.append(trainingA,testA,axis = 0).T[:-1])
    
    
    goodFA = []
    goodFinfoA = []
    for i in range(len(FAccs)):
        if FAccs[i] > MINaCC:
            goodFA.append(FsA[i])
            goodFinfoA.append(FinfoA[i])
        if len(FAccs) != len(FsA):
            print("ERROR, mismatched FAcc and FsA lengths")
            time.sleep(10)
    print("good F infos:",goodFinfoA)
    FsA = goodFA
    FinfoA = goodFinfoA
    GguessesA,GFAccs = getGuesses(np.array(FsA),FinfoA,np.append(trainingA,testA,axis = 0).T[:-1],gameA)
    print(GFAccs,stat.mean(GFAccs))
    lastDayGuesses = np.array(GguessesA)[:,-1]
    print(lastDayGuesses,np.mean(lastDayGuesses))
    runTime = time.time()-startT
    print(runTime/60, " minute runtime")
    
def getGuesses(FsA,FinfoA,TtA,testA): #needs to see answers to make acc, c
    guessesA = []
    FAccs = []
    for i in range(FsA.shape[0]):
        F = FsA[i]
        index = FinfoA[i][0]
        backPoints = FinfoA[i][1]
        guesses = predict(F,TtA[index],testA.T[index],backPoints)
        guesses = zScoreL(guesses)
        #guesses = makeLBinary(guesses)        
        guessesA.append(guesses)        
        print("\nIndex,backPoints",index,backPoints)
        print("net:",net(guesses,testA.T[-1])) ########################################
        acc1 = acc(guesses,zScoreL(testA.T[-1]))
        print("acc:",acc1)
        FAccs.append(acc1)
    return(guessesA,FAccs)

def zeroOutliersA(A,nSDs):
    shape = A.shape
    newA = np.zeros(shape)
    for i in range(shape[0]):
        for j in range(shape[1]):
            if A[i,j] < nSDs and A[i][j] > -nSDs:
                newA[i,j] = A[i,j]
    return(newA)



def makeFWeights(scoreA,scoreL):
    weights = np.ones(scoreA.shape[1])
    for i in range(scoreA.shape[0]):
        for j in range(scoreA.shape[1]):
            if scoreA[i,j] < 0:
                scoreA[i,j] = 0
    #print(scoreA)
    for com in scoreL:
        weights = np.multiply(weights,scoreA[com])
        
    return(weights)
            
        
    
     
def findColFs(TzSA,ans,terms,strtRng,tuneSteps,tuneLoops,scoreL,backDays):
    if backDays > 1:
        zAns = zScoreL(ans[backDays:])
    else:
        zAns = zScoreL(ans)
    shape = TzSA.shape
    Fs = []
    nxsA = []
    Finfo = []
    for i in range(shape[0]):
        xs = TzSA[i]
        F = genThF(xs,zAns,terms,strtRng,tuneSteps,scoreL,backDays)
        F,nxs = tuneThF(F,xs,zAns,1,tuneSteps,scoreL,backDays,[1])
        F,nxs = tuneThF(F,xs,zAns,1,tuneSteps,scoreL,backDays,[2])
        F,nxs = tuneThF(F,xs,zAns,1,tuneSteps,scoreL,backDays,[0])
        for j in range(tuneLoops):
            F,nxs = tuneThF(F,xs,zAns,1/(j+2),tuneSteps/2,scoreL,backDays,[random.randint(0,2)]) #picks random col in fa to update
        Fs.append(F)
        nxsA.append(nxs)
        Finfo.append([i,backDays])
        print("col:",i,"bd:",backDays)
        showF1(F)
        plt.scatter(nxs,zAns)
        plt.show()
        print("\n\n\n")
    return(Fs,nxsA,Finfo)


def predict(F,trainingXs,teXs,backDays):    
    shape = testA.shape

    if backDays > 1:
        try:
            trXs = trainingXs[-backDays * 2:]
        except:
            print("invalid range for trXs")
    else:
        #print("UNLIMITED BACK DATA USED IN PREDICTIONS")
        trXs = trainingXs
        
    guesses = []
    for i in range(len(teXs)):
        trXs = np.append(trXs,teXs[i])
        trXs = trXs[1:]
        guess = guessPoint(trXs,F,backDays)
        guesses.append(guess)   
    return(guesses)





def guessPoint(trainXs,F,backDays):    
    zsXs = zScoreL(trainXs)
    nXs = runThF(F,zsXs,backDays)
    try:
        nxs = zScoreL(nXs)
        return(nxs[-1])
    except:
        print("error calculating zscore")
        return(0)

        
        
def superposition1(TzA,weights):
    shape = TzA.shape
    superXs = []
    nTzA = []
    for i in range(shape[0]):
        attributesR = TzA[i]
        weight = weights[i]
        newRow = []
        for elem in attributesR:
            newRow.append(elem*weight)
        nTzA.append(newRow)
    zA = np.array(nTzA).transpose()
    for row in zA:
        superXs.append(np.sum(row))
    return(superXs)


def superposition(zA):
    superXs = []
    for row in zA:
        superXs.append(np.sum(row))
    return(superXs)        


def makeLBinary(lis):
    for i in range(len(lis)):
        if lis[i] < 0:
            lis[i] = -1
        elif lis[i] > 0:
            lis[i] = 1
    return(lis)
             


def net(v1,v2): #v2 is answers
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

def cor(v1,v2):
    if len(v1) != len(v2):
        print("error mismatched comparison list length")
    score = 0
    for index in range(len(v1)):
        i = v1[index]
        j = v2[index]
        score += i * j
    return(score)
    
def acc(v1,v2):
    if len(v1) != len(v2):
        print("error mismatched comparison list length")
    total = 0
    correct = 0
    for index in range(len(v1)):
        i = v1[index]
        j = v2[index]
        if i > 0 and j > 0:
            correct += 1
        elif i < 0 and j < 0:
            correct += 1
        total += 1        
        
    return((correct/total - .5)*2)    



def zScoreL1(lis):
    try:
        mean = stat.mean(lis)
        sd = stat.stdev(lis)
        lLis = len(lis)
        nL = np.zeros(lLis)
        if sd == 0:
            return(nL)
        for i in range(lLis):
            nL[i] = (lis[i] - mean)/(sd + 0)
        return(nL)
    except:
        print("error calculating zScoreL")      
        lLis = len(lis)
        return(np.zeros(lLis))
        

def zScoreL(lis):
    mean = stat.mean(lis)
    sd = stat.stdev(lis) 
    lLis = len(lis)
    nL = np.zeros(lLis).tolist()
    if sd == 0:
        return(nL)
    for i in range(lLis):
        nL[i] = (lis[i] - mean)/(sd + 0.1)
    return(nL)

        


def zScoreA(TA): #by row
    shape = TA.shape
    nA = np.zeros(shape)
    i = 0
    for row in TA:       
        mean = stat.mean(row)
        sd = stat.stdev(row)
        for j in range(shape[1]):
            nA[i,j] = (TA[i,j] - mean)/(sd + 0)
        i += 1
    return(nA)



def genThF(xs,ans,N,tuneRange,tuneLoops,scoreL,backDays): #N terms
    F = []
    for i in range(N):
        term = [random.choice((-1,1)),random.uniform(-1,1),random.uniform(-2,2)] #coeff,multiplier,xOffset
        F.append(term)
    nF,nxs = tuneThF(F,xs,ans,tuneRange,tuneLoops,scoreL,backDays,[0,1,2])
    return(nF)
        

    
def tuneThF(F,xs,ans,tuneRange,tuneLoops,scoreL,backDays,indexL): #randomly updates every part of every term in f then tests
    tS = tuneRange/tuneLoops
    i = 0.001
    score,nxs = scoreThF(F,xs,ans,scoreL,backDays)
    print("ThF initial score:",score,indexL)
    bnxs = nxs
    while i < tuneRange:
        newF = copy.deepcopy(F)
        for j in range(len(F)):
            randRange = tuneRange - i
            for k in indexL:
                newF[j][k] = F[j][k] + F[j][k] * random.uniform(-randRange,randRange)
        nScore,nxs = scoreThF(newF,xs,ans,scoreL,backDays)
        if nScore > score:
            F = copy.deepcopy(newF)
            score = nScore
            #print("tuneFc:",score)
            bnxs = nxs
        i += tS
    return(F,bnxs)    
        
    
        
def runThF(F,xs,backDays):
     if backDays == -1:
         nxs = runThF1(F,xs)
         return(nxs)
     nxs = []
     lXs = len(xs)
     for i in range(backDays,lXs):                
         pastxs = []
         for j in range(backDays):
             pastxs.append(xs[i-j])
         x = zScoreL(pastxs)[0]
         nx = 0
         for term in F:
             nx += term[0] * math.tanh(term[1] * (x - term[2]))
         nxs.append(nx)
     nxs = zScoreL(nxs) 
     return(nxs)
     
     
def runThF1(F,xs):     
     nxs = []
     for x in xs:
         nx = 0
         for term in F:
             nx += term[0] * math.tanh(term[1] * (x - term[2]))
         nxs.append(nx)
     nxs = zScoreL(nxs) 
     return(nxs)     
    


def scorenxsA(nxsA,ans,scoreL):
    scores = []
    for nxs in nxsA:
        #nxs = zScoreL(nxs)
        #plt.scatter(nxs,ans)
        #plt.show()
        score = 1
        for com in scoreL:
            if com == 0:
                score = score * max(acc(nxs,ans),0)
            elif com == 1:
                score = score * max(net(nxs,ans),0)            
            elif com == 2:
                score = score * max(cor(nxs,ans),0)
            elif com == 3:
                score = score * max(net(ans,nxs),0)   
        scores.append(score)
    return(scores)
        

def scoreThF(F,xs,ans,scoreL,backDays):
    nxs = runThF(F,xs,backDays)
    score = 1
    for com in scoreL:
        if com == 0:
            score = score * max(acc(nxs,ans),0)
        elif com == 1:
            score = score * max(net(nxs,ans),0)            
        elif com == 2:
            score = score * max(cor(nxs,ans),0)
        elif com == 3:
            score = score * max(net(ans,nxs),0)   
        elif com == -1:
            score = score * -1
    return(score,nxs)



def trimL0s(lis):
    newLis = []
    for elem in lis:
        if elem != 0:
            newLis.append(elem)
    return(newLis)



def showF1(F):
    demoXs = []
    for i in range(-100,100):
        demoXs.append(i/30)
    nxs = runThF1(F,demoXs) 
    plt.scatter(demoXs,nxs)
    plt.show() 


def showF(F,backDays):
    demoXs = []
    for i in range(0,100):
        #demoXs.append((i/100)**2 * 3)
        demoXs.append(i/30)
    nxs = runThF(F,demoXs,backDays) 
    #print(len(demoXs[backDays+1:]),len(nxs))
    plt.scatter(demoXs[backDays+1:],nxs)
    plt.show()


    
main(trainingA)
