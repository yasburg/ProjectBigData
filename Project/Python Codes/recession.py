#!/usr/bin/env python
# coding: utf-8

# In[14]:

import pandas as pd
import numpy as np
import sys
import time
import datetime
import matplotlib.pyplot as plt

import statsmodels.api as sm
import matplotlib.dates as mdates
import matplotlib.cbook as cbook
from matplotlib.dates import DateFormatter

# In[15]:

data_location = "DC_Properties.csv"

# In[16]:

df = pd.DataFrame()
index = 0

with open(data_location) as file:
    next(file)  

    for line in file:
        dic = {'SALEDATE': None, 'PRICE': None}
        line_content_list = line.split(',')

        saledate_str = line_content_list[12]
        price_str = line_content_list[13]

        # since all rows represents different house we can just append the necessary parts from the rows
        # here appending if both saledate and price values exist
        if saledate_str is not '' and price_str is not '':
            format = "%Y-%m-%d %H:%M:%S"  # the format that is used to convert string to datetime object
            datetime_object = datetime.datetime.strptime(saledate_str, format)
            dic['SALEDATE'] = datetime_object
            dic['PRICE'] = int(float(price_str))
            df = df.append(pd.Series(dic, name=index))
            index += 1
            
# In[26]:
            
df = df.sort_values('SALEDATE').reset_index(drop=True)

# In[74]:

x = df["SALEDATE"]
y = df["PRICE"]

# In[97]:

plt.figure(figsize=(12,8))
counts, bins, bars = plt.hist(x,bins=100)
plt.title("Number of Sales in Each Year", fontsize=12)
plt.xlabel("Years")
plt.ylabel("Numbers of Sales")
plt.savefig("recession1.png")

print(counts)
# In[98]:

current_year = x[0].year
total_price_per_year = 0
df_price = pd.DataFrame()
i = 0

for index, row in df.iterrows():
    if current_year == row['SALEDATE'].year:
        total_price_per_year += row['PRICE']/1000000
    else:
        dic = {'T_PRICE': total_price_per_year}
        index = current_year
        df_price = df_price.append(pd.Series(dic, name=index))
        #i += 1
        
        current_year = row['SALEDATE'].year
        total_price_per_year = row['PRICE']/1000000
        
dic = {'T_PRICE': total_price_per_year}        
df_price = df_price.append(pd.Series(dic, name=2018))

# In[99]:

print(df_price)
plt.figure(figsize=(12,8))
plt.plot(df_price.index, df_price["T_PRICE"])
plt.xticks(np.arange(1982, 2020, 2.0))
plt.title("Total Money Spent on House Per Year", fontsize=12)
plt.xlabel("Year")
plt.ylabel("Money Spent on House (in millions $)")
plt.savefig("recession2.png")

# In[101]:

response_variable = df_price["T_PRICE"]
explanatory_variable = df_price.index

mod = sm.OLS(response_variable, explanatory_variable)
res = mod.fit()
print(res.summary())