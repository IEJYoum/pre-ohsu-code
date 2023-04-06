# -*- coding: utf-8 -*-
"""
Created on Mon Jan 18 17:59:17 2021

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
import kFilter as Filter



DATA = np.loadtxt("data\RetractCurve.txt")

def main():
    weights = getWeights()
    predictions = Filter.getPredictions(DATA,weights)
   
    for i in range(DATA.shape[1]):
        plt.plot(DATA[:,i])
        plt.plot(predictions[:,i])
        plt.show()
        plt.scatter(DATA[:,i],predictions[:,i])
        plt.show()
        

def getWeights():
    return([0,0,1])    
    
main()