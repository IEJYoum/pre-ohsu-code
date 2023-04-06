# -*- coding: utf-8 -*-
"""
Created on Wed Sep  9 19:17:44 2020

@author: Jalaa
"""

import random
import numpy as np
import time
import matplotlib.pyplot as plt 
import math
import statistics as stat
import copy

MINpOINTS = 10
CM = 5
NpATHS = 80

FRAMES = 6
ROWS = 20
COLS = 20



def main():
    pi = math.pi
    growF = [.5,0,-.1]
    ten = generateTunnelData(FRAMES,ROWS,COLS,4,5,growF) #nF,nR,nC,nshades,?    one in ? points of noise    
    #showTen(ten,-1)
    showTen(ten,[-1,-2,-3])
    showTen(ten,0)
    ansFrame,key = getAnsFrame(ten)
    ten = makePos(ten)
    #showTen(np.array([ansFrame,key]),1)
    #showTen(ten,"")
    #showTen(np.array([key]),1)
    allCents = genCents([1,ROWS-1],[1,COLS-1])
    aBoxesT = genBoxes(key,allCents)
    centScores = []
    for aBoxes in aBoxesT:
        bDist = boxProfile(aBoxes)
        #bDists.append(bDist)
        centScores.append(scoreDist(bDist,0,1))
    aCenter = allCents[centScores.index(max(centScores))]
    #aBoxes = genBoxes(ansFrame,[aCenter])[0]
    #aBProf = boxProfile(aBoxes)
    aPaths = genPaths(ansFrame,key,aCenter,NpATHS)
    aPProf = linProfile(aPaths)
    aComp = profToComp(aPProf)
    
    
    nearCents = genCents([aCenter[0]-CM,aCenter[0]+CM],[aCenter[1]-CM,aCenter[1]+CM])
    fCents = []
    fVecs = []
    fOutlines = []
    for frame in ten:
        binFrame = makeBinA(copy.deepcopy(frame),aComp,0,.1)
        fBoxesT = genBoxes(binFrame,nearCents)
        bCScores = []
        for boxes in fBoxesT:
            bFDist = boxProfile(boxes)
            bCScores.append(scoreDist(bFDist,0,1))
        fCent = nearCents[bCScores.index(max(bCScores))]
        fCents.append(fCent)
        #copyFrame = copy.deepcopy(frame)
        #copyFrame[fCent[0],fCent[1]] = 99
        #showTen(np.array([copyFrame]),"")
        if len(nearCents) != len(bCScores):
            print("error near cents not same as bcscores")
            time.sleep(1)
        fPaths = genPaths(frame,binFrame,fCent,NpATHS)
        goodPaths,goodInds = matchProf(fPaths,aPProf)
        for ind in goodInds:
            angle = (2*pi)/NpATHS * ind
            length = len(fPaths[ind])-1
            fVecs.append([angle,length])
        
        outline = traceVectors(frame,fCent,fVecs,9)
        fOutlines.append(outline)
    
    showTen(np.array(fOutlines),9)
        



def matchProf(paths,prof):
    inds = []
    cts = []
    nums = []
    freqs = []
    for dist in prof:
        inds.append(dist[0])
        cts.append(dist[1])
        ns = []
        fs = []
        for i in range(2,len(dist)-1,2):
            ns.append(dist[i])
            fs.append(dist[i+1])
        nums.append(ns)
        freqs.append(fs)
    
    goodPaths = []
    goodInds = []
    counter = 0
    for path in paths:
        match = 1
        endPoint = min(max(inds),len(path))
        for i in range(round(-len(path)/2),endPoint):
            if i not in inds:
                match = 0
                print("path index not in profiled indexes",print(i))
                break
            index = inds.index(i)
            ns = nums[index]
            if(path[i]) in ns:
                pass
            else:
                #print("bad path:",path)
                match = 0
        if match > 0:
            if 0 in path:
                print("good path containing 0:", path)
            goodPaths.append(path)
            goodInds.append(counter)
        counter += 1
        

    #print(len(paths),len(goodPaths),"\n paths,  goodpaths\n\n")
    return(goodPaths,goodInds)
            
        
    

def makeBinA(frame,aComp,command,Fs):
    shape = np.shape(frame)
    if command == 0:
        goodNums = []
        for i in range(len(aComp[0])):
            if aComp[1][i] / sum(aComp[1]) > Fs:
                goodNums.append(aComp[0][i])

        for i in range(shape[0]):
            for j in range(shape[1]):
                if frame[i,j] in goodNums:
                    frame[i,j] = 1
                else:
                    frame[i,j] = 0
        return(frame)
                

