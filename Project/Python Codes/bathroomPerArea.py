#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import re
import datetime
import csv

import scipy.stats

import sys
from io import StringIO
import traceback
from queue import Queue
import requests
import json
import threading
import statsmodels.api as sm
from matplotlib import pyplot as plt

data_location = 'DC_Properties.csv'

# In[37]:

df = pd.read_csv(data_location, sep=",", header=[0])

df = df[['BATHRM', 'HF_BATHRM', 'AYB', 'GBA']].replace([np.inf, -np.inf], np.nan)
df = df[['BATHRM', 'HF_BATHRM', 'AYB', 'GBA']].dropna(how='any')
df['AGE'] = 2019 - df['AYB']
df['BATHRM_CO'] = (df['BATHRM'] + 0.5 * df['HF_BATHRM'] )*1000 / df['GBA']
df = df.sort_values('GBA').reset_index(drop=True)
df = df.drop([i for i in range(0,12)]).reset_index(drop=True)

# In[44]:

response_variable = df['BATHRM_CO']
explanatory_variable = df['AGE']

mod = sm.OLS(response_variable, explanatory_variable)
res = mod.fit()
print(res.summary())

plt.subplots(figsize=(10, 8))
plt.title("Age and Bathroom per Square foot")
plt.xlabel("Age")
plt.ylabel("Bathroom (1000/f^2)")
plt.scatter(explanatory_variable, response_variable)
plt.savefig('bathroomPerArea.png')