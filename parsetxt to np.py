# -*- coding: utf-8 -*-
"""
Created on Fri Jul 17 17:05:52 2020

@author: Jalaa
"""

import math
import matplotlib.pyplot as plt
import random
import numpy as np
import time




INfILE = "abalone.csv"
OUTfILE = "abalone out.csv"


TsTEP = .1
VOLUMEfACTOR = .0001



def main(inFile):
    A = loadFile(inFile)
    np.savetxt(OUTfILE,A)







def loadFile(inFile):
    file = open(inFile, "r")
    parsedA = []
    for line in file:
        newLine = []
        sLine = line.split(",")
        for elem in sLine:
            try:
                newLine.append(float(elem))
            except:
                pass
        parsedA.append(newLine)
        
    file.close
    return(parsedA)


main(INfILE)    
    