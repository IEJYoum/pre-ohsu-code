# -*- coding: utf-8 -*-

import random
from KMbot_collection import  Detective, Grudger, Cooperator, Cheater, Copycat, Copykitten, Random
from KMsimulator import create_bot, run_game


class Organism:
    def __init__(self,genome,name,fitness,generatingNumber,memory):
        self.genome = genome
        self.name = name
        self.fitness = fitness 
        self.generatingNumber = generatingNumber
        self.memory = memory


GLOBALlIST = []
MAXgENERATIONS = 50
NURSERY = []
ECOSYSTEM = []
GRAVEYARD = []


def main(): 
    generation = 0
    commandList = generateCommandList(0,0)
    eve = generateGenome(Organism([],0,0,0,[]),commandList)
    phenome = runGenome(eve)
    runPhenome(eve,phenome)
    reproduce(eve,phenome)
    cycleLife()    
    generation += 1
    print(phenome,eve.fitness)
    
    minFitness = 0
    
    while generation < MAXgENERATIONS:
        
        for organism in ECOSYSTEM:
            commandList = generateCommandList(organism.generatingNumber,generation)
            organism = generateGenome(organism,commandList)
            phenome = runGenome(organism)
            runPhenome(organism,phenome)
            if organism.fitness > minFitness:
                reproduce(organism,phenome)
            print(phenome,organism.fitness)

        minFitness = generationAverageFitness() - 50 
        
        cycleLife()
        if len(ECOSYSTEM) > 0:
            print(minFitness)
            print("generation", generation)
        generation += 1
        
        
        

    
    
    #print("name:",organism.name, organism.fitness, organism.genome,"\n", phenome,"\n\n\n")
    
def generationAverageFitness():
    totalFitness = 0
    for organism in ECOSYSTEM:
        totalFitness += organism.fitness
    l = len(ECOSYSTEM)
    if l > 0:
        return(totalFitness / len(ECOSYSTEM))
    else:
        return(0)


   
def generateCommandList(listNumber,generation):
    commandList = []    
    if listNumber == 0:
        commandList.append([0,2,12,100,1]) #makes 100 offspring whose 2nd index is random(0,6)
        commandList.append([0,12,0,1,0])

    elif listNumber == 1 and generation < 2:
        commandList.append([2,2,12,100,1,2,0,1,1]) #replace old reproduction command with make one clone
    
    elif len(ECOSYSTEM) < 30:
        commandList.append([2,2,0,1,1,2,0,3,1])
    
    elif len(ECOSYSTEM) > 60:
        commandList.append([2,2,0,3,1,2,0,1,1])
    
    return(commandList)




def generateGenome(organism,commandList):
    cursor = 0
    while cursor < len(commandList):                
        command = commandList[cursor]
        
        if type(command) == int:        
            
            
            if command == -1: #read all GLOBALlIST entries into memory
                organism.genome.append([3,1,0,0])      
            
            
            if command == 0: #read all memory         
                for entry in GLOBALlIST:
                    organism.genome.append([10,1,1,0])


            if command == 1: #clear memory
                organism.genome.append([10,4,0,0]) 
                
            if command == 2: 
                organism.genome.append([12,0,0,0])

        elif type(command) == list:              
            if command[0] == 0: #insert gene
                i = 1
                geneBucket = []
                while i < 5:
                    geneBucket.append(command[i])
                    i += 1
                organism.genome.append(geneBucket)
                
            elif command[0] == 1: #for all genes whose command[1]th index == command[2], append [gene = command[3]] immediately next
                functionalGroup = []
                lenCommand = len(command)
                i = 3
                while i < lenCommand:
                    functionalGroup.append(command[i])
                    i += 1
        
                functionalGroup.reverse()
                subCursor = 0
                while subCursor < len(organism.genome):
                    
                    if organism.genome[subCursor][command[1]] == command[2]:
                        for gene in functionalGroup:                             
                            organism.genome.insert(subCursor + 1,gene)
                    
                    subCursor += 1                  
           
            elif command[0] == 2: #swaps first gene in list for second gene in list [2,9,9,9,9,1,2,3,4]
                for gene in organism.genome:
                    i = 0
                    while i < 4:
                        if gene[i] != command[i+1]:
                            i = 5
                        i += 1
                    if i < 5:
                        i = 0
                        while i < 4:
                            gene[i] = command[i + 5]                            
                            i += 1
                        
            
        cursor += 1
                
    return(organism)
    
    
    

