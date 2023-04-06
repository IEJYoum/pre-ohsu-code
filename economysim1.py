# -*- coding: utf-8 -*-
"""
Created on Sat Jun  6 22:35:52 2020

@author: Jalaa
"""

import random


class Business:
    def __init__(self, name, money, inventoryValue, income, employees):
        self.name = name
        self.money = money
        self.inventoryValue = inventoryValue
        self.income = income
        self.employees = employees


class Consumer:
    def __init__(self, name, money, employer, salary):
        self.name = name
        self.money = money
        self.employer = employer
        self.salary = salary
        



BUSINESSES = []
CONSUMERS = []
YEAR = 0
ENDyEAR = 4

numberOfBusinesses = 100
numberOfConsumers = 1000



def main():
    global YEAR
    generateBusinesses(numberOfBusinesses)
    generateConsumers(numberOfConsumers)
    while YEAR < ENDyEAR:
        consume()
        hire()
        produceSupply()
        '''
        for business in BUSINESSES:
            
            try:
                print("business:",business.name,"money:", business.money, "inventoryValue:",business.inventoryValue, "highest paid employee:", business.employees[0].salary, "number of employees:", len(business.employees), "\n")
            
            except:
                print(business.name, "money:", business.money, "no employees")
        '''
        #print(YEAR, "\n\n\n\n\n\n\n")
        YEAR += 1
    

    for business in BUSINESSES:
    
        try:
            print("business:",business.name,"money:", business.money, "inventoryValue:",business.inventoryValue, "highest paid employee:", business.employees[0].salary, "number of employees:", len(business.employees), "\n")
        
        except:
            print("business:",business.name, "money:", business.money, "no employees \n")

    



def produceSupply():
    global BUSINESSES
    global CONSUMERS
    for business in BUSINESSES:
        size = len(business.employees)
        business.inventoryValue += size * 10
        for employee in business.employees:
            business.money -= employee.salary
            employee.money += employee.salary



def hire():
    global BUSINESSES
    global CONSUMERS
        
    salaryOffers = [] #index should match business name
    
    for business in BUSINESSES:
        totalCost = 0
        for employee in business.employees:
            totalCost += employee.salary
        
        business.employees = []
        biddingPrice = round((business.income-totalCost) / 5)   ############################################
        salaryOffers.append(biddingPrice)
        business.income = 0
        
    for consumer in CONSUMERS:
        consumer.employer = -1
        try:
            bestOffer = salaryOffers.index(max(salaryOffers))
            consumer.employer = bestOffer
            consumer.salary = salaryOffers[bestOffer]
            if salaryOffers[bestOffer] > 0:
                salaryOffers[bestOffer] -= 1
            else:
                del salaryOffers[bestOffer]
            
        
            for business in BUSINESSES:
                if bestOffer == business.name:
                    business.employees.append(consumer)
            
        except:
            #print("no jobs for", consumer.name)
            a = 0
        
        
        



def consume():
    global BUSINESSES
    global CONSUMERS
    for consumer in CONSUMERS:
        buyChecker = 0
        totalTries = 0
        while buyChecker == 0 and totalTries < numberOfBusinesses:
            
            storeName = random.randint(0,numberOfBusinesses - 1)
            totalTries += 1
            
            for business in BUSINESSES:
                if business.name == storeName and business.inventoryValue >= consumer.money:
                    spendingMoney = round(consumer.money/4)  #######################################################
                    business.money += spendingMoney
                    business.income += spendingMoney
                    business.inventoryValue -= spendingMoney
                    consumer.money -= spendingMoney
                    buyChecker = 1
            
                
           


    
#name, money, employer, salary   
def generateConsumers(numberOfConsumers):
    i = 0
    while i < numberOfConsumers:
        consumer = Consumer(i,10,-1,0) ###############################################
        CONSUMERS.append(consumer)
        i += 1

#name, money, inventoryValue, income, employees

def generateBusinesses(numberOfBusinesses):
    i = 0
    while i < numberOfBusinesses:
        business = Business(i, 100, 50, 0, []) ########################################################
        BUSINESSES.append(business)
        i += 1

    




main()