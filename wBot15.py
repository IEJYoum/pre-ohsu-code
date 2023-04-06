# -*- coding: utf-8 -*-
"""
Created on Mon Jan 11 02:43:06 2021

@author: Jalaa
"""

import math
import matplotlib.pyplot as plt
import random
import pandas as pd
import numpy as np
import time
import math
import DataObjects4 as obj
import statistics as stat
import copy


class Bot:
    def __init__(self,name,tensor,wiggler,memory):
        self.name = name
        self.tensor = tensor #A,B,Q,H,R
        self.wiggler = wiggler
        self.memory = memory
    
    def spawn(self,n):
        t = self.tensor
        w = self.wiggler
        if t.shape != w.shape:
            print("error mismatched shapes")
            print(t,"t")
            print(w,"w")
        wiggles = []
        wiggles.append(copy.deepcopy(self))
        for i in range(n):
            egg = copy.deepcopy(self)
            returns = egg.wiggle()
            egg.name = self.name + 1
            egg.tensor = returns[0]
            egg.wiggler = returns[1]
            egg.memory = returns[2]
            wiggles.append(egg)
        return(wiggles)

        
        
    def wiggle(self):
        t = self.tensor
        w = self.wiggler
        m = self.memory
        shape = t.shape
        #for i in range(shape[0]):
        i = 0
        for j in range(shape[1]):      
            for k in range(shape[2]):
                if k >= j:
                    tC = t[i,j,k]
                    mC = m[i,j,k] #measure of how many times this index has moved
                    wC = w[i,j,k] #measure of how large the last successful move was
                    if random.uniform(0,1) > .9:
                        m[i,j,k] +=1
                        rand = random.uniform(-1,1)
                        rand2 = rand**2
                        t[i,j,k] = t[i,j,k] * (1 + rand * wC) + wC
                        w[i,j,k] = wC * (1 + rand/(2*wC+1))
                    else:
                        w[i,j,k] = max(wC * ( random.uniform(.7,1) + .01/(wC**2 + .1)),.001)
                    
        returns = [t,w,m]
        return(returns)        


def rollMemory(m,tC,mC,wC,minHeat): #minheat 
    avgMoves = np.sum(m)/(m.shape[1]*m.shape[2]/2)
    #print(mC,avgMoves)
    heat = (mC/avgMoves + 1)*(wC + 1)
    #print(heat)   
    if heat == 1:
        return(False)
    elif random.uniform(0,heat) + .1/(heat+.1) > .5 + heat/2:
        return(True)
    else:
        return(False)
    

    


    def scaleWiggler(self,scaler):
        w = self.wiggler
        m = self.memory
        shape = w.shape
        for i in range(shape[0]):
            for j in range(shape[1]):
                for k in range(shape[2]): 
                    rand = random.uniform(0,2)
                    w[i,j,k] = w[i,j,k] * rand 
                    m[i,j,k] = m[i,j,k] * rand
        self.wiggler = w
                    


   