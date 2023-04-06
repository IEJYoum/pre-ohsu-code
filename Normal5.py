# -*- coding: utf-8 -*-
"""
Created on Mon Feb  8 17:32:03 2021

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


#TRAINf = "diabetes out.csv"
#TESTf = "diabetes 2.csv"
#TRAINf = "wine out.csv"
#TESTf = "wine out.csv"
#TRAINf = "abalone out.csv"
#TESTf = "abalone out.csv"

#TRAINf = "xorNP long.csv"
#TESTf = "xorNP.csv"

#TRAINf = "A data.csv" #ten layers, some noise some linear some hard
#TRAINf = "B data.csv"
#TRAINf = "C data.csv"  
#TRAINf = "D data.csv" #noise
#TRAINf = "E data.csv"
#TRAINf = "F data.csv" #hard

#TRAINf ="O18 20.csv"
#TESTf = "O20 1 8.csv"
#TRAINf ="MSFT april19 april20.csv"
#TESTf ="MSFT april sep.csv"
TRAINf ="M20 jul jun.csv"
TESTf ="M20 jun sep.csv"
#TRAINf = "NKE18 20.csv"
#TESTf = "NKEpresent.csv"
#TESTf = "GOOG19 jun20.csv"
#TRAINf = "2016 2017GOOG_data.csv"


#TRAINf = "parsedirisDataCopy.csv"
#TESTf = "parsedirisDataGame.csv"
#GAMEf = "parsedirisDataGame.csv"

#TRAINf = "parsedirisDataCopy.csv"
#TRAINf2 = "SN9processedDataGoog19.csv"
#TRAINf3 = "SN9processedDataGoog20.csv"
#TRAINf4 = "GOOG19 jun20.csv"


#TRAINf = "O18 20.csv"
#market = Market('NYT')
#trainingA = parse.main(market.getPrices('2020-4-19','2020-11-5'))
#np.savetxt(TRAINf,trainingA)


DATA = np.loadtxt("data/"+TRAINf)
testDATA = np.loadtxt("data/"+TESTf)
SHAPE = DATA.shape
startTime = time.time()
maxToShow = 3

def main():
    global DATA
    global testDATA
    global SHAPE
    '''
    #DATA = addDer()
    DATA = addDer()
    dataHolder = copy.deepcopy(DATA)
    DATA = testDATA
    SHAPE = testDATA.shape
    #DATA = addDer() #correct for 2 ders
    testDATA = addDer()
    DATA = dataHolder
    '''
    print(DATA[1],"\n\n",testDATA[2])
    thetas,scores = genThetas(30,[0],106) #(genSize,scoreF, selectionF)
    #thetas,scores = selectThetas(thetas,scores,100)
    shown = 0
    for theta in thetas:
        if shown < maxToShow:
            showTheta(testDATA[:,:-1],testDATA[:,-1],theta)
            shown += 1
    thetas,scores = selectThetas1(thetas,[2],0)
    print(scores)
    #print(sum(scores),"net")
    avg = sum(scores)/len(scores)
    print(avg,"average score")
    print("compared to a hold change of", testDATA[-1,-8] - testDATA[0,-8] )
    print(testDATA[0,:])
    print(avg/testDATA[0,-8] * 100,"percent in",testDATA.shape[0],"days from an initial investment of",testDATA[0,-8])
    print(avg/testDATA[0,-8] * 100 * 360/testDATA.shape[0], "percent a year")
    



def genThetas(genSize,scoreF,selectionF):
    Xs,Ys = randomFolds()
    thetas = findThetas(Xs,Ys)  
    scores = test(DATA,thetas,scoreF)
    for i in range(genSize):
        Xs,Ys = randomFolds()
        newThetas = findThetas(Xs,Ys)
        thetas = np.append(thetas,newThetas,axis=0)           
        newScores = test(DATA,newThetas,scoreF)
        scores = np.append(scores,newScores)                
    nScores = []
    while len(nScores) < 1:
        nThetas,nScores = selectThetas(thetas,scores,selectionF)
        selectionF = selectionF-1
    print("gen thatas elapsed time (m):", (time.time()-startTime)/60,"\n final selectionF",selectionF+1)
    return(nThetas,nScores)


"""
print("tr te correlation:",score(trScores,teScores,[0]))
    plt.scatter(trScores,teScores)
    plt.show()
    print("length v avgScore:",score(foldLengths,avgScores,[1]))
    plt.scatter(foldLengths,avgScores)
    plt.show()
