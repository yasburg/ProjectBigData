# -*- coding: utf-8 -*-
"""
We truthfully declare:
- to have contributed approximately equally to this assignment [if this is not true, modify this sentence to disclose individual contributions so we can grade accordingly]
- that we have neither helped other students nor received help from other students
- that we provided references for all code that is not our own

Yasin Aydin yasinaydin@sabanciuniv.edu
Faruk Simsekli faruksimsekli.7@gmail.com
"""

"""
This template is meant as a guideline. Feel free to alter existing functions and add new functions.
Remember to use descriptive variable names and to keep functions concise and readable.
"""

sleepdatafile   = 'hue_week_3.csv'
surveydatafile  = 'hue_questionnaire.csv'

"""
The main() function is called when template_week_4.py is run from the command line.
It is a good place to define the logic of the data flow (for example, reading, transforming, analyzing, visualizing).
"""
import pandas as pd
import numpy as np
import math
import scipy.stats
import statsmodels.api as sm
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import axes3d
from matplotlib import cbook
from matplotlib import cm
from matplotlib.colors import LightSource
import matplotlib.pyplot as plt
import numpy as np

def main(sleepdatafile,surveydatafile):
    str_diff_list = ["Day 1 Bedtime Difference Time (sec)", "Day 2 Bedtime Difference Time (sec)", "Day 3 Bedtime Difference Time (sec)",
                     "Day 4 Bedtime Difference Time (sec)", "Day 5 Bedtime Difference Time (sec)", "Day 6 Bedtime Difference Time (sec)",
                     "Day 7 Bedtime Difference Time (sec)", "Day 8 Bedtime Difference Time (sec)", "Day 9 Bedtime Difference Time (sec)",
                     "Day 10 Bedtime Difference Time (sec)", "Day 11 Bedtime Difference Time (sec)", "Day 12 Bedtime Difference Time (sec)", ]
    str_inbed_list = ['Day 1 In Bed Time (sec)', 'Day 2 In Bed Time (sec)', 'Day 3 In Bed Time (sec)', 'Day 4 In Bed Time (sec)',
                      'Day 5 In Bed Time (sec)', 'Day 6 In Bed Time (sec)', 'Day 7 In Bed Time (sec)', 'Day 8 In Bed Time (sec)',
                      'Day 9 In Bed Time (sec)', 'Day 10 In Bed Time (sec)', 'Day 11 In Bed Time (sec)', 'Day 12 In Bed Time (sec)', ]

    sleep, survey = read_data(sleepdatafile,surveydatafile)
    df = pd.DataFrame(columns=['ID', 'group', 'delay_nights', 'delay_time', 'sleep_time'])
    df.set_index('ID', inplace=True)
    survey.set_index('ID', inplace=True)
    # print (survey.to_string())
    for index,row in sleep.iterrows():
        delay_n_count = 0
        total_delay = 0
        total_sleep = 0
        slept_days = 0

        #COUNTING DAYS WITH DELAYED SLEEP AND ADDING THEM
        for day in str_diff_list:
            if math.isnan(row[day]):
                continue
            elif int(row[day]) > 0:
                delay_n_count += 1
                total_delay += int(row[day])

        #COUNTING TOTAL SLEEP TIME AND ADDING THEM
        for day in str_inbed_list:
            if math.isnan(row[day]):
                continue
            else:
                total_sleep += int(row[day])
                slept_days += 1

        #CHECKING FOR DIVISION 0 ERROR
        if delay_n_count == 0:
            delay = "-"
        else:
            delay = total_delay // delay_n_count

        if slept_days == 0:
            s_time = "-"
        else:
            s_time = total_sleep // slept_days

        df = df.append(pd.Series({'group': row['Condition'], 'delay_nights': delay_n_count, 'delay_time': delay,
                                  'sleep_time': s_time}, name=row['ID']))
    #MERGE both files
    merged_dfs = pd.concat([df, survey], axis=1, join="inner")
    # print (df)
    print(merged_dfs.to_string())

    correlation = []
    #STEP 1 CORRELATIONS
    print("1.1 :")
    bp_array = []
    sleep = []
    for i in merged_dfs['bp_scale'].index:
        if not merged_dfs['sleep_time'][i] == "-":
            bp_array.append(merged_dfs['bp_scale'][i])
            sleep.append(merged_dfs['sleep_time'][i])

    print(correlate(bp_array, sleep, 'pearson'))

    print("1.2 :")
    age_array = []
    delay_arr = []
    for i in merged_dfs['age'].index:
        if not merged_dfs['delay_time'][i] == "-":
            age_array.append(merged_dfs['age'][i])
            delay_arr.append(merged_dfs['delay_time'][i])

    print(correlate(age_array, delay_arr, 'kendall'))
    print("1.3 :")

    delayt_arr = []
    dt_arr = []
    for i in merged_dfs['delay_time'].index:
        if not merged_dfs['delay_time'][i] == "-":
            delayt_arr.append(merged_dfs['delay_time'][i])
            dt_arr.append(merged_dfs['daytime_sleepiness'][i])

    print(correlate(delayt_arr, dt_arr, 'pearson'))

    # significant differences between the experimental group and the control group
    print("2.1 :")
    ex_group = []
    con_group = []
    for i in merged_dfs.index:
        if merged_dfs['group'][i] == 1:#experimental
            ex_group.append(merged_dfs['delay_nights'][i])
        else:
            con_group.append(merged_dfs['delay_nights'][i])

    print(compare(ex_group, con_group, 'wilcoxon'))

    print("2.2 :")
    ex_group = []
    con_group = []
    for i in merged_dfs.index:
        if merged_dfs['group'][i] == 1:#experimental
            if not merged_dfs['sleep_time'][i] == "-":
                ex_group.append(merged_dfs['sleep_time'][i])
        else:
            if not merged_dfs['sleep_time'][i] == "-":
                con_group.append(merged_dfs['sleep_time'][i])
    print(compare(ex_group, con_group, 'ttest'))

    print("2.3 :")
    ex_group = []
    con_group = []
    for i in merged_dfs.index:
        if merged_dfs['group'][i] == 1:#experimental
            if not merged_dfs['delay_time'][i] == "-":
                ex_group.append(merged_dfs['delay_time'][i])
        else:
            if not merged_dfs['delay_time'][i] == "-":
                con_group.append(merged_dfs['delay_time'][i])
    print(compare(ex_group, con_group, 'ttest'))

    target = []
    predictors =[]
    for index in merged_dfs.index:
        if not merged_dfs['delay_time'][index] == "-":
            target.append(int(merged_dfs['delay_time'][index]))
            predictors.append([int(merged_dfs['age'][index]),
                               int(merged_dfs['motivation'][index]),
                               int(merged_dfs['daytime_sleepiness'][index])])
    regress(target, predictors)
    visualize(target, predictors)

