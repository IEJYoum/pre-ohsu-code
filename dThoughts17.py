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



NoPS = 7
NhCOMS = 5
NvCOMS = 2

CDsTEPcOEFF = 3





def main(trainingA,functions,cmd):  

    if cmd == 0.1:    #gens random VF HF and finds best OTOF and finds confidences
        answers = trainingA[:,-1]
        trA = trainingA[:, :-1]    
        VF = genRVF(trA)
        tA = runVF(trA,VF)  
        HF = genRHF(tA)
        compXs = runHF(tA,HF)
        OtOFs = genNR1to1F([10,400,20])
        xStatsL = getLStats(compXs)
        #print("xSatsL 0:",xStatsL)
        bestF,bestScore,nxs = findBestF(compXs,answers,OtOFs,xStatsL,[4])
        ranges,confidences = CD(copy.deepcopy(nxs),answers)
        print("CONFIDENCE DISTRIBUTION:")
        plt.step(ranges,confidences)
        plt.show()
        return(trA,VF,tA,HF,compXs,bestF,nxs,answers,ranges,confidences)

    if cmd == 0:    #gens random VF HF and finds best OTOF 
        answers = trainingA[:,-1]
        trA = trainingA[:, :-1]    
        VF = genRVF(trA)
        tA = runVF(trA,VF)  
        HF = genRHF(tA)
        compXs = runHF(tA,HF)
        print("\n\n\n\n\n\ninput data:")
        plt.scatter(compXs,answers)
        plt.show()
        OtOFs = genNR1to1F([10,100,20])
        xStatsL = getLStats(compXs)
        #print("xSatsL 0:",xStatsL)
        bestF,bestScore,nxs = findBestF(compXs,answers,OtOFs,xStatsL,[4])
        showF(bestF,xStatsL)
        return(trA,VF,tA,HF,compXs,bestF,nxs,answers)

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
        
    elif cmd == 2:
        rows,collumns = averageRC(trainingA)
        return(rows,collumns)
    
    elif cmd == 3: #Swaps out trainingA[:,-1] for functions 
      trA = trainingA[:, :-1]
      return(np.concatenate((trA,np.transpose(functions)),axis=1))
    
    elif cmd == 4.1: #inserts functions in trainingArray second to last column
        answers = trainingA[:,-1]
        trA = trainingA[:, :-1]
        try:
            return(np.concatenate((trA,np.transpose(functions),np.transpose([answers])),axis=1))
        except:
            try:
                return(np.concatenate((trA,functions,np.transpose([answers])),axis=1))            
            except:
                try:
                    return(np.concatenate((trA,np.transpose([functions]),np.transpose([answers])),axis = 1))
                except:
                    try:
                        return(np.concatenate((trA,[functions],np.transpose([answers])),axis = 1))
                    except:
                        print(trA)
                        print(functions)
                        print(answers)
                        print("ERROR -1")
                        print((trA,np.transpose([functions]),np.transpose([answers])))
                        time.sleep(1)
    elif cmd == 4: #inserts functions in first collumn
        try:
            return(np.concatenate((functions,trainingA),axis = 1))
        except:
            try:
                return(np.concatenate((np.transpose(functions),trainingA),axis = 1))
            except:                                  
                try:
                    return(np.concatenate(([functions],trainingA),axis = 1))
                except:
                    try:
                        return(np.concatenate((np.transpose([functions]),trainingA),axis = 1))
                    except:
                        print(trainingA)
                        print(functions)
                        print("ERROR -3")
                        print(np.transpose([functions]),trainingA)
                        time.sleep(1)
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
                           



    '''    
    elif cmd == 2: #runs all [VF HF bestF]s in functions and returns function predicting how frequently point was predicted accurately (correct side of means) by various function combinations, and a list of how frequently each node predicted accurately
        answers = trainingA[:,-1]
        trA = trainingA[:, :-1]
        tripFScores = []
        tripAccs = []
        tripPointsScores = []
        for trip in functions:
            VF = trip[0]
            tA = runVF(trA,VF)
            trAr,teAr,trAn,teAn = splitA(tA,answers,.75)                        
            HF = trip[1]
            trCXs = runHF(trAR,HF)
            xStatsL = getLStats(compXs)
            bestF = trip[2]
            nbestF,bestScore,nxs = findBestF(compXs,answers,[bestF],xStatsL,[4]) #use this line to tune functions to data. nbestf currently inactive
            tripFScores.append(bestScore)
            tripAccs.append()
    
    
 
        
    elif cmd == 1: #runs VF HF BF on data and finds CDs
        answers = trainingA[:,-1]
        trA = trainingA[:, :-1]
        VF = functions[0]
        tA = runVF(trA,VF)
        HF = functions[1]
        compXs = runHF(tA,HF)
        xStatsL = getLStats(compXs)
        #print("xSatsL 1:",xStatsL)
        bestF = functions[2]
        nbestF,bestScore,nxs = findBestF(compXs,answers,[bestF],xStatsL,[4])
        ranges,confidences = CD(copy.deepcopy(nxs),answers)
        nxStatsL = getLStats(nxs)
        return(trA,VF,tA,HF,compXs,bestF,nxs,answers,ranges,confidences,xStatsL,nxStatsL)        
    '''        
    


