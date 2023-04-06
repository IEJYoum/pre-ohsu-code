# -*- coding: utf-8 -*-
"""
Created on Fri Jul 17 17:05:52 2020

@author: Jalaa
"""

import math
import matplotlib.pyplot as plt
import random
import numpy as np





FILE = "A data.csv"

TsTEP = .1
DIMS = 10

def main():
    function = genfunction()
    data = makePoints(function)
    plot(data)
    npWrite(data)
    #print(data)
    
    
def npWrite(data):
    np.savetxt(FILE,np.array(data))


def write(data):
    xs = ""
    ys = ""
    for i in data:
        xs += str(i[0])
        xs += ","
        ys += str(i[1])
        ys += ","
    
    xs = xs[:-1]
    ys = ys[:-1]
    file = open(FILE,"w")
    file.write(xs)
    file.write('\n')
    file.write(ys)    
    file.close()


def genfunction():
    Fs = []
    for i in range(DIMS):
        Fs.append(random.randint(0,3))
    return(Fs)


def plot(data):
    xs = []
    ys = []
    for i in data:
        xs.append(i[0])
        ys.append(i[-1])
    plt.plot(xs,ys)
    


def makePoints(Fs):
    data = []
    t = 0
    twoPi = 2 * 3.14159
    while t < twoPi:
        data.append([t])
        t += TsTEP        
    
    for function in Fs:
        t = 0
        i = 0
        print(function)
        if function == 0:
            for i in range(len(data)):
                y = random.uniform(-1,1)                
                data[i].append(y)
                t += TsTEP
                i += 1
        elif function == 1:
            for i in range(len(data)):
                y = t + 2           
                data[i].append(y)
                t += TsTEP 
                i += 1
        elif function == 2:
            for i in range(len(data)):
                y = math.sin((t-1)*3) + t**(1.5-t/4) - t*5           
                data[i].append(y)
                t += TsTEP
                i += 1
        elif function == 3:
            for i in range(len(data)):
                y = (math.sin(t-1)+.5)**2 + (t+.2)**(-2) - t ** i
                print(y)             
                data[i].append(y)
                t += TsTEP 
                i += 1
         
    print("data",data)
    #for lis in data:
        #lis = lis.reverse()
    print("data",data)
    return(data)    


    
    
    
    
main()    