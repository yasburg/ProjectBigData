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

residential = 'DC_Properties.csv'

def read_csv_data(residential): 

    data = pd.read_csv("C:\\Users\Atal\\Desktop\\School\\Project datas\\deresidential\\" + residential,  

                      sep=",", header=[0]) 

 

    return data 

data = read_csv_data(residential) 

data = data[['PRICE','AYB','GBA']].replace([np.inf, -np.inf], np.nan)
data = data[['PRICE','AYB','GBA']].dropna(how='any')

response_variable = data['PRICE']

GBA = data['GBA']

mod1 = sm.OLS(response_variable, GBA)
res1 = mod1.fit()

print(res1.summary())

plt.scatter(data['GBA'],data['PRICE'], s=20, alpha=0.5)
plt.title('GBA-Price')
plt.show
plt.savefig("C:\\Users\Atal\\Desktop\\School\\Project datas\\deresidential\\plotGBA.png")