def read_data(sleepdatafile, surveydatafile): 
    dfsleep = pd.read_csv(sleepdatafile)
    dfsurvey = pd.read_csv(surveydatafile)
    return dfsleep, dfsurvey

def correlate(x, y, test_type = 'pearson'):
    if test_type == 'pearson':
        return scipy.stats.pearsonr(x, y)
    elif test_type == 'kendall':
        return scipy.stats.kendalltau(x, y)

def compare(x, y, test_type = 'ttest'):
    if test_type == 'ttest':
        return scipy.stats.ttest_ind(x, y)
    elif test_type == 'wilcoxon':
        return scipy.stats.ranksums(x, y)

def regress(target, predictors):
    #predictors = sm.add_constant(predictors)

    model = sm.OLS(target, predictors).fit()
    #predictions if necessary
    #predictions = model.predict(predictors)
    print(model.summary())
    # print(target)

"""
Tip: create one function per visualization, and call those functions from the main visualize() function.
"""
def visualize(target,predictors):

    ##########################
    age = []
    motiv = []
    sleep = []
    for i in range(len(predictors)):
        age.append(predictors[i][0])
        motiv.append(predictors[i][1])
        sleep.append(predictors[i][2])

    plt.figure()
    plt.title("Age vs. Delay time")
    plt.xlabel("Age")
    plt.ylabel("Bedtime delay time (seconds)")
    plt.scatter(age, target, s=250)
    plt.show()

    target = [x //4 for x in target]
    plt.figure()
    plt.title("Motivation vs. Daytime Sleepiness")
    plt.xlabel("Motivation")
    plt.ylabel("Sleepiness")
    plt.scatter(motiv, sleep, s=target , alpha = 0.7)
    plt.show()

    age, target = zip(*sorted(zip(age, target)))
    plt.plot(age,target, linewidth=3.0)
    plt.title("Age vs. Bedtime delay time (seconds)")
    plt.ylabel("Bedtime delay time (seconds)")
    plt.xlabel("Age")
    plt.show()

    sleep, motiv = zip(*sorted(zip(sleep, motiv)))
    plt.plot(sleep,motiv, linewidth=3.0)
    plt.title("Motivation vs. Daytime Sleepiness")
    plt.ylabel("Motivation")
    plt.xlabel("Sleepiness")
    plt.show()

    sleep, target = zip(*sorted(zip(sleep, target)))
    plt.bar(sleep,target, width= 0.5)
    plt.title("Age vs. Daytime sleepiness")
    plt.ylabel("delay")
    plt.xlabel("sleep")
    plt.show()


'''
    #changed from https://www.geeksforgeeks.org/python-get-unique-values-list/
    unique_list = []
    unique_list_counter = []
    # traverse for all elements
    for x in age:
        # check if exists in unique_list or not
        if 
        if x not in unique_list:
            unique_list.append(x)
            unique_list_counter.append(1)
            # print list
        else:
            unique_list_counter[unique_list.index(x)] += 1

    print (sleep,unique_list_counter)
    fig = plt.figure()
    plt.title("adsf,")
    plt.xlabel("age")
    plt.ylabel("motiv")
    plt.bar(unique_list_counter, sleep, color="green")
    plt.show()
'''
'''
    target = np.linspace(min(target), max(target), len(target))
    x = np.linspace(min(age), max(age), len(age))
    y = np.linspace(min(motiv), max(motiv), len(motiv))
    x, y = np.meshgrid(x, y)


    region = np.s_[5:50, 5:50]
    print(x,y,target)
    x, y, target = x[region], y[region], target[region]

    # Set up plot
    fig, ax = plt.subplots(subplot_kw=dict(projection='3d'))

    ls = LightSource(270, 45)
    # To use a custom hillshading mode, override the built-in shading and pass
    # in the rgb colors of the shaded surface calculated from "shade".
    rgb = ls.shade(z, cmap=cm.gist_earth, vert_exag=0.1, blend_mode='soft')
    surf = ax.plot_surface(x, y, z, rstride=1, cstride=1, facecolors=rgb,
                           linewidth=0, antialiased=False, shade=False)
    plt.show()
'''

if __name__ == '__main__':
    main(sleepdatafile, surveydatafile)
