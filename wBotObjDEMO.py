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
        for i in range(shape[0]):
            for j in range(shape[1]):
                for k in range(shape[2]):
                    mC = m[i,j,k]
                    wC = w[i,j,k]
                    if random.uniform(0,1.5) < m[i,j,k]:
                        rand = random.uniform(-1,1) 
                        rand2 = (rand**2)**.5
                        if mC < .94:
                            m[i,j,k] += .1*rand2/(mC + .1) 
                        else:
                            m[i,j,k] = .9                                                                              
                        t[i,j,k] = t[i,j,k] * (1 + w[i,j,k] * rand) + (rand/2)**5
                        w[i,j,k] = wC/2 + wC * (rand2 + m[i,j,k]/10)
                        w[i,j,k] = max(w[i,j,k],.01)

                    else:  
                        if  mC > .1:
                            m[i,j,k] -= .05
                            w[i,j,k] = wC * .9
                            if wC < .0001:
                                w[i,j,k] = .1
                        else:
                            m[i,j,k] = .2 

        returns = [t,w,m]
        return(returns)        
                    


   