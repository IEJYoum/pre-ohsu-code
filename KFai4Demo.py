# -*- coding: utf-8 -*-
"""
Created on Sun Dec  6 18:10:10 2020

@author: Jalaa
"""

import random
import numpy as np
import time
import matplotlib.pyplot as plt 
import math
import statistics as stat
import copy
import KFObjects4 as obj

def main():
    data = generateData(3) #nDims
    #print(data)
    xs = np.array(data)[:,-1]
    times = np.arange(len(xs))
    plt.plot(times,xs)
    plt.show()
    fitter = obj.Fitter(0,randTrigF(7),[10,10,200],[1,2]) #[nodes per loop, nRepeats, magnitude attenuation rate]
    fitter = obj.tuneFitt(fitter,xs)
    #print(fitter.tanhF)
    plt.plot(times,obj.zScoreL(xs))
    obj.showTrigF(fitter.tanhF,min(times),max(times))

    nxs,sco = fitter.run(np.arange(100),xs)  
    plt.plot(obj.zScoreL(xs),obj.zScoreL(nxs))

        
    
      
    
def generateData(dims):
    data = []
    function = [random.uniform(-1,1),random.uniform(-2,2),random.uniform(-1,1)]
    noise = random.uniform(0,1)
    cent = random.randint(-100,100)
    for i in range(100):
        x = []
        term = 0
        for j in range(dims):
            #term = function[0] * (i+1)**(2*function[1])  + term + (i+1) ** function[1] + term * function[0]*math.cos(i * term) + random.uniform(-1,noise) * term / (1+j)
            term = function[0] * (i-function[1]*cent)**2 + random.randint(1,1000) * math.cos(term * i / cent) + term * function[2] + i/function[2]
            x.append(term)
        data.append(x)
    print(np.array(data).shape)
    return(data)
      
def randTrigF(terms):
    thF = []
    for i in range(terms * 6):
        thF.append(random.uniform(-2,2))
    return(thF)

        
def randThF(terms):
    thF = []
    for i in range(terms * 3):
        thF.append(random.uniform(-2,2))
    return(thF)

main()