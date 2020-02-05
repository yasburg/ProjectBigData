'''
Yasin AYDIN 06/21/2019
'''
import pandas as pd
import numpy as np
import sys
import time
import datetime
import matplotlib.pyplot as plt

import matplotlib.dates as mdates
import matplotlib.cbook as cbook
from matplotlib.dates import DateFormatter

data_location = "DC_Properties.csv"

#NOTE: IT TAKES AROUND 126 SECOND TO READ ALL FILE AND CREATE DATA FRAME
def read_csv(data_loc):
    df = pd.DataFrame()
    index = 0
    # reading file
    with open(data_loc) as file:
        next(file)  # skipping the first line (titles)

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
    return df

def to_csv(df):
    df = df.sort_values('SALEDATE')
    df.to_csv('price-date-sorted.csv', sep=',', index=False)
    return df

def visualize(df):

    datetime_list = df['SALEDATE'].tolist()
    date_list = []
    for i in range(len(datetime_list)):
        format = "%m/%d/%Y"  # the format that is used to convert string to datetime object
        datetime_object = datetime.datetime.strptime(datetime_list[i], format)
        day = datetime.date(datetime_object.year, datetime_object.month, datetime_object.day)
        date_list.append(day)

    year_average_list = []
    for year in range(1982,2018):
        num_of_sale_this_year = 0
        total_price = 0
        for index, sale_date in enumerate(df['SALEDATE']):
            if int(sale_date[6:10]) == year:
                total_price += int(df['PRICE'][index])
                num_of_sale_this_year += 1
        if num_of_sale_this_year == 0:#to avoid division by zero error
            num_of_sale_this_year = 1
        year_average_list.append(total_price//num_of_sale_this_year)

    fig, ax = plt.subplots(figsize=(10, 8))
    # price_bubble = [i//10000 for i in df['PRICE']]
    myFmt = mdates.DateFormatter('%Y')
    ax.scatter(range(1982,2018), year_average_list, s=200, color='green', alpha=0.7)

    mean_five_year_list = []
    years = [1985,1990,1995,2000,2005,2010,2015]

    index = 0
    for i in range(len(year_average_list)//5):
        total_five_year = year_average_list[index] + year_average_list[index+1] + year_average_list[index+2] + year_average_list[index+3] + year_average_list[index+4]
        mean_five_year_list.append(total_five_year//5)
        index += 5
    print("1990 mean price:", mean_five_year_list[1], "\n2015 mean price:", year_average_list[2016-1982])#we will user 2016 resuls as mean since the outliers influence the results
    ax.plot(years, mean_five_year_list, color='blue', alpha=0.7)
    ax.set(xlabel="Date", ylabel="Price ($)", )
    ax.set_title("House prices over the years")
    ax.set_ylim([0, 1600000])
    plt.show()

def main():
    start_time = time.time()

    #disable these after first run to not waste time!
    df = read_csv(data_location)
    #to_csv sorts df by sale date!
    df = to_csv(df)

    df = pd.read_csv("price-date-sorted.csv")
    print("It took", "%.3f" % (time.time() - start_time), "seconds")
    visualize(df)



if __name__ == '__main__':
    main()
