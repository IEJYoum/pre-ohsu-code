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




#TRAINf = "A data.csv" #ten layers, some noise some linear some hard
#TESTf = "A data.csv"
#TRAINf = "F data.csv" #hard
#TESTf = "F data.csv"
#TRAINf = "parsedirisDataCopy.csv"
#TRAINf = "APPL20 1 8.csv"
TRAINf = "RetractCurve.csv"

trainingA = np.loadtxt("data/"+TRAINf)  

'''
NfEATURES = 10
NpOINTS = 10
trainingA = []
for i in range(NfEATURES):
    newRow = []
    for j in range(NpOINTS):
        newRow.append(i+j + random.uniform(-(i+j),i+j+1)/(i+1))
    trainingA.append(newRow)
trainingA = np.array(trainingA)
print(trainingA)
'''
    

NnODES = 1
WIGGLESpERnODE = 25
TUNErEPEATS = 8 #n times in a row must find same node in tuning before selecting
TUNEf = [0,0,1,1,1,1]

thTERMS = 10 #Tanh function terms. High terms allows for much more intricate patterns, slower runtime

def main(trainingA):
    startThF = []
    for i in range(thTERMS):
        startThF.append([random.uniform(-1,1),random.uniform(-1,1),random.uniform(-1,1)])
    
    #startNode = obj.Node(0,[10,20,100],np.ones(trainingA.shape[1]-1),startThF,[])
    startNode = obj.Node(0,99,np.ones(trainingA.shape[1]-1),startThF,[])
    
    zA = zScoreA(trainingA.T).T
    ans = zA[:,-1]
    wiggleF = [.1,10,.05] # ([0] + 1/(i + [1])**[2])
    goodNodes = []
    for i in range(NnODES):
        goodNodes.append(tuneNode(startNode,zA,ans,wiggleF,WIGGLESpERnODE,TUNEf))
    '''
    gate = obj.Gate(0,[1],1)
    bestNodes,bnxsA = gate.pickNodes(goodNodes,zA)
    print("data before transformation:")
    plt.scatter(zA[:,0],zA[:,-1])
    plt.show()
    for node in bestNodes:
        node.showSelf()
        nxs = node.runSelf1(zA[:,:-1])
        plt.scatter(nxs,ans)
        plt.show()
    '''

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
        #plt.scatter(np.arange(len(startNode.linF)),startNode.linF)
        #np.show()
        obj.showThF(startNode.thF)
        print("acc:",obj.getAcc(goodnxs,ans)*2)#,"net",obj.getNet(goodnxs,trainingA[:,-1]))
        plt.scatter(goodnxs,ans)
        plt.show()
        print(startNode.name,"\n\n")
        #print(startNode.name,"\ntimeF",startNode.timeF,"\nlinF",startNode.linF,"\nthF",startNode.thF)
            
    return(startNode)
    



def wiggleNode(oldNode,f,i): #steps of size 1/(1+i)^rate
    node = copy.deepcopy(oldNode)
    for linT in range(len(node.linF)): 
        pass   # !!!!!!!!!!!!!!!!!!!!!! CURRENTLY NOT WIGGLING LIN             
        node.linF[linT] += random.uniform(-2,2) * node.linF[linT] * (f[0] + 1/(i+f[1])**f[2]) * random.randint(0,1)
    for k in range(len(node.thF)):
        for j in range(len(node.thF[0])):                      
            node.thF[k][j] += random.uniform(-2,2) * node.thF[k][j] * (f[0] + 1/(i+f[1])**f[2]) * random.randint(0,1)
    if type(node.timeF) == list:        
        for k in range(len(node.timeF)):                        
            node.timeF[k]  += random.uniform(-2,2) * node.timeF[k]  * (f[0] + 1/(i+f[1])**f[2]) * random.randint(0,1)
    return(node)




def randomWi(node,rnge):
    for i in range(len(node.linF)):
        node.linF[i] += random.uniform(-rnge,rnge)
    for i in range(len(node.thF)):
        for j in range(len(node.thF[0])):
            node.thF[i][j] += random.uniform(-rnge,rnge)
    
    if type(node.timeF) == list:
        for i in range(len(node.timeF)):
            node.timeF[i] += random.uniform(-rnge,rnge)
    return(node)
        

def scaledWi(node,rnge):
    for i in range(len(node.linF)):
        node.linF[i] += random.uniform(-rnge,rnge) * node.linF[i]
    for i in range(len(node.thF)):
        for j in range(len(node.thF[0])):
            node.thF[i][j] += random.uniform(-rnge,rnge) * node.thF[i][j]    
    if type(node.timeF) == list:
        for i in range(len(node.timeF)):
            node.timeF[i] += random.uniform(-rnge,rnge) * node.timeF[i]
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


main(trainingA)





#needs tanhF for slow things and linear fs for fast things. 


