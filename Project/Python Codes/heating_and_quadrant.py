'''
Yasin AYDIN 06/23/2019
'''
import pandas as pd
import statsmodels.api as sm
import warnings
import math
import time
import matplotlib.pyplot as plt

#It takes around 443.68 seconds for the first run!! because of the string inputs
def main():
    start_time = time.time()
    warnings.simplefilter(action='ignore', category=FutureWarning)
    # df = read_csv('DC_Properties.csv')
    # to_csv(df)
    new_df = pd.read_csv('heat_quadrant_price.csv')
    # preparation of the lists for the regression model
    target = []
    predictors = []
    for index, row in new_df.iterrows():
        target.append(new_df.get_value(index, 'Quadrant'))
        predictors.append(new_df.get_value(index, 'Heat'))

    print("It took ", "%.2f" % (time.time() - start_time), "seconds")
    visualization(new_df)


def read_csv(data_loc):
    df = pd.read_csv(data_loc)
    new_df = pd.DataFrame()

    for index, row in df.iterrows():
        heating_str = df.get_value(index, 'HEAT')
        quadrant_str = df.get_value(index, 'QUADRANT')
        price_str = df.get_value(index, 'PRICE')
        if not math.isnan(price_str) and not heating_str == '' and type(quadrant_str) == str and not quadrant_str == '' and int(price_str) > 1:
            dic = {'Heat': str(heating_str), 'Quadrant': str(quadrant_str), 'Price': int(price_str)}
            new_df = new_df.append(pd.Series(dic, name=index))

    return new_df

def to_csv(df):
    df.to_csv('heat_quadrant_price.csv', sep=',', index=False)
    return df

def visualization(df):

    ave_prices_quad = df.groupby(['Quadrant']).mean()['Price'].tolist()
    heat_list = df['Heat'].tolist()
    quadrant_list = df['Quadrant'].tolist()
    set_quad = list(set(quadrant_list))
    price_list = df['Price'].tolist()

    price_list = [i // 50000 for i in price_list]
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.scatter(heat_list, quadrant_list, s=price_list, alpha=0.7)
    ax.set(xlabel="Heating type", ylabel="Quadrant", )
    ax.set_title("Heating type and quadrant relation\nwith price of residence")
    fig.autofmt_xdate()
    plt.show()

    fig, ax = plt.subplots(figsize=(10, 8))
    ax.set(xlabel="Quadrants", ylabel="Average Price ($)")
    ax.set_title("Average prices of residences \nin different quadrants")
    ax.bar(set_quad, ave_prices_quad, width=0.5)
    plt.show()

    heat_count_quad = df.groupby(['Heat', 'Quadrant'])['Quadrant'].count().unstack().reset_index().plot.bar(x='Heat', y=set_quad)
    heat_count_quad.set_title("Number of houses and heat types\n with each quadrant")
    heat_count_quad.set(xlabel="Heating types", ylabel="Number of residences")
    plt.show()


if __name__ == '__main__':
    main()
