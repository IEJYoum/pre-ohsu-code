# -*- coding: utf-8 -*-
"""
Created on Mon Aug 10 06:13:48 2020

@author: Jalaa
"""

import numpy as np
import dThoughts17 as thought
import matplotlib.pyplot as plt
import random
import time


#TRAINf = "2018ABC_data.csv"
#TRAINf = "2016 2017ABC_data.csv"
#TRAINf = "generatedDataNp.csv"
#TRAINf = "xorNP.csv"
#TRAINf = "xorNP long.csv"
#TESTf = "xorNP.csv"
#GAMEf = "xorNP.csv"
#TRAINf = "parsedirisDataCopy.csv"
#TESTf = "parsedirisDataCopy.csv"
#TRAINf = "AMG18 20.csv"
#TRAINf = "O18 20.csv"
#TRAINf = "NKE18 20.csv"

TRAINf = "A data.csv"
#TRAINf = "B data.csv"
#TRAINf = "C data.csv" #cosine thing
#TRAINf = "D data.csv" #noise
#TRAINf = "E data.csv"
#TRAINf = "F data.csv" #hard

#TRAINf = "O20 7 8.csv"
#TESTf = "O20 1 8.csv"
#GAMEf = "O20 7 8.csv"

#TRAINf = "O18 20.csv"
#TESTf = "O18 20.csv"
#GAMEf = "O20 1 8.csv"


#TRAINf = "parsedirisDataCopy.csv"
#TESTf = "parsedirisDataCopy.csv"
#GAMEf = "parsedirisDataGame.csv"



'''
TRAINf = "O18 20.csv"
TESTf = "O20 1 8.csv"
market = Market('O')
trainingA = parse.main(market.getPrices('2018-1-1','2020-1-1'))
testA = parse.main(market.getPrices('2020-1-2','2020-8-1'))
np.savetxt(TRAINf,trainingA)
np.savetxt(TESTf,testA)
'''

PATHS = []
NlOOPS = 2
NpATHS = 2

NoUTSIDEbUCKETS = 0

class Node():
    def __init__ (self,name,dims,inp,nodeF,out,score):
        self.name = name
        self.dims = dims
        self.inp = inp
        self.nodeF = nodeF
        self.out = out
        self.score = score


trainingA = np.loadtxt(TRAINf)
#testA = np.loadtxt(TESTf)


a  = "ding"  

class Path():
    def __init__(self,nodes,ranges,CDs,acc):
        self.nodes = nodes
        self.ranges = ranges
        self.CDs = CDs
        self.acc = acc
        

def main():
    newA = trainingA
    for i in range(NlOOPS):
        newA = modifyAByPaths(newA)
    for i in range(5):
        print(newA[i])
    for i in range(5):
        print(newA[-i])   
    

def modifyAByPaths(array):
    #make oldpaths to keep them
    PATHS.clear()
    spawnStartPaths(array)      
    trips = makeFTrips()
    tripFScores,scoreSheets,tripGSs = thought.main(array,trips,1)

    nodeAccs, pointAccs = thought.main(np.array(scoreSheets),0,2)
    print("nodeAccs:",nodeAccs)
    for i in range(len(nodeAccs)):
        acc = nodeAccs[i]
        if acc < .53:
            nodeAccs[i] = 0
    tripGSs = thought.main(tripGSs,nodeAccs,5) #let functions take care of these transformations
    tripGSs = thought.main(tripGSs,pointAccs,5)
    junk,pointTotals = thought.main(tripGSs,0,2)
    #print(tripGSs,"tripGSs")
    print("pointTotals:",pointTotals)
    #print(pointAccs)
    newA = array
    #newA = thought.main(trainingA,np.array([pointAccs]),4)
    nnA = thought.main(newA,pointTotals,4)
    print("nnA[0]",nnA[0])
    return(nnA)
    

def makeFTrips():
    trips = []
    for path in PATHS:
        trip = []
        for node in path.nodes:
            trip.append(node.nodeF)
        trips.append(trip)
    return(trips)


def spawnStartPaths(array):
    for i in range(NpATHS):
        path = makePath(array)
        PATHS.append(path)


def makePath(array):
    trA,VF,tA,HF,compXs,bestF,nxs,answers = thought.main(array,0,0)    
    #thought.showF(bestF,thought.getLStats(compXs))
    nodes = []
    n = "nDarray"
    verNode = Node(0,[n,n],trA,VF,tA,0)
    nodes.append(verNode)
    horNode = Node(1,[n,1],tA,HF,compXs,0)
    nodes.append(horNode)
    nNode = Node(2,[1,1],compXs,bestF,nxs,0)
    #xStatsL = thought.getLStats(compXs)
    #thought.showF(bestF,xStatsL)
    nodes.append(nNode)
    path = Path(nodes,0,0,0)
    print("Path After Transformation:")
    plt.scatter(nxs,answers)
    plt.show() 
    return(path)
    
def plotCDs():
    for path in PATHS:
        for node in path.nodes:
            pass
            #print(node.name,"\n",node.dims,"\n",node.inp,"\n",node.nodeF,"\n",node.out,"\n",node.score,"\n\n\n\n")
        ranges = path.ranges
        CDs = path.CDs
        plt.scatter(ranges,CDs)
        plt.show()


main()   
    