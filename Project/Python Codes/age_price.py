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

residential = 'DC_Properties.csv'


def read_csv_data(residential):
    data = pd.read_csv(residential, sep=",", header=[0])
    return data


data = read_csv_data(residential)

data = data[['PRICE', 'AYB']].replace([np.inf, -np.inf], np.nan)
data = data[['PRICE', 'AYB']].dropna(how='any')

data['age'] = 2019 - data['AYB']
set_years = list(set(data['age']))
response_variable = data['PRICE']
explanatory_variable = data['age']
years_average_price = data.groupby(['age']).mean()['PRICE'].tolist()

print(years_average_price)
mod = sm.OLS(response_variable, explanatory_variable)
res = mod.fit()
print(res.summary())

fig, ax = plt.subplots(figsize=(10, 8))
ax.set_title("Average price of residences with their age")
ax.set(xlabel="Age of residence", ylabel="Average price ($)")
ax.plot(set_years, years_average_price)
ax.set_ylim([0, 10000000])
plt.show()

