'''
Yasin AYDIN 06/22/2019
'''
import pandas as pd
import statsmodels.api as sm
import warnings
import math
import time
import matplotlib.pyplot as plt

#It takes around 120 seconds to run everything for the first time!
def main():
    start_time = time.time()
    warnings.simplefilter(action='ignore', category=FutureWarning)
    df = read_csv('DC_Properties.csv')
    to_csv(df)
    new_df = pd.read_csv('only_room_types_and_price.csv')
    #preparation of the lists for the regression model
    target = []
    predictors = []
    # for index, row in new_df.iterrows():
    #     target.append(int(new_df.get_value(index, 'Price')))
    #     predictors.append([int(new_df.get_value(index, 'Rooms')), int(new_df.get_value(index, 'Bathroom')), int(new_df.get_value(index, 'Bedroom')), int(new_df.get_value(index, 'Kitchen')), int(new_df.get_value(index, 'Landarea'))])

    # for index, row in new_df.iterrows():
    #     target.append(int(new_df.get_value(index, 'Rooms')))
    #     predictors.append([int(new_df.get_value(index, 'Bathroom')), int(new_df.get_value(index, 'Bedroom')), int(new_df.get_value(index, 'Kitchen'))])

    predictors = new_df.loc[:, ['Rooms', 'Bathroom', 'Bedroom', 'Kitchen', 'Landarea']]
    regress(new_df['Price'], predictors)
    print("It took ", "%.2f" % (time.time()-start_time), "seconds")
    visualization(new_df)

def read_csv(data_loc):
    df = pd.read_csv(data_loc)
    new_df = pd.DataFrame()

    for index,row in df.iterrows():
        rooms_str = df.get_value(index, 'ROOMS')
        bathroom_str = df.get_value(index, 'BATHRM')
        bedroom_str = df.get_value(index, 'BEDRM')
        kitchens_str = df.get_value(index, 'KITCHENS')
        landarea_str = df.get_value(index, 'LANDAREA')
        price_str = df.get_value(index, 'PRICE')
        if type(df.get_value(index, 'SALEDATE')) == str:
            saleyear_str = df.get_value(index, 'SALEDATE')[0:4]
        else:
            continue
        if not math.isnan(bathroom_str) \
                and not math.isnan(rooms_str) \
                and not math.isnan(bedroom_str) \
                and not math.isnan(kitchens_str) \
                and not math.isnan(price_str) \
                and not math.isnan(landarea_str) \
                and int(price_str) > 1 \
                and int(saleyear_str) < 2015 \
                and int(saleyear_str) >= 2009:
            dic = {'Rooms': int(rooms_str), 'Bathroom': int(bathroom_str), 'Bedroom': int(bedroom_str), 'Kitchen': int(kitchens_str), 'Landarea': int(landarea_str), 'Price': int(price_str)}
            new_df = new_df.append(pd.Series(dic, name=index))

    return new_df

def to_csv(df):
    df.to_csv('only_room_types_and_price.csv', sep=',', index=False)
    return df
    
def regress(target, predictors):
    model = sm.OLS(target, predictors).fit()
    print(model.summary())

    # predictions = model.predict(predictors)
    # print(predictions)

def visualization(df):

    average_heat_list = df.groupby('Rooms').mean()['Price'].tolist()
    room_list = df['Rooms'].tolist()
    set_room = list(set(room_list))

    rooms_list = df['Rooms'].tolist()
    landarea_list = df['Landarea'].tolist()
    price_list = df['Price'].tolist()
    landarea_list = [i//300 for i in landarea_list]
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.scatter(rooms_list, price_list, s=landarea_list, alpha=0.7)
    ax.set(xlabel="Number of rooms", ylabel="Price ($)", )
    ax.set_title("Number of rooms and prices of residences")
    ax.plot(set_room, average_heat_list, color='purple')
    plt.show()

if __name__ == '__main__':
    main()