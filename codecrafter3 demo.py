# -*- coding: utf-8 -*-
"""
Created on Tue May 26 02:13:02 2020

@author: Jalaa
"""

CLOCK = 0
CURSOR = 0
HOLDER = 0

SCRIPT = []
SCRIPT0 = []
INTEGERsET = []
CONDITIONS = []
OLDsCRIPT = []
VARIABLES = []
STORAGE = []
MAXcLOCK = 40
MAXlENGTH = 10


import random

class Variable:
    def __init__(self,name,value):
        self.name = name
        self.value = value


        
        
def main():
    getConditions()
    getIntegerSet()
    for i in CONDITIONS:
        generateScript(i)




        
def generateScript(condition):
    global SCRIPT
    global SCRIPT0
    global OLDsCRIPT
    global CLOCK
    global INTEGERsET
    goal = False
    scriptLength = 0


    '''
    SCRIPT = []
    runScript()
    goal = True
    '''
    


    while goal == False:
        CLOCK += 1
        if CLOCK > MAXcLOCK:
            break
        
        if scriptLength > MAXlENGTH:
            print("RESTARTING script")
            scriptLength = 0
            restartScript()
        
        
        updateScript()      
        
        try:
            runScript()
            print("working script:",SCRIPT0)
            for i in SCRIPT0:
                OLDsCRIPT.append(i)
            scriptLength += 1   
            goal = checkGoal(condition)
        
        except:
            print("failed script:",SCRIPT0)
            restartScript()
            #revertScript()                            
        
        
    if CLOCK <= MAXcLOCK:        
        result = "success!"
    else:
        result = "failure"
    
    print("CLOCK:",CLOCK)
    print(result)


def checkGoal(condition):
    if condition == "endTrue":
        if SCRIPT[-1] == True:
            return(True)
        else:
            return(False)
            
                
def restartScript():
    global SCRIPT
    global SCRIPT0
    global OLDsCRIPT
    SCRIPT = []
    SCRIPT0 = []
    OLDsCRIPT = []
    '''
    there's a bug somewhere here that lead to this:
        RESTARTING script
        working script: [8]
        working script: [8, 'lessThan', 'if']  where this should have raised an error
    
    '''
    
    

def revertScript():
    global SCRIPT
    global SCRIPT0
    global OLDsCRIPT
    print("reverting script")   
    SCRIPT = []
    SCRIPT0 = []
    for i in OLDsCRIPT:
        SCRIPT.append(i)
        SCRIPT0.append(i)         
            



  # boolSwitch switch endSwitch incrimentVariable "incrimentVariableDelete" getVariable delete makeVariable getHolder, zeroCursor zeroCursorDelete1 zeroCursorDelete2, findRemains, if + equalTo etc while, zeroHolder, incrimentHolder

 
    
  #need updateList where list2 gets storage and holder is clear
  #needs generate random
  #remove holder bits from while
  #needs more storage commands


def updateScript():
    global SCRIPT
    global HOLDER
    #script = [10,10,"equalTo","if","boolSwitch","true!","printDelete2","switch","false!","printDelete2","endSwitch"]
    allCommands = ["boolSwitch", "switch", "endSwitch","incrimentVariable", "incrimentVariableDelet", "getVariable", "makeVariable","getHolder", "zeroCursor", "zeroCursorDelete", "findRemains", "if", "equalTo", "lessThan", "greaterThan", 0, "while", "endWhile", "zeroHolder","incrimentHolder","add","insert","removeFromList","returnFromList","length" ]
    numberOfCommands = len(allCommands)
    script = []
    toScript = random.randint(0,numberOfCommands-1)
    script.append(allCommands[toScript])
    
    '''
    if toScript == 0:
        script.append(random.randint(2,10))
        
        
    elif toScript == 1:
        script.append(random.randint(2,30))             
        
    elif toScript == 2:
        script.append("equalTo")
        script.append("if")

        
    elif toScript == 3:
        script.append("lessThan")
        script.append("if")
    '''    
        
    #make list that keeps track of permutations and avoids repeating failed scripts

        
        
    for i in script:
        SCRIPT.append(i)
        SCRIPT0.append(i)
    
    #print("script:", script)
    #print("SCRIPT:", SCRIPT)
    #print("SCRIPT0", SCRIPT0)


