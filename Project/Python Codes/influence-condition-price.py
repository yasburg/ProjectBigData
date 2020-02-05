# -*- coding: utf-8 -*-
"""
Bob Mes
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats
import statsmodels.api as sm

def main():
    df = read()
    print(df.groupby('CNDTN').count())
    dfMeanPrice = df.groupby('CNDTN').mean()
    dfMeanPrice = dfMeanPrice[dfMeanPrice.index != 'Default']
    
    conditionOrders = ['Poor', 'Average', 'Fair', 'Good', 'Very Good', 'Excellent']
    priceOrders = [dfMeanPrice['PRICE'][conditionOrders[0]], dfMeanPrice['PRICE'][conditionOrders[1]], 
               dfMeanPrice['PRICE'][conditionOrders[2]], dfMeanPrice['PRICE'][conditionOrders[3]], 
               dfMeanPrice['PRICE'][conditionOrders[4]], dfMeanPrice['PRICE'][conditionOrders[5]]]
    barChart2Of(conditionOrders, priceOrders, 
            'Barchart of average price against condition', 'average price', 'barchartCondition.svg')
    
    dataDict = makeDataDict(df, 'PRICE')
    conditionOrders = ['Poor', 'Average', 'Fair', 'Good', 'Very Good', 'Excellent']
    npconditionOrders = np.array(conditionOrders)
    for i in conditionOrders:
        print(i)
        for j in npconditionOrders[npconditionOrders != i]:
            print('P-value t-test between ' + i + ' and '+ j + ' = ' + str(scipy.stats.ttest_ind(dataDict[i], 
                                                                                                 dataDict[j])[1]))
        print("")
    
def makeDataDict(data, whichParameter):
    neighboorhoods = data.iloc[:, 0].unique()
    PricePerNeigh = {}
    for i in neighboorhoods:
        PricePerNeigh[i] = (data[data['CNDTN'] == i][whichParameter])
        
    return PricePerNeigh
    
def barChart2Of(names, prices, title, ylabel, nameSave):
    y_pos = np.arange(len(names))
    
    plt.figure(figsize=(10, 5))
    plt.bar(y_pos, prices, align='center', alpha=0.5)
    plt.xticks(y_pos, names, rotation='horizontal', ha='center')
    plt.xlabel('condition')
    plt.ylabel(ylabel)
    plt.title(title)
    plt.tight_layout()
    plt.savefig(nameSave, format='svg')

    plt.show()
    
def read(): 
    df = pd.read_csv('C:\\Users\\bob\\Desktop\\premaster BA - VU\\Project Big Data\\EindOpdracht\\' +
                                  "DC_Properties.csv", header=0)
    data = df[['CNDTN','PRICE']]  
    
    return data.dropna(axis=0)

if __name__ == '__main__':
    main()