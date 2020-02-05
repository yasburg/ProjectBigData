'''
Bob Mes 06/23/2019
'''
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats
import statsmodels.api as sm


def main():
    df = read('DC_Properties.csv')

    dataDictPrice = makeDataDict(df, 'PRICE')
    dataDictGBA = makeDataDict(df, 'GBA')

    df_describePRICE = dataFramWithDescribe(dataDictPrice)
    df_describeGBA = dataFramWithDescribe(dataDictGBA)

    # Checking difference
    print(checkDifferenceAnova(dataDictPrice))
    print(checkDifferenceAnova(dataDictGBA))

    # Regression
    dfDummies = pd.get_dummies(df['ASSESSMENT_NBHD'], prefix='category')
    print("Regresion only Neighborhood")
    regress(df['PRICE'], dfDummies)

    print("Regresion on the rooms")
    regress(df['PRICE'], df['GBA'])

    print("Regresion on both")
    regress(df['GBA'], dfDummies)

    # Visualization
    barChart2Of(df_describePRICE.index, df_describePRICE['mean'],
                'Barchart of average price of property per neighborhood', 'Average price of property (dollars)',
                'barchartPrice')
    barChart2Of(df_describeGBA.index, df_describeGBA['mean'],
                'Barchart of the average GBA per property per neighborhood', 'Average GBA of property (square feet)',
                'barchartGBA')

    print(df_describePRICE['mean'].sort_values())
    print(df.groupby(by='ASSESSMENT_NBHD').mean())


def read(file):
    df = pd.read_csv('C:\\Users\\bob\\Desktop\\premaster BA - VU\\Project Big Data\\EindOpdracht\\' +
                     file, header=0)
    data = df[['ASSESSMENT_NBHD', 'GBA', 'PRICE']]

    data = deleteNeighbourhood('Crestwood', data)
    return data.dropna(axis=0)


def makeDataDict(data, whichParameter):
    neighboorhoods = data.iloc[:, 0].unique()
    PricePerNeigh = {}
    for i in neighboorhoods:
        PricePerNeigh[i] = (data[data['ASSESSMENT_NBHD'] == i][whichParameter])

    return PricePerNeigh


def deleteNeighbourhood(name, data):
    data = data[data['ASSESSMENT_NBHD'] != name]
    return data


def checkDifferenceAnova(dataDict):
    return scipy.stats.f_oneway(dataDict['Old City 2'], dataDict['Old City 1'], dataDict['Capitol Hill'],
                                dataDict['Georgetown'], dataDict['Burleith'], dataDict['Palisades'],
                                dataDict['Berkley'], dataDict['Kent'], dataDict['Wesley Heights'],
                                dataDict['American University'], dataDict['Spring Valley'], dataDict['Chevy Chase'],
                                dataDict['Kalorama'], dataDict['Mt. Pleasant'], dataDict['Columbia Heights'],
                                dataDict['16th Street Heights'], dataDict['Brightwood'], dataDict['Petworth'],
                                dataDict['Ledroit Park'], dataDict['Eckington'], dataDict['Brookland'],
                                dataDict['Brentwood'], dataDict['Trinidad'], dataDict['Woodridge'],
                                dataDict['Lily Ponds'], dataDict['Deanwood'], dataDict['Marshall Heights'],
                                dataDict['Fort Dupont Park'], dataDict['Hillcrest'], dataDict['Anacostia'],
                                dataDict['Randle Heights'], dataDict['Congress Heights'])


def dataFramWithDescribe(dataDict):
    df_describe = pd.DataFrame(columns=dataDict['Old City 2'].describe().index)
    for key in dataDict.keys():
        df_describe = df_describe.append({'count': dataDict[key].describe()[0], 'mean': dataDict[key].describe()[1],
                                          'std': dataDict[key].describe()[2], 'min': dataDict[key].describe()[3],
                                          '25%': dataDict[key].describe()[4], '50%': dataDict[key].describe()[5],
                                          '75%': dataDict[key].describe()[6], 'max': dataDict[key].describe()[7]},
                                         ignore_index=True)
    df_describe.index = dataDict.keys()
    return df_describe


def regress(y, x):
    mod = sm.OLS(y, x)
    res = mod.fit()
    print(res.summary())


def barChart2Of(names, prices, title, ylabel, nameSave):
    y_pos = np.arange(len(names))

    plt.figure(figsize=(15, 5))
    plt.bar(y_pos, prices, align='center', alpha=0.5)
    plt.xticks(y_pos, names, rotation='vertical', ha='center')
    plt.xlabel('Neighborhood')
    plt.ylabel(ylabel)
    plt.title(title)
    plt.savefig(nameSave, format='svg')

    plt.show()


if __name__ == '__main__':
    main()

