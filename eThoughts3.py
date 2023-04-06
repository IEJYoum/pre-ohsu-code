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


#TRAINf = "2016 2017ABC_data.csv"
#TRAINf = "generatedDataNp.csv"
#TRAINf = "xorNP.csv"



NoPS = 6
NhCOMS = 5
NvCOMS = 1

CDsTEPcOEFF = 3





def main(trainingA,functions,cmd):  

    if cmd == 0.1:    #gens random VF HF and finds best OTOF and finds confidences
        answers = trainingA[:,-1]
        trA = trainingA[:, :-1]    
        VF = genRVF(trA)
        tA = runVF(trA,VF)  
        HF = genRHF(tA)
        compXs = runHF(tA,HF)
        OtOFs = genNR1to1F([1,400,20])
        xStatsL = getLStats(compXs)
        #print("xSatsL 0:",xStatsL)
        bestF,bestScore,nxs = findBestF(compXs,answers,OtOFs,xStatsL,[4])
        ranges,confidences = CD(copy.deepcopy(nxs),answers)
        print("CONFIDENCE DISTRIBUTION:")
        plt.step(ranges,confidences)
        plt.show()
        return(trA,VF,tA,HF,compXs,bestF,nxs,answers,ranges,confidences)

    if cmd == -2:    #gens HF with signal
        answers = trainingA[:,-1]
        trA = trainingA[:, :-1] 
        FGenL = functions[0]   
        ScoreL = functions[1]        
        colScores = scoreCols(trA,FGenL,ScoreL) 
        return(colScores)
    
    elif cmd == -1:
        answers = trainingA[:,-1]
        trA = trainingA[:, :-1]
        FGenL = functions[0]
        ScoreL = functions[1]
        colScores = functions[2]        
        bestHF = genHF(trA,FGenL,ScoreL,colScores) #make an open function for scoring and solve for the best function
        return(bestHF)
        
    elif cmd == 0:        
        answers = trainingA[:,-1]
        trA = trainingA[:, :-1]       
        FGenL = functions[0]
        ScoreL = functions[1]
        HF = functions[2]
        compXs = runHF
        xStatsL = getLStats(compXs)
        bestF,bestScore,nxs = findBestF(compXs,answers,OtOFs,xStatsL,[4])
        #showF(bestF,xStatsL)
        return(bestF,bestScore,nxs)

    elif cmd == 1: #evaluates each compX and returns list of how frequently x was predicted correctly and how well each node performed
        #measures how well each function learns the data and how well each datapoint can be learned
        answers = trainingA[:,-1]
        trA = trainingA[:, :-1]
        tripFScores = []
        tripPointsScores = []      
        tripGSs = []
        for trip in functions:
            VF = trip[0]
            tA = runVF(trA,VF)
            HF = trip[1]
            compXs = runHF(tA,HF)
            xStatsL = getLStats(compXs)
            bestF = trip[2]
            nbestF,bestScore,nxs = findBestF(compXs,answers,[bestF],xStatsL,[4]) #use this line to tune functions to data. nbestf currently inactive
            tripFScores.append(bestScore)
            nxStatsL = getLStats(nxs)
            scoreSheet = []
            guessSheet = []
            for i in range(len(nxs)):
                x = nxs[i]
                ans = answers[i]
                aStats = getLStats(answers)
                if evaluateSingleX(x,nxStatsL,0): 
                    guessSheet.append(1)
                    if ans > aStats[0]:
                        scoreSheet.append(1)
                    else:
                        scoreSheet.append(0)
                    
                elif not evaluateSingleX(x,nxStatsL,0): 
                    guessSheet.append(-1)
                    if ans <= aStats[0]:
                        scoreSheet.append(1)                  
                    else:
                        scoreSheet.append(0)
            tripPointsScores.append(scoreSheet)
            tripGSs.append(guessSheet)
        return(tripFScores,tripPointsScores,tripGSs)
        
    elif cmd == 5: #multiply vectors
        v1 = trainingA
        v2 = functions    
        try:
            return(np.multiply(v1,v2))
        except:
            try:
                #print("attempting to multimply transpose")
                return(np.multiply(np.transpose(v1),v2))
            
            except:
                try:
                    print("attempting to multimply inside brackets")
                    return(np.multiply([v1],v2))
                except:
                    try:
                        print("attempting to multimply brackets")
                        return(np.multiply(v1,[v2]))                
                    except:
                        print("ERROR")
                           
    elif cmd == 6: #find best transformation on array  nxm to 1xn-list by testing for signal
        answers = trainingA[:,-1]
        A = trainingA[:, :-1]
        bestScore = -9999
        bestOut1D = []
        
        for i in range(functions[0]):
            T = genNLin1to1F([2,1,2])[0]
            out1D = runAT(A,T)
            Fs = genNR1to1F([10,100,10])
            xStatsL = getLStats(out1D)
            F,score,NXs = findBestF(out1D,answers,Fs,xStatsL,[4])
            if score > bestScore:
                print("new Best Score! \nData after transformation (cmd6)\n\n")
                plt.scatter(out1D,answers)
                plt.show()                
                bestScore = score
                bestT = T
                bestOut1D = out1D
                showF(F,getLStats(NXs))
                plt.scatter(NXs,answers)
                plt.show()
                print("bestScore:",score,"\nnew best data (cmd6)\n\n\n\n\n\n")
        
        return(bestT,bestOut1D)
        
       
    