def profToComp(prof):
    nums = []
    counts = []
    for dist in prof:
        dCount = dist[1]
        for i in range(2,len(dist)-1,2):
            distN = dist[i]
            if distN not in nums:
                nums.append(distN)
                counts.append(dCount)
            else:
                counts[nums.index(distN)] += dCount
    return([nums,counts])
                
        

def scoreDist(dist,command,functions):
    score = 0
    sizes = []
    nums = []
    freqs = []
    for boxProf in dist:
        sizes.append(boxProf[0])
        numb = []
        freb = []
        for i in range(2,len(boxProf)-1,2):
            numb.append(boxProf[i])
            freb.append(boxProf[i+1])
        nums.append(numb)
        freqs.append(freb)
    if command == 0:  #functions is int, searches and adds frequency 
        for i in range(len(sizes)):
            sizeNums = nums[i]
            sizeFreqs = freqs[i]
            if functions in sizeNums:
                index = sizeNums.index(functions)
                freq = sizeFreqs[index]
                score += freq
            else:
                return(score)
        return(score)
 
def genCents(rowR,colR):
    cents = []
    for i in range(rowR[0],rowR[1]):
        for j in range(colR[0],colR[1]):
            cents.append([i,j])
    return(cents)



def boxProfile(boxes): #takes boxes for one center (3d array)
    dists = [] #size,#,%,#,%
    for box in boxes:
        if len(box) > 2:           
            size = round((len(box) + len(box[0]))/2)
            shades = []
            counts = []
            for row in box:
                lRow = len(row)
                for i in range(lRow):
                    if row[i] not in shades:
                        shades.append(row[i])
                        counts.append(1)
                    else:
                        counts[shades.index(row[i])] += 1
            dist = [size,sum(counts)]
            for i in range(len(counts)):
                dist.append(shades[i])
                dist.append(counts[i]/sum(counts))
            if len(dist) > 2:
                dists.append(dist)
    return(dists)
        
        


def linProfile(paths):
    dists = [] #[index,main#,%,next#,%next#,etc.]
    for index in range(4*len(paths[0])):
        index = index - len(paths[0])*2
        shades = []
        counts = []
        for path in paths:
            if index < len(path) and -index < len(path):
                if path[index] not in shades:
                    shades.append(path[index])
                    counts.append(1)
                else:
                    counts[shades.index(path[index])] += 1
        dist = [index,sum(counts)]
        if sum(counts) > MINpOINTS:
            for i in range(len(counts)):
                dist.append(shades[i])
                dist.append(counts[i]/sum(counts))
            if len(dist) > 2:
                dists.append(dist)
            #print(dist)
    return(dists)
        



def genPaths(A,key,center,nPaths):
    paths = []
    shape = np.shape(key)
    pi = math.pi
    for i in range(nPaths):
        angle = 2*pi/nPaths * i
        traj = makeTraj(angle,shape)
        path = []
        for coord in traj:
            coord[0] += center[0]
            coord[1] += center[1]
            if coord[0] < shape[0] and coord[0] > -1:
                aRow = A[coord[0]]
                kRow = key[coord[0]]
                if coord[1] < shape[1] and coord[1] > -1:
                    if kRow[coord[1]] == 1:
                        path.append(aRow[coord[1]])
        paths.append(path)
    return(paths)
    


       

    

def genBoxes(A,cents):
    boxesT = []
    shape = np.shape(A)
    for cent in cents:
        boxes = []
        for boxN in range(1,round((shape[0] + shape[1])/8)):
            box = []
            for i in range(-boxN,boxN):
                if cent[0] + i > -1 and cent[0] + i < shape[0]:
                    boxR = []
                    sourceR = A[cent[0]+i]
                    for j in range(-boxN,boxN):
                        if cent[1] + j > -1 and cent[1] + j < shape[1]:
                            boxR.append(sourceR[cent[1]+j])
                    if len(boxR) > 1:
                        box.append(boxR) #each box is a 2d array around a center
            boxes.append(box)  #each boxes contains data of all 2DA for one center                              
        boxesT.append(boxes)
    return(boxesT)
            
    


def makeTraj(angle,shape):
    traj = [[0,0]]
    for i in range(shape[1]+shape[0]):
        cursor = traj[-1]
        nex = [0,0]
        hStep = math.cos(angle) * i
        vStep = math.sin(angle) * i
        if hStep > 0 and hStep - cursor[1] > 1:
            nex[1] += 1
        elif hStep < 0 and hStep - cursor[1] < -1:
            nex[1] -= 1
        if vStep > 0 and vStep - cursor[0] > 1:
            nex[0] += 1
        elif vStep < 0 and vStep - cursor[0] < -1:
            nex[0] -= 1    
        nex[0] += cursor[0]
        nex[1] += cursor[1]
        traj.append(nex)

    #print(traj,"trajectory")
    return(traj)
        

