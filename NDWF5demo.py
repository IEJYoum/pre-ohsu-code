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
import NDFWobjects5 as obj


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


TRAINf = "parsedirisDataCopy.csv"
TESTf = "parsedirisDataGame.csv"
#GAMEf = "parsedirisDataGame.csv"




trainingA = np.loadtxt("data/"+TRAINf)
testA = np.loadtxt("data/"+TESTf)

    
def main(trainingA):
    node = obj.Node(0,[.1,10],[1,-1],[[1,1,1],[-1,3,1]],[])
    ans = zScoreL(trainingA[:,-1])
    nxs,score = node.runSelf(trainingA[:,:-1],ans,[0])
    obj.showThF([[1,1,1],[-1,2,1]])
    plt.scatter(nxs,trainingA[:,-1])
    plt.show()
    print(score)
    


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

    
main(trainingA)





#needs tanhF for slow things and linear fs for fast things. 