"""

def selectThetas(thetas,scores,selectionF):
    if selectionF == 0: #all
        return(thetas,scores)
    elif selectionF == 1: #best
        scores = scores.tolist()
        return(np.array([thetas[scores.index(max(scores)),:]]),[max(scores)])
    else:
        medScore = stat.median(scores)
        goodT = []
        goodS = []
        for i in range(len(scores)):
            if scores[i] > medScore * selectionF / 100:
                goodT.append(thetas[i,:])
                goodS.append(scores[i])
        return(np.array(goodT),np.array(goodS))  
        
def selectThetas1(thetas,scoreF,selectionF): #runs on test data
    scores = test(testDATA,thetas,scoreF)
    if selectionF == 0: #all
        return(thetas,scores)
    elif selectionF == 1: #best
        scores = scores.tolist()
        return(np.array([thetas[scores.index(max(scores)),:]]),[max(scores)])
    else:
        medScore = stat.median(scores)
        goodT = []
        goodS = []
        for i in range(len(scores)):
            if scores[i] > medScore * selectionF / 100:
                goodT.append(thetas[i,:])
                goodS.append(scores[i])
        return(np.array(goodT),np.array(goodS))   

def test(dataA,thetas,scoreL):
    scores = []
    #print("\n\n",thetas)
    for theta in thetas:
        scores.append(score(np.matmul(dataA[:,:-1],theta),dataA[:,-1],scoreL))
    #showTheta(DATA[:,:-1],DATA[:,-1],thetas[scores.index(max(scores))])
    return(scores)




def addDer():
    newDATA = []
    for i in range(SHAPE[1]-1):
        dataCol = DATA[:,i]
        derCol = [0]
        for j in range(SHAPE[0]-1):
            derCol.append(dataCol[j+1] - dataCol[j])
        newDATA.append(derCol)
    newDATA = np.array(newDATA).T
    data = np.append(newDATA,DATA,axis = 1)
    return(data)
        
        
    


def findThetas(Xs,Ys):
    nFolds = len(Xs)
    thetas = []
    for i in range(nFolds):
        thetas.append(runNormal(Xs[i],Ys[i]))
        #showTheta(Xs[i],Ys[i],thetas[i]) 
    return(np.array(thetas))

  



def showTheta(X,ans,theta):
    print("\nTheta:\n",theta)
    Y = np.matmul(X,theta)
    plt.scatter(Y,ans)
    plt.show()
    plt.plot(zScoreL(ans))
    plt.plot(zScoreL(Y))
    plt.show()
    

def runNormal(X,Y):
    invx2 = np.linalg.inv(np.matmul(X.T,X))
    theta = np.matmul(np.matmul(invx2,X.T),Y)
    return(theta)


def randomFolds():
    size = random.randint(15,int(SHAPE[0]/4-1))
    cursor = 0
    Xs = []
    Ys = []
    while cursor < SHAPE[0]-size:
        x = (DATA[cursor:cursor+size,:-1])
        Xs.append(x)
        Ys.append(DATA[cursor:cursor+size,-1])       
        cursor += size
    return(Xs,Ys)


def zScoreL(L):
    lL = len(L)
    mean = stat.mean(L)
    sd = stat.stdev(L)
    nL = []
    for i in range(lL):
        nL.append((L[i]-mean)/sd)
    return(nL)

def score(Xs,Ys,scoreF):
    score = 1
    nScore = 1
    zXs = zScoreL(Xs)
    zYs = zScoreL(Ys)
    scores = [99,99,99,99]
    for com in scoreF:
        currentS = scores[com]
        if currentS == 99:
            if com == 0:
                acc = getAcc(Xs,Ys)
                #scores[0] = (acc-.5) * 100
                scores[0] = acc
            elif com == 1:
                cov = getCov(zXs,zYs)
                scores[1] = cov                          
            elif com == 2:
                net = getNet(zXs,Ys)
                scores[2] = net  
            elif com == 3:
                net = getNet(Ys,Xs)
                scores[3] = net
        
        if score < 0 and scores[com] < 0:
            score += scores[com]
        else:
            score *= scores[com]
        #nScore *= min(scores[com],-1) * -1    
    #return(score-nScore)
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
    #print("acc:",correct/total)    
    return(correct/total) 



main()