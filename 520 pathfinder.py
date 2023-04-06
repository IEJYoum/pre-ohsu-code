# -*- coding: utf-8 -*-


import random
maze = []



class Node:
    def __init__(self,x,y,n,s,e,w):
        self.x=x
        self.y=y
        self.n=n
        self.s=s
        self.e=e
        self.w=w


def main(size):
    #randomly generates the maze
    i = 0
    while i < size:
        j = 0
        while j < size:
            maze.append([j,i,random.randint(0,2)])
            j+=1
        i+=1
    maze[0]=[0,0,3]
    maze[size**2-1] =[size-1,size-1,-10]
    print(maze)
    drawmaze(maze)

    #searches each available square for available squares
    node0 = Node(0,0,0,0,0,0)
    tosearch = [node0]
    solved = 0
    while solved < 100:
        for ts in tosearch:
            node0 = findnear(ts,size)
            tosearch.remove(ts)
            #node0.n used to store "win condition" to determine if G has been reached
            if node0.n == 2:
                tosearch.clear()
                print("Solvable!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                k = 1
                while k != 0:               
                    k = findpath(size)
                    print(k)
                print("SOLVED!!!!!")
                solved += 100
            
            #records free squares to search
            if node0.n == 1:
                node0.n = 0
                noden = Node(0,0,0,0,0,0)
                noden.x = node0.x
                noden.y = node0.y - 1
                tosearch.append(noden)                
            if node0.s == 1:
                node0.s = 0
                nodes = Node(0,0,0,0,0,0)
                nodes.x = node0.x
                nodes.y = node0.y + 1 
                tosearch.append(nodes)               
            if node0.e == 1:
                node0.e = 0
                nodee = Node(0,0,0,0,0,0)
                nodee.x = node0.x + 1
                nodee.y = node0.y
                tosearch.append(nodee)               
            if node0.w == 1:
                node0.w = 0
                nodew = Node(0,0,0,0,0,0)
                nodew.x = node0.x - 1
                nodew.y = node0.y
                tosearch.append(nodew)

        solved += 1
    maze[size**2-1] =[size-1,size-1,-10]
    maze[0]=[0,0,10]
    drawmaze(maze)


#finds and removes dead ends from the path
def findpath(size):
    changesmade=0
    tempath = [[size-1,size-1,3]]
    for i in maze:
        if i[2] == 3:
            tempath.append(i)
    for i in tempath:
        iscore = 0
        for j in tempath:
            if i[0] == j[0] and i[1] == j[1]:
                nothing = 0
            else:
                if i[0] == j[0]:
                    if i[1] == j[1]+1 or i[1] == j[1]-1:
                        iscore += 1
                
                if i[1] == j[1]:
                    if i[0] == j[0]+1 or i[0] == j[0]-1:
                        iscore += 1   
        if iscore < 2 and i[0] + i[1] > 0 and i[0] + i[1] < 2*(size-1):
            i[2] = 4
            changesmade += 1
        
    print(tempath)
    return(changesmade)




def drawmaze(maze):
    row = 0
    toprint = []
    for i in maze:
        if i[1] == row:
            if i[2] == 2:
                toprint.append("X")
            elif i[2] == 3:
                toprint.append("O")
            elif i[2] == -10:
                toprint.append("G")
            elif i[2] == 10:
                toprint.append("S")
            else:
                toprint.append(" ")
        else:
            print(toprint)
            toprint.clear()
            row += 1
            if i[2] == 2:
                toprint.append("X")
            elif i[2] == 3:
                toprint.append("O")
            else:
                toprint.append(" ")
    print(toprint)

#checks to see if adjacent squares are open            
def findnear(node,size):
    i = 0
    while i < size**2:
        tile = maze[i]
        if tile[0] == node.x and tile[1] == node.y - 1 and tile[2] < 2:
            #print("North open")
            node.n = 1
        if tile[0] == node.x and tile[1] == node.y + 1 and tile[2] < 2:
            #print("South open")
            node.s = 1               
        if tile[0] == node.x + 1 and tile[1] == node.y and tile[2] < 2:
            #print("East open")
            node.e = 1
        if tile[0] == node.x - 1 and tile[1] == node.y and tile[2] < 2:
            #print("West open")
            node.w = 1 
        if tile[0] == node.x and tile[1] == node.y:
            if tile[2] == -10:
                node.n = 2
            else:
                tile[2] = 3 
        i+=1

    return(node)
    
            
        
        
#main's argument determines the length ("size") of randomly generated maze       
main(4)