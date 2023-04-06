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
import NDFWobjects17demo as obj

import parseTiingo as parse
from tiingo import Market
import tickers as tick

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

#TRAINf = "NYT19 jun20.csv"
#TESTf = "NYT20 jun sep.csv"
#TRAINf = "GOOG19 jun20.csv"
#TRAINf = "GOOG20 jun sep.csv"
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

#TRAINf = "APPL 18 20.csv"
#TESTf = "APPL 18 20.csv"
#GAMEf = "APPL20 1 8.csv"
#TRAINf = "APPL20 1 8.csv"
#TESTf = "APPL20 1 8.csv"

#TRAINf = "NKE18 20.csv"
#TESTf = "NKEpresent.csv" #goes from 101 to 96
#TESTf = "NKE18 20.csv"
#TRAINf = "NKEpresent.csv"


#TRAINf = "parsedirisDataCopy.csv"
#TESTf = "parsedirisDataGame.csv"
#GAMEf = "parsedirisDataGame.csv"



'''
#TRAINf = "data/AMG to oct1.csv"
TRAINf = "data/NYT to oct1.csv"
trainingA = np.loadtxt(TRAINf)
'''
#TRAINf = "data/AAP to oct1.csv"
#np.savetxt(TRAINf,trainingA)


TUNErEPEATS = 4 #n times in a row must find same node in tuning before selecting

thTERMS = 3
TRAININGnODES = 100
NpTUNElOOP = 20
GATES = 2



def main():    
    global thTERMS
    global GATES
    while True:
        startTime = time.time()
        thTERMS = random.randint(1,5)
        #GATES = random.randint(2,3)
        try:
            ticker = tick.randomTicker()
            #ticker = "HBAN"
            market = Market(ticker)
            print("\n\n\nTICKER:", ticker, "\ntanh terms, gates:",thTERMS, GATES)
            trainingA = parse.main(market.getPrices('2020-1-1','2020-10-4'))
        except:
            print("\n\nerror loading trainingA")
            ticker = tick.randomTicker()
            market = Market(ticker)
            print("TICKER:", ticker)
            trainingA = parse.main(market.getPrices('2020-1-1','2020-10-4'))            
        TrALen = min(random.randint(60,200),trainingA.shape[0])
        #TrALen = trainingA.shape[0]
        print("trALen:",TrALen)
        trainingA = trainingA[-TrALen:]
        origA = trainingA
        testAs = []
        step = int(TrALen/(GATES+random.randint(1,5)))
        for i in range(GATES):
            testA = trainingA[-step:]
            trainingA = trainingA[:-step]
            testAs.append(testA)
        print("testA len:",testAs[0].shape[0])
        print("trainingA len:",len(trainingA))
        testAs.reverse()
        
        trainedNodes = trainNodes(trainingA)
        gate = obj.Gate(0,[2],2)
        goodNodes = trainedNodes
        
        for i in range(GATES):
            oldNodes = goodNodes
            if len(oldNodes) == 0:
                print("no nodes left")
                break
            print("\nGATE NUMBER:",i)
            goodNodes,goodnxs = gate.pickNodes(goodNodes,testAs[i])
            print(len(goodNodes)/len(oldNodes), "  fraction of nodes passing through gate")
            voteTotal = 0
            aye = 0
            nae = 0
            print("answer:",testAs[i][-1][-1])
            for j in range(len(goodnxs)):
                #print(zScoreL(goodnxs[j])[-1])
                voteTotal += zScoreL(goodnxs[j])[-1]
                if zScoreL(goodnxs[j])[-1] > 0:
                    aye += 1
                else:
                    nae += 1
            try:
                print("voteTotal,aye,nae:",voteTotal,aye,nae)
                print("weightedVote", voteTotal/(aye + nae))
                print("unweightedVote", (aye-nae)/(aye + nae))
            except:
                print("no good nodes left")
        if len(goodNodes) > 2:
            gate = obj.Gate(0,[1],1)
            bestNode,bestnxs = gate.pickNodes(goodNodes,origA)
            bN = bestNode[0]
            #bN.showSelf()
            print("best Node's prediction:",zScoreL(bestnxs[0])[-1])
        
        print("runtime:",(time.time()-startTime) /60)

        