def traceVectors(frame,startC,vecs,outShade):
    shape = np.shape(frame)
    blankF = np.zeros(shape)
    for vec in vecs:
        angle = vec[0]
        length = vec[1]
        coord = startC
        traceL = 0
        traj = makeTraj(angle,shape)
        for step in traj:
            coord = [startC[0]+step[0],startC[1] + step[1]]
            if coord[0] < shape[0] and coord[0] > -1 and coord[1] < shape[1] and coord[1] > -1:
                blankF[coord[0],coord[1]] = outShade
                traceL += 1
                if traceL >= length:
                    break
    return(blankF)
        
            
                
            
        
    



def generateTunnelData(x,y,z,shades,noise,growF):
    ten = np.zeros((x,y,z))
    ten = genNoise(ten,shades,noise)
    ten = genTun(ten,shades,growF)  
    ten = addSkin(ten)
    ten = addSkin(ten)
    return(ten)


        


def findMax(scoreA):
    rowMaxes = []
    for row in scoreA:
        rowMaxes.append(max(row))
    bestRi = rowMaxes.index(max(rowMaxes))
    lis = scoreA[bestRi].tolist()
    bestCi = lis.index(max(lis))
    return([bestRi,bestCi])
        


def makePos(ten):
    shape = np.shape(ten)
    pTen = copy.deepcopy(ten)
    for i in range(shape[0]):
        A = ten[i]
        for j in range(shape[1]):
            vec = A[j]
            for k in range(shape[2]):
                if vec[k] < 0:
                    pTen[i][j][k] = -vec[k]
    return(pTen)
                    


def addSkin(ten):
    shape = np.shape(ten)
    for A in ten:
        aMin = np.amin(A)
        if aMin < 0:
            sShade = aMin - 1
            for i in range(shape[1]-2):
                if i == 0:
                    i += 2
                vec = A[i]               
                for j in range(shape[2]-2):
                    if j == 0:
                        j += 2
                    if vec[j] == aMin  and random.randint(0,100) < 95:
                        if vec[j+1] >= 0:
                            vec[j+1] = sShade
                        if vec[j-1] >= 0:
                            vec[j-1] = sShade                       
                        if A[i+1][j] >= 0:
                            A[i+1][j] = sShade                
                        if A[i-1][j] >= 0:
                            A[i-1][j] = sShade
    return(ten)
                            
def genTun(ten,shades,growF):
    shape = ten.shape
    nFra = shape[0]    
    nRow = shape[1]
    nCol = shape[2]
    array0 = ten[0]
    startRow = random.randint(nRow/2 - 4,nRow/2 + 4)
    startCol = random.randint(nCol/2 - 4,nCol/2 + 4)
    array0[startRow,startCol] = -1
    array0[startRow+1,startCol] = -1
    
    for i in range(nFra):
        if i == 0:
            i += 1
        preA = ten[i-1]
        A = ten[i]
        coords = []
        for j in range(nRow):
            vec = preA[j]
            for k in range(nCol):
                elem = vec[k]
                if elem == -1:
                    coords.append([j,k])       
        
        for coord in coords:
            j = coord[0]
            k = coord[1]
            nAdj = countAdj(preA,coord,-1)
            if i < 3 or nAdj == 4:
                A[j,k] = -1                         
            if nAdj > 0:
                out = runPolyF(growF,i)
                if out > 0:
                    term = out/(5-nAdj)
                else:
                    term = out/(nAdj+1)
                if j + 1 < nRow and k + 1 < nCol and j - 1 > -1 and k - 1 > -1:
                    if random.uniform(-1,1) + term  > 0:
                        A[j+1,k] = -1
                    if random.uniform(-1,1) + term  > 0:
                        A[j,k+1] = -1                
                    if random.uniform(-1,1) + term  > 0:
                        A[j-1,k] = -1                
                    if random.uniform(-1,1) + term  > 0:
                        A[j,k-1] = -1                             
    return(ten)





def runPolyF(F,x):
    lenF = len(F)
    out = 0
    for i in range(lenF):
        coeff = F[i]
        out += coeff * x ** i
    #print("pollyF out:",out)
    return(out)
        
    

def genNoise(ten,shades,noise):    
    for mat in ten:
        for vec in mat:
            for i in range(len(vec)):
                if random.randint(1,noise) == 1:
                    vec[i] = random.randint(1,shades)
    return(ten)


def countAdj(A,coord,shade):
    nRow = A.shape[0]
    nCol = A.shape[1]
    j = coord[0]
    k = coord[1]
    nAdj = 0
    if j + 1 < nRow:
        if A[j+1,k] == shade:
            nAdj += 1
    else:
        nAdj += 1
    
    if k + 1 < nCol:
        if A[j,k+1] == shade:
            nAdj += 1
    else:
        nAdj += 1
    
    if j - 1 > -1:
        if A[j-1,k] == shade:
            nAdj += 1
    else:
        nAdj += 1
    
    if k - 1 > -1:
        if A[j,k-1] == shade:
            nAdj += 1
    else:
        nAdj += 1  

    return(nAdj)

