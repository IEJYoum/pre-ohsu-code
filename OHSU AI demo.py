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
import SFobjects3 as obj


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

TRAINf = "APPL 18 20.csv"
#TESTf = "APPL 18 20.csv"
#GAMEf = "APPL20 1 8.csv"
#TRAINf = "APPL20 1 8.csv"
#TESTf = "APPL20 1 8.csv"

#TRAINf = "NKE18 20.csv"
#TESTf = "NKEpresent.csv" #goes from 101 to 96
#TESTf = "NKE18 20.csv"
#TRAINf = "NKEpresent.csv"


#TRAINf = "parsedirisDataCopy.csv"
#GAMEf = "parsedirisDataGame.csv"




trainingA = np.loadtxt("data/"+TRAINf)
#testA = np.loadtxt("data/"+TESTf)




#tuneF: [nodes per loop,mRepeats*10,repeatFocus*10,scoreF,wiggleF]
#wiggleF: [min d100 roll to wiggle row, min roll for element,magFactor,ifactor,rfactor]
#scoreF[0,1,2,4] acc cor net stdev(zScore(nxs))

#0: [spawn and train nodes, n nodes, tuneF]
#1:


def main(trainingA):
    trainingA = zScoreA(trainingA.T).T
    startGate = obj.Gate(0,[[1,1,10,50,20,0,0,0,1,20,20,1,1,40]],[])
    nodes = startGate.processNodes([],trainingA)
    for node in nodes:
        node.showSelf(trainingA[:,:-1],trainingA[:,-1])



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