def trainNodes(trainingA):
    tA = trainingA[:,:-1]
    ans = trainingA[:,-1]
    startThF = []
    for i in range(thTERMS):
        startThF.append([random.uniform(-1,1),random.uniform(-1,1),random.uniform(-1,1)])
    startNode = obj.Node(0,[10**random.randint(0,2),10**random.randint(0,2),10**random.randint(0,2)],np.ones(tA.shape[1]),startThF,[])
    wiggleF = [.001,3,.3] # 10*([0] + 1/(i + [1])**[2])
    trainedNodes = []
    for i in range(TRAININGnODES):
        tunedNode = tuneNode(startNode,tA,ans,wiggleF,NpTUNElOOP,[0,0,1])
        trainedNodes.append(tunedNode)
        '''
        plt.scatter(np.arange(len(tunedNode.linF)),tunedNode.linF)
        plt.show()
        obj.showThF(tunedNode.thF)
        print(tunedNode.timeF,"\n\n")
        '''
    return(trainedNodes)


def tuneNode(startNode,zA,ans,wiggleF,nPerLoop,scoreF):
    repeats = 0
    i = 0
    while repeats < TUNErEPEATS:
        i += 1
        nodes = [startNode]
        for j in range(nPerLoop):
            #node = wiggleNode(startNode,[[0,3*(LOOPS-i)/LOOPS]])
            node = wiggleNode(startNode,wiggleF,i)
            node.name = nodes[-1].name + 1
            nodes.append(node)
        gate = obj.Gate(0,scoreF,1)
        goodNode,goodnxs = gate.pickNodes(nodes,zA)
        if startNode.name == goodNode[0].name:
            repeats += 1
        else:
            repeats = 0
        startNode = goodNode[0]
        goodnxs = zScoreL(goodnxs[0])
        '''
        #plt.scatter(np.arange(len(startNode.linF)),startNode.linF)
        #np.show()
        obj.showThF(startNode.thF)
        print("acc:",obj.getAcc(goodnxs,ans),"net",obj.getNet(goodnxs,trainingA[:,-1]))
        plt.scatter(goodnxs,ans)
        plt.show()
        '''
        #print(startNode.name,"\ntimeF",startNode.timeF,"\nlinF",startNode.linF,"\nthF",startNode.thF)
         
    
    
    return(startNode)
    



def wiggleNode(oldNode,f,i): #steps of size 1/(1+i)^rate
    node = copy.deepcopy(oldNode)
    for linT in range(len(node.linF)):              
        node.linF[linT] += random.uniform(-2,2) * node.linF[linT] * 10*(f[0] + 1/(i+f[1])**f[2]) * random.randint(0,1)
    for k in range(len(node.thF)):
        for j in range(len(node.thF[0])):                      
            node.thF[k][j] += random.uniform(-2,2) * node.thF[k][j] * 10*(f[0] + 1/(i+f[1])**f[2]) * random.randint(0,1)
    if type(node.timeF) == list:        
        for k in range(len(node.timeF)):                        
            node.timeF[k]  += random.uniform(-2,2) * node.timeF[k]  * 10*(f[0] + 1/(i+f[1])**f[2]) * random.randint(0,1)
    return(node)



def zScoreL(lis):
    mean = stat.mean(lis)
    sd = stat.stdev(lis) 
    lLis = len(lis)
    nL = np.zeros(lLis).tolist()
    if sd == 0:
        sd  += .1
    for i in range(lLis):
        nL[i] = (lis[i] - mean)/sd
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


main()





#needs tanhF for slow things and linear fs for fast things. 