'''
def Map(key):
    shape = np.shape(key)
    cursor = [0,0] #v,h
    centers = []
    scores = []
    while cursor[0] < shape[0]:
        cursor[1] = 0
        while cursor[1] < shape[1]:
            verz = 9
            horz = 9
            i = 1
            while verz > 2 and horz > 2:
                verz = shape[0]/4 - i
                horz = shape[1]/4 - i
                vEdge = cursor[0] + verz
                hEdge = cursor[1] + horz
                rown = cursor[0]
                coln = cursor[1]
                score = 0
                while rown < vEdge and rown < shape[0]:
                    row = key[rown]
                    while coln < hEdge and coln < shape[1]:
                        score += row[coln]
                        coln += 1
                    rown += 1
                centers.append([round(cursor[0]+verz/2),round(cursor[1]+horz/2)])
                scores.append(score**2/(verz*horz+1))
                i += 1
            cursor[1] += 1
        cursor[0] += 1
    #print(centers,scores)
    
    scoreMat = np.zeros(shape)
    entriesMat = np.zeros(shape)
    lScores = len(scores)
    for i in range(lScores):
        center = centers[i]
        score = scores[i]
        try:
            scoreMat[center[0],center[1]] += score
            entriesMat[center[0],center[1]] += 1
        except:
            pass
    for rowi in range(shape[0]):
        coli = 0
        while coli < shape[1]:
            if entriesMat[rowi,coli] > 0:
                scoreMat[rowi,coli] = scoreMat[rowi,coli]/entriesMat[rowi,coli]*100
            coli += 1
    
    return(scoreMat)


def findCents(ten,boxDists,ansCent):
    cents = []
    boxesTs = []
    shape = np.shape(ten)
    pastG = ansCent
    for A in ten:
        guesCents = []
        for i in range(CENTERmOVEMENT):
            for j in range(CENTERmOVEMENT):
                guess = [0,0]                
                guess[0] = round((pastG[0]+ansCent[0])/2)+i
                guess[1] = round((pastG[1]+ansCent[1])/2)+j                
                if guess[0] < shape[1] and guess[1] < shape[2]:
                    guesCents.append(guess)
                #print("guess",guess)
        

        boxesT = genBoxes(A,guesCents) #each T holds boxes for one frame in the tensor
        boxesTs.append(boxesT)
    

        bProfs = []
        for boxes in boxesT:
            bProf = boxProfile(boxes)
            bProfs.append(bProf)

        profScores = []
        for prof in bProfs: #prof is a distribution for the boxes associated with a guess regarding he center
            profScores.append(match(boxDists,prof))

        #print("profScores:",profScores,"\n")
        besti = profScores.index(min(profScores)) 
        if len(profScores) != len(guesCents):
            print("error, scores length is", len(profScores), "guessesLen is",len(guesCents))
            time.sleep(4)
        bestCent = guesCents[besti]
        cents.append(bestCent)
        print("bestCenter:", bestCent)
        #print(prof,"\n",boxDists,"\n\n")
        
    return(cents)
'''


def getAnsFrame(ten):
    #number = int(input("get answers from frame number:"))
    number = round(ten.shape[0]/2)
    posTen = makePos(ten)
    A = ten[number]
    copyA = copy.deepcopy(A)
    shape = np.shape(A)
    for i in range(shape[0]):
        vec = A[i]
        for j in range(shape[1]):
            if vec[j] < 0:
                copyA[i][j]= 1
            else:
                copyA[i][j] = 0
    return(posTen[number],copyA)


def showTen(ten,shade):
    print("\n\n\n TENSOR:")
    if type(shade) == int:
        nCol = ten.shape[2]
        for A in ten:
            print("\n next frame:")
            for vec in A:
                newVec = []
                for i in range(nCol):
                    if vec[i] == shade:
                        newVec.append("X")
                    else:
                        newVec.append(" ")
                print(newVec)
    elif type(shade) == list:
        nCol = ten.shape[2]
        for A in ten:
            print("\n next frame:")
            for vec in A:
                newVec = []
                for i in range(nCol):
                    if vec[i] in shade:
                        newVec.append("X")
                    else:
                        newVec.append(" ")
                print(newVec)
    else:
        for A in ten:
            print("\n next frame:")
            for vec in A:
                lis = []
                for el in vec:
                    lis.append(int(el))
                    #lis.append(round(el,2))
                print(lis)
                


main()    