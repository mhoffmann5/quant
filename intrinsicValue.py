# Hoff is a virgin (.Y.)

import pandas as pd
import requests
from bs4 import BeautifulSoup
from tabulate import tabulate
import numpy as np

sym = ["BABA", "AAPL", "BIDU", "AMZN", "GM", "TSLA"]

print("Growth Rate Analysis")

for ticker in sym:
    incomeStatment = requests.get("https://finance.yahoo.com/quote/" + ticker + "/financials/")
    income = BeautifulSoup(incomeStatment.content,'lxml')
    incStatement = income.find_all('table')[0]
    df = pd.read_html(str(incStatement))
    IS = df[0]
    
    cashFlows = requests.get("https://finance.yahoo.com/quote/" + ticker + "/cash-flow?p=" + ticker)
    cfs = BeautifulSoup(cashFlows.content,'lxml')
    cflows = cfs.find_all('table')[0]
    df_FCF = pd.read_html(str(cflows))
    CF = df_FCF[0]
    
    book = requests.get("https://finance.yahoo.com/quote/"+ticker+"/balance-sheet?p="+ticker)
    bv = BeautifulSoup(book.content,'lxml')
    bookval = bv.find_all('table')[0]
    df_BV = pd.read_html(str(bookval))
    BookValue = df_BV[0]
    
    RevGrowth(IS)
    NIGrowth(IS)
    FCFGrowth(CF)
    BVGrowth(BookValue)

def RevGrowth(IS):

    rev = []
    revGrowth = []

    for r in range(1, 5):
        rev.append(int(IS[r][1]))
    
    for i in range(len(rev) - 1):
        growth = ((rev[i] - rev[i+1]) / rev[i+1])
        revGrowth.append((growth))
        
    geoProd = 1
    for t in range(len(revGrowth)):
        geoProd = geoProd * (1+revGrowth[t])
    
    geoRevGrowth = round(((geoProd)**(1/len(revGrowth)) - 1) * 100, 2)
    
    print("--------------------------------------")
    print(ticker+":")
    print("Compound Annual Revenue Growth Rate = ", geoRevGrowth, "%")
    print("STD DEV: ", round(np.std(revGrowth)*100, 2), "%")
    

def NIGrowth(IS):

    NI = []
    NIGrowth = []

    for r in range(1, 5):
        NI.append(int(IS[r][25]))
    
    for i in range(len(rev) - 1):
        growth = ((NI[i] - NI[i+1]) / NI[i+1])
        NIGrowth.append((growth))
   
    geoProd = 1
    for t in range(len(NIGrowth)):
        geoProd = geoProd * (NIGrowth[t]+1)
    
    geoNIGrowth = round(((geoProd)**(1/len(NIGrowth)) - 1) * 100, 2)
   
    print("Compound Annual NI Growth Rate = ", geoNIGrowth, "%")
    print("Std Dev: ", round(np.std(NIGrowth)*100, 2), "%")
    
    
def FCFGrowth(FCF):
    FCF = []
    FCFGrowth = []

    for r in range(1, 5):
        FCF.append(int(CF[r][9]))

    for i in range(len(FCF) - 1):
        growth = ((FCF[i] - FCF[i+1]) / FCF[i+1])
        FCFGrowth.append((growth))

    geoProd = 1
    for t in range(len(FCFGrowth)):
        geoProd = geoProd * (FCFGrowth[t]+1)
 
    geoFCFGrowth = round(((geoProd)**(1/len(FCFGrowth)) - 1) * 100,2)

    print("Compound Annual FCF Growth Rate = ", geoFCFGrowth, "%")
    print("Std Dev: ", round(np.std(FCFGrowth)*100, 2), "%")

    
def BVGrowth(Book):
    BV = []
    BVGrowth = []

    for r in range(1, 5):
        BV.append(int(Book[r][36]))

    for i in range(len(BV) - 1):
        growth = ((BV[i] - BV[i+1]) / BV[i+1])
        BVGrowth.append((growth))

    geoProd = 1
    for t in range(len(BVGrowth)):
        geoProd = geoProd * (BVGrowth[t]+1)
 
    geoBVGrowth = round(((geoProd)**(1/len(BVGrowth)) - 1) * 100,2)
    
    print("Compound Annual Book Value Growth Rate = ", geoBVGrowth, "%")
    print("Std Dev: ", round(np.std(BVGrowth)*100, 2), "%")

# To do:
# margins growth, sustainable growth rate
# change std dev measure change to variation in of TOTAL rev, book value, etc. --> sensitivity analysis (+- 2stdevs)
