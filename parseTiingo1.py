    # -*- coding: utf-8 -*-
"""
Created on Fri Jul 17 17:05:52 2020

@author: Jalaa
"""

import math
import matplotlib.pyplot as plt
import random
import pandas as pd
import numpy as np
import time
import datetime



class Day():
    def __init__(self,position,opn,high,low,close,volume,rnge,recentHigh,recentLow,recentNet,recentVolume,net,pnet,pvolume,nnet):
        self.position = position # 0
        self.opn = opn # 1
        self.high = high # 2
        self.low = low # 3
        self.close = close # 4
        self.volume = volume # 5
        self.rnge = rnge # 6
        self.net = net #7
        self.nnet = nnet

DAYS = []
LISTS = []



VOLUMEfACTOR = .00001
NETfACTOR = 1
RANGEfACTOR = 100



def main(dataframe):
    DAYS.clear()
    LISTS.clear()
    readData(dataframe)
    updateAttributes()
    makeLists()
    return(np.array(LISTS))

    
    

def makeLists():
    for day in DAYS:
        a = [day.opn,day.high,day.low,day.close, day.volume,day.rnge,day.net,day.nnet]
        #print("day:",a)
        #time.sleep(.1)
        LISTS.append(a)
    #print("sample day:", a)
 
    
def updateAttributes():
    index = 0
    while index < len(DAYS) - 1:
        day = DAYS[index]
        day.nnet = DAYS[index + 1].net
        index += 1
        #print("day.nnet:",day.nnet)





def readData(dataframe):
    array = dataframe.to_numpy()
    for line in array:
        #print(line[0],line[1],type(line[0]),line[2],line[3])
        if isinstance(line[0], datetime.date):
            i = 1
        else:
            i = 2
        day = Day(0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)
        attributes = []
        while i < 7:                
            attributes.append(line[i])
            i += 1

            #isinstance(float,var):                
        
        day.position = len(DAYS)
        day.opn = attributes[3]
        day.high = attributes[1]
        day.low = attributes[2]
        day.close = attributes[0]
        day.volume = attributes[4] * VOLUMEfACTOR
        day.net =  (day.close - day.opn) * NETfACTOR
        #print("opn,close,net",day.opn,day.close,day.net)
        #time.sleep(0.1)
        day.rnge = (day.high - day.low) * RANGEfACTOR
        DAYS.append(day)                     
    


#main("agq stock prices small.txt")    
    