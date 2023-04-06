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
import DataObjects4 as obj
import statistics as stat
import copy


def main():
    data = np.loadtxt("data\RetractCurveClean.txt")
    shape = data.shape
    ansInd = 4
    Y = data[:,ansInd]
    X = np.delete(data,ansInd,1)
    x2i = np.linalg.inv(np.matmul(X.T,X))
    A = np.matmul(np.matmul(x2i,X.T),Y)
    print(A)
    outY = np.matmul(A,X.T)
    plt.plot(Y)
    plt.plot(outY)
    plt.show()
    kalmanFilter(X,Y,theta)
        



    
    
main()