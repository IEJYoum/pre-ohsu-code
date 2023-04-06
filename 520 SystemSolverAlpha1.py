# -*- coding: utf-8 -*-



import matplotlib.pyplot as plt

class Equation:
    def __init__(self,x0,x1,x2,x3,x4,x5):
        self.x0=x0
        self.x1=x1
        self.x2=x2
        self.x3=x3
        self.x4=x4
        self.x5=x5



equations = []
solutions = []

MIN = -10 #chenge to XMIN XMAX 
MAX = 10
RATE = .01  #determines the size of step along x axis to find points near solution. Increase to save time for larger x range
WINDOW = 10 #determines distance from a perfect solution to be considered as "near" solutions. Decrease to save time for smaller y range

ax = []
ay = [] 
bx = []
by = []
ey = []
nears = [] 
 

def main():
    geteqns(2) #currently only functional for 2 equations  "get equations entered by the user or load canned if user does not provide valid entries"
    finddif() #don't put the burden on the user to figure out the point of any function
    findnear()
    findsols()
    print(solutions) #make this all its own function and describe it vv
    sx = []
    sy = []
    
    for i in solutions:
        sx.append(i[0])
        sy.append(i[1])
        
    plt.plot(ax,ay)
    plt.plot(bx,by)
    plt.plot(sx,sy, marker = "X")


def findsols():
    i = 0
    while i < len(nears)-1:
        a = nears[i]
        b = nears[i+1]
        aX = a[0]     # decide if this could benefit from more descriptive name
        aY = a[1]
        bX = b[0]
        bY = b[1]
        
        #removes from "nears" anywhere except immediately before equations cross (will not find soltuons if the graphs only "kiss" e.g. y = 1 and y = x^2 + 1)
        if aY * bY > 0 or bX - aX > (2 * RATE) :
            nears.remove(a)
        else:
            i += 1
    del nears[-1]
    

    #scans remaining "nears" in small incriments to find closest solution
    i = 0 
    fy = []
    while i < len(nears):
        a = Equation(0,0,0,0,0,0)
        a = equations[0]
        b = Equation(0,0,0,0,0,0)
        b = equations[1] 
        n = nears[i]
        nx = n[0]
        
        cx = nx
        while cx <= nx + RATE:
        
            cy = a.x0 + a.x1*cx + a.x2*cx**2 + a.x3*cx**3 + a.x4*cx**4 + a.x5*cx**5
            dy = b.x0 + b.x1*cx + b.x2*cx**2 + b.x3*cx**3 + b.x4*cx**4 + b.x5*cx**5
            difference = ((cy - dy)**2)**.5
            fy.append(difference)        
            cx += RATE / 1000
            
        minY = min(fy)
        minX = nx + fy.index(minY) * RATE / 1000
        cx = minX
        averageAtX = (a.x0 + a.x1*cx + a.x2*cx**2 + a.x3*cx**3 + a.x4*cx**4 + a.x5*cx**5 + b.x0 + b.x1*cx + b.x2*cx**2 + b.x3*cx**3 + b.x4*cx**4 + b.x5*cx**5)/2
        solutions.append((minX,averageAtX))
        i += 1
            
                    

#adds all points within "WINDOW" of solution
def findnear():
    i = 0
    l = len(ey)
    while i < l:
        ii = ey[i]
        if (ii ** 2) ** 0.5 < WINDOW:            
            j = MIN + (i * RATE)
            nears.append((j,ii))
        i += 1


def finddif():
    a = Equation(0,0,0,0,0,0)
    a = equations[0]
    b = Equation(0,0,0,0,0,0)
    b = equations[1]

    
    cx = MIN
    while cx <= MAX:
    
        cy = a.x0 + a.x1*cx + a.x2*cx**2 + a.x3*cx**3 + a.x4*cx**4 + a.x5*cx**5
        dy = b.x0 + b.x1*cx + b.x2*cx**2 + b.x3*cx**3 + b.x4*cx**4 + b.x5*cx**5
        
        ey.append(cy - dy)
        
        ax.append(cx)
        bx.append(cx)
        ay.append(cy)
        by.append(dy)
        
        cx += RATE

    


def geteqns(n):   #name n "number of equations being solved"
    i = 0
    while i < n:
        print("\n\n\n\nEQUATION #%i" % i)
        try:            
            x0 = int(input("0th order term:"))   #look for refactoring or recursion ******refactor into its own method and recurse through it*******
        except:
            x0 = 0
            print("USING CANNED DATA")
            i = -1
 
        if i == -1:       
            equations.append(Equation(5,-10,0,0,0,0)) 
            equations.append(Equation(0,100,0,-2,0,0))
            i = n+1
        else:              
            try:
                x1 = int(input("1st order term:"))
            except:
                x1 = 0
                print("set to 0")
                
            try:
                x2 = int(input("2nd order term:"))
            except:
                x2 = 0
                print("set to 0")
                
            try:
                x3 = int(input("3rd order term:"))
            except:
                x3 = 0
                print("set to 0")
    
            try:
                x4 = int(input("4th order term:"))
            except:
                x4 = 0
                print("set to 0")        
            
            try:
                x5 = int(input("5th order term:"))
            except:
                x5 = 0
                print("set to 0")            
            
            equationbucket = Equation(x0,x1,x2,x3,x4,x5)
            
            equations.append(equationbucket)            
            i += 1 
    



    
main()