def reproduce(organism,phenome):
    cursor = 0
    while cursor < len(phenome):
        gene = phenome[cursor]
        if gene[0] == 2:
            offspringTotal = gene[2]
            generatingNumber = gene[3]
            offspringCount = 0
            while offspringCount < offspringTotal:
                baby = Organism([],0,0,0,[])
                baby.name = len(NURSERY) + len(ECOSYSTEM) + len(GRAVEYARD)
                baby.generatingNumber = generatingNumber
            
                for genomeGene in organism.genome:
                    geneBucket = []
                    for strand in genomeGene:
                        geneBucket.append(strand)
                    baby.genome.append(geneBucket)
                
                for item in organism.memory:                        
                    baby.memory.append(item)

  
                '''
                MUTATIONS BELOW
                '''
                if gene[1] == 12: #edit 12 type genes' 2nd index                    
                    subcursor = 0
                    while subcursor < len(baby.genome):
                        if baby.genome[subcursor][0] == 12:
                           baby.genome[subcursor][2] = random.randint(0,6)
                        subcursor += 1

                        
                NURSERY.append(baby)
                offspringCount += 1                
                
        
        cursor += 1
                

def cycleLife():
    while len(ECOSYSTEM) > 0:
        GRAVEYARD.append(ECOSYSTEM[0])
        del ECOSYSTEM[0]
    while len(NURSERY) > 0:
        ECOSYSTEM.append(NURSERY[0])
        del NURSERY[0]
        


def runPhenome(organism,phenome):
    global GLOBALlIST
    global COUNTER
    cursor = 0
    while cursor < len(phenome):        

        gene = phenome[cursor]
       
        if gene[0] == 1.1:
            sourceGene = phenome[gene[1]]
            destinationGene = phenome[gene[2]]            
            destinationGene[gene[3]] = sourceGene[3]
            
        elif gene[0] == 1.2:
            sourceGene = phenome[cursor + gene[1]]
            destinationGene = phenome[cursor + gene[2]]            
            destinationGene[gene[3]] = sourceGene[3]

        elif gene[0] == 1:
            sourceGene = phenome[cursor + gene[1]]
            destinationGene = phenome[cursor + gene[2]]            
            destinationGene[3] = sourceGene[3]            
        
        elif gene[0] == 3:
            if gene[1] == 0:         
                gene[3] = GLOBALlIST[gene[2]]
            if gene[1] == 1:
                for element in GLOBALlIST:
                    organism.memory.append(element)



        #5,F(),o,t where F() ==0addition ==1subtraction ==2* ==3/ ==4%, firstNumber = phenome[cursor + gene[2]][3], secondNumber = phenome[cursor + gene[3]][3]
        elif gene[0] == 5:
            firstNumber = phenome[cursor + gene[2]][3]
            secondNumber = phenome[cursor + gene[3]][3]

            if gene[1] == 0:
                phenome[cursor+1][3] = firstNumber + secondNumber
            
            elif gene[1] == 1:
                phenome[cursor+1][3] = firstNumber - secondNumber

            elif gene[1] == 2:
                phenome[cursor+1][3] = firstNumber * secondNumber

            elif gene[1] == 3:
                phenome[cursor+1][3] = firstNumber / secondNumber   
                
            elif gene[1] == 4:
                phenome[cursor+1][3] = firstNumber % secondNumber

        #if false delete phenome[cursor + 1], if true delete phenome[cursor + 2]
        #6,X,o,t, where X == 0 for equality  ==1 for 1 > 2 and ==2 for 1>=2, number1 = phenome[cursor + gene[2]][3], number2 = phenome[cursor + gene[3]][3]
        elif gene[0] == 6: #compare by relative index 
            number1 = phenome[cursor + gene[2]][3]
            number2 = phenome[cursor + gene[3]][3]
            if gene[1] == 0: #compare equality
                
                if number1 == number2:
                    del phenome[cursor + 2]
                else:
                    del phenome[cursor + 1]

            if gene[1] == 1: #true if #1 > #2
                
                if number1 > number2:
                    del phenome[cursor + 2]
                else:
                    del phenome[cursor + 1]

            if gene[1] == 2: #true if #1 >= #2
                
                if number1 >= number2:
                    del phenome[cursor + 2]
                else:
                    del phenome[cursor + 1]
                    
            
        elif gene[0] == 7: 
                #0,S,I  return len(GLOBALlIST) to Stepincursor, IndexinGene
            if gene[1] == 0:
                phenome[cursor + gene[2]][gene[3]] = len(GLOBALlIST)

                #1,S,I prints  sourceoffset[Index]
            if gene[1] == 1:               
                sourceGene = phenome[cursor + gene[2]]
                print(sourceGene[gene[3]])
                
            if gene[1] == 1.1:
                print(organism.memory)
                
            #7,2,
            if gene[1] == 2:
                if gene[2] == 0:
                    COUNTER = 0
                if gene[2] == 1:
                    COUNTER += 1
                if gene[2] == 2:
                    gene[3] = COUNTER

        
        elif gene[0] == 8:
            if gene[1] == 0:
                organism.memory.append(gene[3])
            
            if gene[1] == 1:
                organism.memory.append(phenome[cursor + gene[2]][3])
                
                
        elif gene[0] == 10:   
            if gene[1] == 0:
                gene[3] = organism.memory[0]
            
            if gene[1] == 1:
                if len(organism.memory) > 0:
                    gene[3] = organism.memory[0]
                    del organism.memory[0]
                else:
                    numberOfGenesToDelete = gene[2] #includes self, deletes this many genes after to get rid of sequences set for each input of data
                    deletedGenes = 0
                    while deletedGenes < numberOfGenesToDelete:
                        del phenome[cursor]
                    cursor -= 1
                    
            if gene[1] == 2:
                del organism.memory[0]
                
                
            if gene[1] == 3:
                i = 0
                organism.memory.reverse()
                while i < len(organism.memory):
                    phenome.insert(cursor+1, [0,10,0,organism.memory[i]])
                    i += 1
                
            
            if gene[1] == 4:                    
                while len(organism.memory) > 0:
                    del organism.memory[0]
                        

        elif gene[0] == 11:
            if gene[1] == 0: #lengths
                if gene[2] == 0:
                    gene[3] = len(phenome)
                if gene[2] == 1:
                    gene[4] = len(organism.memory)

        elif gene[0] == 12:
            if gene[1] == 0: #run Kai's Bot thing with 10 different opponents, 5x each
                botList = [Cheater, Cooperator, Copycat, Copykitten, Grudger, Detective, Random]                
                bot1 = create_bot(botList[gene[2]],1)[0]
                i = 0
                while i < 10:
                    opponentBot = botList[random.randint(0,6)]
                    bot2 = create_bot(opponentBot,1)[0]                                                                                    
                    organism.fitness += run_game(bot1,bot2,5)
                    i += 1
                
            
                     
                    
            
            


        cursor += 1       
        
    return(1)    
    