def runHF(A,T):
    data1D = []
    for row in A:
        lRow = len(row)
        newRow = []
        for i in range(lRow):
            elem = row[i] * T[i]
            newRow.append(elem)
        data1D.append(sum(newRow))
    return(data1D)
        

def genHF(trA,FGenL,ScoreL,colScores):
        

def scoreCols(A,FGenL,ScoreL):
    

def evaluateSingleX(x,xStatsL,method):
    mean = xStatsL[0]
    if method == 0:    
        if x > mean:
            return(True)
        else:
            return(False)
  

def CD(xs,answers):
    statsL = getLStats(xs)
    minX = statsL[2]
    maxX = statsL[3]
    exX = statsL[4]
    meanAnswer = stat.mean(answers)
    rng = maxX - minX
    lXs = len(xs)
    #step = rng / lXs * CDsTEPcOEFF
    #step = rng / 10
    step = rng / 5
    buckets = []
    bMins = []
    bucm = minX - exX/100
    while bucm <= maxX + exX/100:
        bucYs = []
        bMins.append(bucm)
        i = 0
        while i < lXs:
            x = xs[i]
            if x >= bucm and x < bucm + step:
                bucYs.append((answers[i]))
                i += 1
                #del xs[i]
                #del ansers[i] would need copy.deepcopy
                #lXs -= 1
            else:
                i += 1
        
        buckets.append(bucYs)
        bucm += step
    #print("buckets:",buckets)
    
    confidences = []
    for bucket in buckets:
        if len(bucket) > 1:
            meanY = stat.mean(bucket)
            stdY = stat.stdev(bucket)
            lY = len(bucket)
            confidences.append((meanY-meanAnswer)*lY/(stdY+1))
        else:
            confidences.append(0)
    
    
    scaledCs = scaleInteTo1(bMins,confidences)
    
    return(bMins,scaledCs)
                
        
    

def scaleInteTo1(xs,ys): #xs must be ordered
    #print("ys before scaling:",ys)
    integral = 0
    lXs = len(xs)
    for i in range(lXs-1):
        y = ys[i]
        ny = ys[i+1]
        integral += (((y+ny)**2)**.5 /2)
    nYs = []
    for y in ys:
        ny = y/integral
        nYs.append(ny)
    return(nYs)
    
 



def findBestF(xs,ys,Fs,xStatsL,fScoreL):
    bestF = []
    bestNXs = []
    bestScore = -9999
    for function in Fs:
        nxs = runF(xs,function,xStatsL)
        #Score(nxs,ys,xStatsL,[0])
        score = Score(nxs,ys,xStatsL,fScoreL)
        #score = Score(nxs,ys,xStatsL,[1]) * Score(nxs,ys,xStatsL,[4])
        if score > bestScore:
            #showF(function,xStatsL)
            bestScore = score
            bestF = function
            bestNXs = nxs
            #print("score:",score)    
    return(bestF,bestScore,bestNXs)



def getLStats(lis):
    statsL = []
    statsL.append(stat.mean(lis))
    statsL.append(stat.stdev(lis))
    statsL.append(min(lis))
    statsL.append(max(lis))
    statsL.append(max(min(lis)**2,max(lis)**2))
    return(statsL)
    
  



def genNR1to1F(genList): 
    nTerms = genList[0]
    N = genList[1]
    length = genList[2]
    newFs = []
    for j in range(N):
        function = []
        ops = []
        for j in range(length):
            ops.append(random.randint(0,NoPS-1))        
        for i in range(nTerms):
            term = copy.copy(ops)
            for j in range(length):
                term.append(10**random.uniform(-1,1)*random.randint(-1,1)) #weights                                          
            function.append(term)            
        newFs.append(function)
    return(newFs)