def runScript():
    global CLOCK
    global CURSOR
    global SCRIPT
    global VARIABLES
    global HOLDER
    while CURSOR < len(SCRIPT):
        if CLOCK > MAXcLOCK:
            print("MAXcLOCK exceeded")
            raise Exception("MAXcLOCK EXCEEDED")
        #print("HOLDER:", HOLDER)
        #print("CLOCK:", CLOCK)
        #print("CURSOR:", CURSOR)
                

        #reset clock and move cursor
        if SCRIPT[CURSOR] == "resetClock":
            CLOCK = 0
            del SCRIPT[CURSOR]


        
        
        #elif SCRIPT[CURSOR] == "generateRandom"
        
        
        #bool, "boolSwitch", true code, "switch", false code, "endSwitch"
        elif SCRIPT[CURSOR] == "boolSwitch":
            trueCode = []
            falseCode = []
            del SCRIPT[CURSOR]
            while SCRIPT[CURSOR] != "switch":
                trueCode.append(SCRIPT[CURSOR])
                del SCRIPT[CURSOR]            
            del SCRIPT[CURSOR]
            
            while SCRIPT[CURSOR] != "endSwitch":
                falseCode.append(SCRIPT[CURSOR])
                del SCRIPT[CURSOR]
            del SCRIPT[CURSOR]
            
            if SCRIPT[CURSOR - 1] == True:
                trueCode.reverse()
                for i in trueCode:
                    SCRIPT.insert(CURSOR,i)
            
            elif SCRIPT[CURSOR - 1] == False:
                falseCode.reverse()
                for i in falseCode:
                    SCRIPT.insert(CURSOR,i)
            
            del SCRIPT[CURSOR - 1]
            
            


        #name, "incrimentVariable"
        elif SCRIPT[CURSOR] == "incrimentVariable":
            for var in VARIABLES:
                if var.name == SCRIPT[CURSOR - 1]:
                    var.value += 1
                    break            
            CURSOR += 1


        #name, "incrimentVariableDelete",
        elif SCRIPT[CURSOR] == "incrimentVariableDelete":
            for var in VARIABLES:
                if var.name == SCRIPT[CURSOR - 1]:
                    var.value += 1
                    break            
            del SCRIPT[CURSOR]
            del SCRIPT[CURSOR-1]
            CURSOR -= 1


        #name, "getVariable", returns value from name
        elif SCRIPT[CURSOR] == "getVariable":
            for var in VARIABLES:
                if var.name == SCRIPT[CURSOR - 1]:
                    SCRIPT.insert(CURSOR + 1,var.value)
                    break
            
            del SCRIPT[CURSOR]
            del SCRIPT[CURSOR-1]
            CURSOR -= 1

        elif SCRIPT[CURSOR] == "delete":
            del SCRIPT[CURSOR]
            del SCRIPT[CURSOR-1]            
            
            
        #name, value, "makeVariable"
        elif SCRIPT[CURSOR] == "makeVariable":
            variable = Variable(SCRIPT[CURSOR-2],SCRIPT[CURSOR-1])
            VARIABLES.append(variable)
            print("name, value, index:", variable.name, variable.value, len(VARIABLES)-1)
            del SCRIPT[CURSOR]
            del SCRIPT[CURSOR-1]
            del SCRIPT[CURSOR-2]
            CURSOR -= 2
            

        #"getClock", clockvalue
        elif SCRIPT[CURSOR] == "getClock":
            SCRIPT.insert(CURSOR + 1,CLOCK)
            print("inserted clock")
            #del SCRIPT[CURSOR]
            CURSOR += 1

        #"getHolder"
        elif SCRIPT[CURSOR] == "getHolder":
            SCRIPT.insert(CURSOR + 1,HOLDER)
            #del SCRIPT[CURSOR]
            CURSOR += 1



        #"zeroCursor"
        elif SCRIPT[CURSOR] == "zeroCursor":
            CURSOR = 0

        
        #"zeroCursorDelete"
        elif SCRIPT[CURSOR] == "zeroCursorDelete":
            del SCRIPT[CURSOR]
            CURSOR = 0


        #"zeroHolder"
        elif SCRIPT[CURSOR] == "zeroHolder":
            HOLDER = 0
            del SCRIPT[CURSOR]
        
        #"incrimentHolder"
        elif SCRIPT[CURSOR] == "incrimentHolder":
            HOLDER += 1
            CURSOR += 1

        #thing to print, "print"
        elif SCRIPT[CURSOR] == "print":
            paper = SCRIPT[CURSOR - 1]
            print(paper)
            #del SCRIPT[CURSOR] 
            CURSOR += 1

        #thing to print and delete, "printDelete1"
        elif SCRIPT[CURSOR] == "printDelete1":
            paper = SCRIPT[CURSOR - 1]
            print(paper)
            del SCRIPT[CURSOR-1]
            
        
                
        #thing to print and delete, "printDelete2"  (also deletes print command)
        elif SCRIPT[CURSOR] == "printDelete2":
            paper = SCRIPT[CURSOR - 1]
            print(paper)
            del SCRIPT[CURSOR]
            del SCRIPT[CURSOR-1]
            CURSOR -= 1
        
        
        #value, index, "add"
        elif SCRIPT[CURSOR] == "add":
            value = SCRIPT[CURSOR - 2]
            print("value",value)
            index = SCRIPT[CURSOR - 1]
            current = SCRIPT[index]    
            current += value
            SCRIPT[index] = current
            del SCRIPT[CURSOR]
            del SCRIPT[CURSOR-1]
            del SCRIPT[CURSOR-2]
            CURSOR -= 2             
        
        
        #value, index, "insert", does not move cursor except to next step past insert
        elif SCRIPT[CURSOR] == "insert":
            value = SCRIPT[CURSOR - 2]
            index = SCRIPT[CURSOR - 1]
            SCRIPT.insert(index,value)
            print(SCRIPT)
            del SCRIPT[CURSOR]
            del SCRIPT[CURSOR-1]
            del SCRIPT[CURSOR-2]
            CURSOR -= 2 
            #CURSOR += 1
            
            


        #index to delete, list name, "removeFromList"
        elif SCRIPT[CURSOR] == "removeFromList":
            listFrom = SCRIPT[CURSOR-1]
            del listFrom[SCRIPT[CURSOR-2]]
            del SCRIPT[CURSOR]
            del SCRIPT[CURSOR-1]
            del SCRIPT[CURSOR-2]
            CURSOR -= 2


        #index to return from, list name, "returnFromList"
        elif SCRIPT[CURSOR] == "returnFromList":
            listFrom = SCRIPT[CURSOR-1]
            value = listFrom[SCRIPT[CURSOR-2]]
            SCRIPT.insert(CURSOR + 1, value)
            del SCRIPT[CURSOR]
            del SCRIPT[CURSOR-1]
            del SCRIPT[CURSOR-2]
            CURSOR -= 2
            
        
        
        
        elif SCRIPT[CURSOR] == "if":
            #1, 3, lessThan, if, booleanReturn
            if SCRIPT[CURSOR - 1] == "lessThan" and type(SCRIPT[CURSOR - 3]) == int:
                
                if SCRIPT[CURSOR - 3] < SCRIPT[CURSOR - 2]:
                    SCRIPT.insert(CURSOR + 1, True)
                    
                else:
                    SCRIPT.insert(CURSOR + 1, False)
                
            if SCRIPT[CURSOR - 1] == "greaterThan":
                
                if SCRIPT[CURSOR - 3] > SCRIPT[CURSOR - 2]:
                    SCRIPT.insert(CURSOR + 1, True)
                    
                else:
                    SCRIPT.insert(CURSOR + 1, False)            
            
            if SCRIPT[CURSOR - 1] == "equalTo":
                
                if SCRIPT[CURSOR - 3] == SCRIPT[CURSOR - 2]:
                    SCRIPT.insert(CURSOR + 1, True)
                    
                else:
                    SCRIPT.insert(CURSOR + 1, False)             


            del SCRIPT[CURSOR]
            del SCRIPT[CURSOR-1]
            del SCRIPT[CURSOR-2]
            del SCRIPT[CURSOR-3]            
            CURSOR -= 3
            
        





        #numerator, denominator, findRemains, remainder
        elif SCRIPT[CURSOR] == "findRemains":
            numerator = SCRIPT[CURSOR-2]
            denominator = SCRIPT[CURSOR-1]
            remainder = numerator % denominator
            SCRIPT.insert(CURSOR + 1, remainder)
            del SCRIPT[CURSOR]
            del SCRIPT[CURSOR-1]
            del SCRIPT[CURSOR-2]
            CURSOR -= 2
                
         
        #listToBeMeasured, "length"
        elif SCRIPT[CURSOR] == "length":
            listToBeMeasured = SCRIPT[CURSOR - 1]
            length = len(listToBeMeasured)
            SCRIPT.insert(CURSOR + 1, length)
            del SCRIPT[CURSOR]
            del SCRIPT[CURSOR-1]
            CURSOR -=1            
 
        
        
            '''
            #index before transformation, moveCursor
            elif SCRIPT[CURSOR] == "moveCursor":
                cursorBucket == SCRIPT[CURSOR-1]
                if cursorBucket > CURSOR:                        
                    del SCRIPT[CURSOR]
                    del SCRIPT[CURSOR-1]
            '''                        

                
        #start, end, incriment, while, code to loop, endWhile, appends subcursor to STORAGE
        elif SCRIPT[CURSOR] == "while":
            print("StartWhile")
            subScript = []
            #subCursor = 1
            
            whileStart = SCRIPT[CURSOR-3]
            whileEnd = SCRIPT[CURSOR-2]
            whileIncriment = SCRIPT[CURSOR-1]
            del SCRIPT[CURSOR]
            del SCRIPT[CURSOR-1]
            del SCRIPT[CURSOR-2]
            del SCRIPT[CURSOR-3]
            CURSOR -= 3
            
            
            while CURSOR < len(SCRIPT):
                if SCRIPT[CURSOR] == "endWhile":
                    del SCRIPT[CURSOR]
                    break
                else:
                    subScript.append(SCRIPT[CURSOR])
                    del SCRIPT[CURSOR]
                    #print("bing",subScript)
            #print("bong",SCRIPT)
            

            subCursor = 0
            returns = []
            

            while whileStart + subCursor < whileEnd:
                #HOLDER = subCursor
                #print(HOLDER)
                print(subScript)
                returnsBucket = runSubScript(subScript,0)
                CLOCK += 1
                
                SCRIPT.insert(CURSOR,returnsBucket)
                '''
                try:
                    for i in returnsBucket:
                        returns.append(i)
                except:
                    if type(returnsBucket) == int or type(returnsBucket) == bool:
                        returns.append(returnsBucket)
                '''
                STORAGE.append(subCursor)
                
                
                subCursor += whileIncriment                            
                    
            #STORAGE.append(returns)
            print("while returns entering STORAGE:", returns)
            print("EndWhile")
            #CURSOR += 1

        
        else:
            CURSOR += 1
        
        #print("CLOCK:",CLOCK)
        #print("CURSOR:",CURSOR)
        #print("# of Variables:", len(VARIABLES))
        #print(VARIABLES[0].value)
        #CLOCK += 1
        

#use 0 instead of subcursor
def runSubScript(subScript,subCursor):
    global SCRIPT
    global CURSOR
    global VARIABLES
    global HOLDER
    scriptHolder = []
    cursorHolder =[]
    scriptHolder.append(SCRIPT)
    cursorHolder.append(CURSOR)
    SCRIPT = subScript
    CURSOR = subCursor
    runScript()
    subScript = SCRIPT
    SCRIPT = scriptHolder[-1]
    CURSOR = cursorHolder[-1]
    del scriptHolder[-1]
    del cursorHolder[-1]
    return(subScript)
    
    
    

    
def goalCheckPrimes():
    primes = [2,3,5,7,11,13,17,19,23]
    setBucket = INTEGERsET
    for j in primes:
        for i in setBucket:
            if i == j:
                setBucket.remove(i)

    if len(setBucket) == 0:
        return(True)
    else:
        return(False)
        
        
        

def getIntegerSet():
    integerSet = [9,2,4,5,3]
    for i in integerSet:        
        INTEGERsET.append(i)


def getConditions():
    CONDITIONS.append("endTrue")
    
    
nullHolder = Variable("null",0) 
VARIABLES.append(nullHolder)
    
main()  