#12 moving cursor (use to build while loops by checking condition and sending cursor back)


#11s get info about organism
    #0 put lengths in 11[3]
       #0 return len(phenome)
       #1 return len(memory)


#10s retrieving memory
    #0 retrieve first entry, save into 3rd index
    #0.1 retrieve and delete first entry
    #0.2 delete first entry

#0s are for storing data and are used in generate organism


#1s are for actions in the phenome, moving information around by index
#1sdx source gene index in phenome, destination gene index in phenome, target index


#1.1SDx source offset, destination offset, index to copy into in destinationgene
            #sourceGene = phenome[cursor + gene[1]]
            #destinationGene = phenome[cursor + gene[2]]            
            #destinationGene[gene[3]] = sourceGene[3]


    
#2s are for reproductive actions
#2TNx - T for offspringType (0 clone 1 mutant), N for offspringNuber


#3s are for reading in data
#30xy where 0 is globallist, x is index from and y holds data
#3,1,?,? append each entry from globallist into memory


#4s are for outputting data
#40By where 0 is globallist, B is 0 for append or 1 for remove, and y is value to append or remove

#5,F(),o,t where F() ==0addition ==1subtraction ==2* ==3/ ==4%, firstNumber = phenome[cursor + gene[2]][3], secondNumber = phenome[cursor + gene[3]][3]


#6,X,o,t, where X == 0 for equality  ==1 for 1 > 2 and ==2 for 1>=2, number1 = phenome[cursor + gene[2]][3], number2 = phenome[cursor + gene[3]][3]
#if false delete phenome[cursor + 1], if true delete phenome[cursor + 2]


#7 functions
    #0,S,I  return len(GLOBALlIST) to Stepincursor, IndexinGene
    #1,S,I print, stepsincursor, index in gene 
    #1.1 print organism.memory
    #2,F,x F ==0 zero Counter, ==1 incriment counter, ==2 copy COUNTER value to x
    #3, return len
    

#8 saving memory
    #0 self 3rd index
    #1 relativephenomeindex geneindex 





def runGenome(organism):
    phenome = []
    for gene in organism.genome:
        geneBucket = []
        for strand in gene:
            geneBucket.append(strand)
        phenome.append(geneBucket)

    return(phenome)

    
    
main()