def runF(xs,F,xStatsL):
    meanX = xStatsL[0]
    stdX = xStatsL[1]
    nxs = []
    for x in xs:
        xVar = (x - meanX)/stdX
        #xVar = x
        newX = 0
        i = 0
        for term in F:          
            newX += runOps(xVar,term)
            np.seterr('warn')
            i += 1
        nxs.append(newX)
    #print("nxs",nxs,"\n")
    return(nxs)
    


def runOps(xVar,term):
    dNX = xVar
    lTerm = len(term)
    i = 0
    while i < lTerm-1:
        Op = term[i]
        weight = term[-(i+1)]
        
        if Op == 0:
            dNX = dNX * xVar 
       
        elif Op == 1:
            dNX = dNX * weight

        elif Op == 2:
            dNX = (dNX ** 2 + 1) ** (weight - 1)
        
        elif Op == 3:
            dNX = dNX * math.sin(xVar * weight)

        elif Op == 4:
            dNX = dNX * math.cos(xVar * weight)

        elif Op == 5:
            dNX += weight
      
        
        i += 1
    return(dNX)
            
    

def scaleLBySelf(lis):
    newLis = copy.copy(lis)
    extreme = max([max(lis)**2,min(lis)**2])**.5
    if extreme == 0:
        zeroLis = []
        for i in lis:
            zeroLis.append(0)
        return(zeroLis)
    lList = len(lis)
    for i in range(lList):
        newLis[i] = lis[i]/extreme
    return(newLis)


def Score(xs,ys,xStatsL,scoreF):   #feed in means and scaled lists from findBestF
    meanX = xStatsL[0]
    stdX = xStatsL[1]
    if scoreF[0] == 0:
        plt.scatter(xs,ys)
        plt.show()
        return(1)
    elif scoreF[0] == 1:
        sxs = scaleLBySelf(xs)
        sys = scaleLBySelf(ys)
        scArray = np.array([sxs,sys])
        covMat = np.cov(scArray)
        covariance = covMat[1,0]
        return(covariance)
    elif scoreF[0] == 2:  #this one is bad
        rTot = 0
        lTot = 0
        meanX = stat.mean(xs)
        for i in range(len(xs)):
            x = xs[i]
            y = ys[i]
            if x > meanX:
                rTot += y
            else:
                lTot += y        
        return(rTot - lTot)
    
    elif scoreF[0] == 3:
        score = 0
        sxs = scaleLBySelf(xs)
        meanX = stat.mean(sxs)
        for i in range(len(sxs)):
            x = sxs[i]
            distance = x - meanX
            y = ys[i]
            score += distance * y
        return(score)
    
    elif scoreF[0] == 4:
        score = 0
        sxs = scaleLBySelf(xs)
        sys = scaleLBySelf(ys)
        meanX = stat.mean(sxs)
        meanY = stat.mean(sys)
        for i in range(len(sxs)):
            x = sxs[i]
            xd = x - meanX
            y = sys[i]
            yd = y - meanY
            score += xd * yd
        return(score)
        
    elif scoreF[0] == 5:        
        score = 0
        for i in range(len(xs)):
            x = xs[i]
            y = ys[i]
            if x > meanX:
                score += y
            else:
                score -= y
        return(score)
                
    elif scoreF[0] == 5:        
        score = 0
        for i in range(len(xs)):
            x = xs[i]
            y = ys[i]
            if x > meanX:
                score += y
            else:
                score -= y
        return(score)                
        
    elif scoreF[0] == 6:  
        score = 0 
        print(xs)
        sxs = scaleLBySelf(xs)
        print(xs)
        print("\n")
        print(sxs)
        meanX = stat.mean(sxs)
        meanY = stat.mean(ys)
        print("\n")
        print("\n")
        print("means",meanX,meanY)
        i = 0
        for i in range(len(xs)):
            x = xs[i]
            y = ys[i]
            if x > meanX:
                score += (y - meanY)
            else:
                score -= (y - meanY)
        return(score) 

def showF(bestF,xStatsL):
    xs = []    
    i = xStatsL[2]
    rng = xStatsL[3] - i
    while i <= xStatsL[3]:
        xs.append(i)
        i += .01 * rng
    nxs = runF(xs,bestF,xStatsL)
    print("\n\nFUNCTION\n",bestF)
    plt.scatter(xs,nxs)
    plt.show()    


def inTime(maxTime,startTime):
    if time.time() < startTime + maxTime:
        return(True)
    else:
        return(False)    

