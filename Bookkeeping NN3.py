# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 17:19:45 2020

@author: Jalaa
"""


import pandas as pd
import numpy as np

FILEpATH = ""
TRANSACTIONfILE = "transactions.csv"
CUSTOMERfILE = "customers.csv"
PRODUCTfILE = "products.csv"



DATA = []


def main():
    loadCSVS()
    menu()
    print(len(DATA))


        
def menu():
    kinds = ["customer","product","transaction"]
    while True:    
        print("1: add new customer")
        print("2: add new product")
        print("3: add new transaction")
        print("4: view existing data")
        print("0: save and quit")        
        while True:
            try:
                a = int(input("action: ")) - 1
                break
            
            except:
                print("please type action number")
            
        if a >= 0 and a < len(DATA):
            dataframe = DATA[a]
            kind = kinds[a]
            addData(dataframe,kind)
        
        elif a == 3:
            searchData()
        
        elif a == -1:
            saveQuit()               
            break    
    

        



def searchData():
    customers = DATA[0]
    products = DATA[1]
    transactions = DATA[2]
    print("\n\n\n searching for...\n")
    print("1: a range of data")
    print("2: a particular customer, product, or transaction")    
    while True:
        try:
            s0 = int(input("action: "))
            break
        except:
            print("please enter action number")
    
    if s0 == 1:
        print("\n\n\n sort data by...\n")
        pass
    
    elif s0 == 2:
        print("\n\n\n searching for...\n")
        print("1: a customer")
        print("2: a product")
        print("3: a transaction")
        while True:
            try:
                s2 = int(input("action: "))
                break
            except:
                print("please enter action number")      
                
                
    if s2 == 1:
        try:
            print(DATA[0])
            cName = input("customer name:")
            print(customers[customers['name'] == cName],"\n")
            try:
                print(transactions[transactions['customer'] == cName],"\n")
            except:
                print("no transactions found for customer",cName,"\n")
        except:
            print("\nclient not found\n")
        
    if s2 == 2:
        try:
            print(DATA[1])
            pName = input("product name:")
            print(products[products['name'] == pName],"\n")
            print(transactions[transactions['product'] == pName],"\n") 
        except:
            print("\nproduct not found\n")
        
        
    if s2 == 3:
        try:
            print(DATA[2])
            date = formatDate(input("transaction date mm/dd/yy:"))
            print(transactions[transactions['date'] == date],"\n")
        except:
            print("\nno transactions found for given date\n")


def formatDate(date):
    while True:
        if len(date) == 8 and date[2] == "/" and date[5] == "/" :
            newDate = date[6:8] + date[0:2] + date[3:5]
            return(newDate)
        else:
            print("\nerror formatting date, please try again\n")
            date = input("date mm/dd/yy:")
            
            
    



def addData(dataframe,kind):
    nump = dataframe.to_numpy()
    
    if kind == "customer":
        print("making new customer")
        name = input("name: ")
        a = np.array([[name,0]])
        nump = np.concatenate((nump,a), axis=0)
        dataframe = pd.DataFrame(nump,columns = ["name","balance"])
        DATA.insert(1,dataframe)
        del DATA[0]

    
    if kind == "product":
        print("making new product")
        name = input("product name: ")
        while True:
            try:
                price = int(input("price: "))
                volume = int(input("volume in stock: "))
                break
            except:
                print("please use plain numbers for price and volume")
        print("pricetype",type(price))
        a = np.array([[name,price,volume,0]], dtype = object)
        #a[0,0] = name        
        nump = np.concatenate((nump,a), axis=0)
        print("TYPE:", type(price),type(a[0,2]))
        print(nump)
        dataframe = pd.DataFrame(nump,columns = ["name","price","volumeInStock","volumeSold"])
        DATA.insert(2,dataframe)
        del DATA[1]

        
    if kind == "transaction":
        newTransaction()
        



def newTransaction():
    customers = DATA[0]
    cNump = customers.to_numpy()
    products = DATA[1]
    pNump = products.to_numpy()
    transactions = DATA[2]
    tNump = transactions.to_numpy()
    
    print("\nnew transaction (will automatically update product volumes and customer balance)\n")

    date = formatDate(input("date (mm/dd/yy): "))
    
    print("\n",pNump,"\n")
    product = input("product: ") #add update product volumes    
    productLocation = np.where(pNump == product)
    pRow = productLocation[0]
    if len(pRow) == 0:
        print("\nproduct not found (case sensitive, must be added as new product), canceling transaction\n")
        return()        
    while True:
        try:
            volumeSold = int(input("volume sold: "))
            break
        except:
            print("\nplease input plain number for volume sold\n")
                    
    pNump[pRow,2] -= volumeSold
    pNump[pRow,3] += volumeSold
    print("\n",pNump,"\n")
    
    print("\n",cNump,"\n")
    customer = input("customer: ") #add update customer balance
    customerLocation = np.where(cNump == customer)
    cRow = customerLocation[0]
    if len(cRow) == 0:
        print("\ncustomer not found (case sensitive, must be added as new customer), canceling transaction\n")
        return() 
    while True:        
        try:
            totalPrice = int(input("total price: ")) 
            totalPayed = int(input("total payed: "))
            cNump[cRow,1] += totalPrice - totalPayed
            print("\n",cNump,"\n")
            break
        except:
            print("\nplease use plain numbers for price and payed\n")
    
    newTransaction = np.array([[date,customer,product,volumeSold,totalPrice,totalPayed]])
    tNump = np.concatenate((tNump,newTransaction), axis=0)
    transactionDF = pd.DataFrame(tNump,columns = ["date","customer","product","volumeSold","totalPrice","totalPayed"])
    customerDF = pd.DataFrame(cNump,columns =["name","balance"])
    productDF = pd.DataFrame(pNump,columns =["name","price","volumeInStock","volumeSold"])
    DATA.clear()
    DATA.append(customerDF)
    DATA.append(productDF)
    DATA.append(transactionDF)




def makeCSV(kind):    
    if kind == "customer":        
        headers = {"name": [],
           "balance": [] }
        dataframe = pd.DataFrame(headers)
        dataframe.to_csv(FILEpATH + CUSTOMERfILE,index = False)
        
    elif kind == "product":
        headers = {"name": [],
           "price": [],
           "volumeInStock": [],
           "volumeSold": []}
        dataframe = pd.DataFrame(headers)
        dataframe.to_csv(FILEpATH + PRODUCTfILE,index = False)
        
    elif kind == "transaction":    
        headers = {"date": [],
           "customer": [],
           "product": [],
           "volumeSold": [],
           "totalPrice": [],
           "totalPayed" : []}
        dataframe = pd.DataFrame(headers)
        dataframe.to_csv(FILEpATH + TRANSACTIONfILE,index = False)

def loadCSVS():
    i = 0
    j = 0
    kinds = ["customer","product","transaction"]
    files = [CUSTOMERfILE,PRODUCTfILE,TRANSACTIONfILE]
    lfiles = len(files) 
    while i < lfiles and j < 4:    
        kind = kinds[i]
        file = files[i]       
        try:
            dataframe = pd.read_csv(FILEpATH + file)
            DATA.append(dataframe)
            i += 1
        except:
            print("no CSV found, making new file at", FILEpATH, file)
            makeCSV(kind)
            j += 1



def viewEditNew():
    while True:
        print("1: view existing")
        print("2: edit existing")
        print("3: add new")
        try:
            a = int(input("action: "))
            return(a)        
        except:
            print("please enter action number")
            



def saveQuit():
    i = 0
    files = [CUSTOMERfILE,PRODUCTfILE,TRANSACTIONfILE]    
    while i < len(files):
        dataframe = DATA[i]
        file = files[i]
        dataframe.to_csv(FILEpATH + file,index = False)        
        i += 1

    
    
main()