def averageRC(array):
    rowSums = []
    nRows = array.shape[0]
    nCols = array.shape[1]
    for i in range(nRows):        
        rowSums.append(sum(array[i])/nCols)
    
    tarray = np.transpose(array)
    colSums = []   
    for i in range(nCols): 
        colSums.append(sum(tarray[i])/nRows)           
    return(rowSums,colSums)
        
            
        



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
    



def genRHF(array):
    nCols = array.shape[1]
    HF = []
    command = random.randint(0,NhCOMS-1)
    HF.append(command)
    for i in range(nCols+1):
        HF.append(random.uniform(-1,1))
    
    HF.append(random.randint(0,array.shape[1]-1))
    return(HF)
        
def runHF(array,HF): #no point running this on list
    #print("running HF:",HF)
    out1D = []
    if HF[0] == 0:
        for NDP in array:
            ODP = 0
            nCols = array.shape[1]
            for i in range(nCols):
                ODP += NDP[i] * HF[i+1]
            out1D.append(ODP)
        return(out1D)
    elif HF[0] == 1:
        for NDP in array:
            ODP = 0
            nCols = array.shape[1]
            for i in range(nCols):
                ODP += NDP[i] * 10**HF[i+1]
            out1D.append(ODP)
        return(out1D)
    else:
        index = HF[-1]
        out1D = array[:,index]
        return(out1D)
        
        
def genRVF(array):
    #nRows = array.shape[0]
    VF = []
    command = random.randint(0,NvCOMS-1)
    VF.append(command)
    for i in range(4):
        VF.append(random.uniform(-1,1))
    return(VF)


def runVF(array,VF): #make compatiable with lists by removing k loop
    #print("running VF:",VF)
    outAL = []
    if VF[0] == 0:
        return(array)
    elif VF[0] == 1:
        print("running back function: bad fo xor should not run")
        nRows = array.shape[0]
        nCols = array.shape[1]
        for i in range(nRows):
            newRow = copy.copy(array[i])
            j = 1
            while i - j >= 0: 
                Srow = array[i - j]
                for k in range(nCols):
                    targetV = Srow[k]
                    newRow[k] += VF[1] * targetV /(j + 2)  + 2**VF[2] * math.cos(targetV/100**VF[3])
                    #print("incriment:",VF[1] * targetV /(j + 2)  + VF[2] * math.cos(targetV/100**VF[3]))
                j += 1
            outAL.append(newRow)        
        return(np.array(outAL))
        
                
        
    


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
    
    for i in range (len(lis)):
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

