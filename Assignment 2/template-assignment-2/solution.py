"""
We truthfully declare:
- to have contributed approximately equally to this assignment [if this is not true, modify this sentence to disclose individual contributions so we can grade accordingly]
- that we have neither helped other students nor received help from other students
- that we provided references for all code that is not our own

Yasin Aydin yasinaydin@sabanciuniv.edu
Faruk Simsekli faruksimsekli.7@gmail.com
"""
import pandas as pd
import warnings
import re
import datetime
from datetime import time, date, timedelta
import time as t
import pymongo
import pprint

def read_csv_data(filenames):
    warnings.simplefilter(action='ignore', category=FutureWarning)
    dic_months = {'januari': 1, 'februari': 2, 'maart': 3, 'april': 4,
                  'mei': 5, 'juni': 6, 'juli': 7, 'augustus': 8,
                  'september': 9, 'oktober': 10, 'november': 11, 'december': 12}

    df = pd.DataFrame()
    counter = 0
    start = t.time()
    for files in filenames:
        with open(files) as file:
            experiment_group_list = []
            for line in file:
                counter += 1
                dic = {'bedtime': None, 'intended_bedtime': None,
                       'risetime': None, 'rise_reason': "",
                       'fitness': None, 'adherence_importance': 0,
                       'in_experimental_group': "False"}
                line_list = line.split(";")
                user_id = int(line_list[1][1:-1])
                event_info = line_list[2]
                value = line_list[3][1:-2]
                # getting the date info
                all_date = re.search("([0-9]+_[a-z]*_+[0-9]*)", event_info)

                if not all_date:
                    continue
                date_list = all_date.group(0).split("_")
                day = int(date_list[0])
                month = dic_months[date_list[1]]
                year = int(date_list[2])

                # getting the time
                # datetime object
                date = datetime.datetime(year, month, day, 0, 0, 0)
                index = (date, user_id)

                all_time = re.search("[0-9]{2}_[0-9]{2}_[0-9]{2}_[0-9]{3}", event_info)
                if all_time:
                    time_list = all_time.group(0).split("_")
                    hour = int(time_list[0])
                    minute = int(time_list[1])
                    second = int(time_list[2])
                    c_time = datetime.time(hour, minute, second)

                    if "lamp_change" in event_info:
                        # print("Inside == > lamp_change")

                        if value == "OFF":

                            dic['bedtime'] = c_time
                            if index not in df.index:
                                df = df.append(pd.Series(dic, name=index))
                                # print("IT IS NOT IN DF SO APPEND IT!\n")
                            else:
                                # print("IT IS IN DATAFRAME SO CHANGE IT IF BIGGER!")
                                # if does exist check and update if necessary
                                if df['bedtime'][index] == None:
                                    df.set_value(index, 'bedtime',c_time)
                                elif c_time > df['bedtime'][index]:
                                    df.set_value(index, 'bedtime',c_time)
                                    # print("1bedtime changed to: ", df['bedtime'][index], "\n")
                                    # print(df.to_string())

                elif "risetime" in event_info:
                    # print("Inside == > risetime")
                    if value == "":
                        time = None
                    else:
                        all_time = re.search("([^\"]+)", value)
                        if not all_time:
                            time = None
                            continue
                        all_time = all_time.group(0)
                        if len(all_time) == 1 or len(all_time) == 2:
                            # print(all_time + ":00")
                            time = datetime.time(int(all_time))
                        else:
                            # print(all_time[:-2] + ":" + all_time[-2:])
                            time = datetime.time(int(all_time[:-2]), int(all_time[-2:]))

                    index = (date, user_id)
                    dic['risetime'] = time
                    if index not in df.index:
                        df = df.append(pd.Series(dic, name=index))
                    else:
                        df.set_value(index, 'risetime', time)
                        # print("risetime changed to: ", df['risetime'][index], "\n")
                        # print(df.to_string())

                elif "bedtime_tonight" in event_info:
                    #print("Inside == > intended_bedtime")
                    if value == "":
                        continue
                    else:
                        str_value = re.search("([^\"]+)", value).group(0)
                        int_value = int(str_value)

                        if int_value < 6:
                            time = datetime.time(int_value, 0, 0)
                        elif int_value >= 6 and int_value < 12:
                            time = datetime.time(int_value + 12, 0, 0)
                        elif int_value == 12:
                            time = datetime.time(0, 0, 0)
                        elif int_value >= 13 and int_value <= 17:
                            time = datetime.time(int_value - 12, 0, 0)
                        elif int_value < 24:
                            time = datetime.time(int_value, 0, 0)
                        elif int_value == 24:
                            time = datetime.time(0, 0, 0)
                        elif int_value <= 59:
                            time = datetime.time(0, int_value, 0)
                        elif int_value >= 100 and int_value <= 159:
                            time = datetime.time(1, int_value % 100, 0)
                        elif int_value >= 200 and int_value <= 259:
                            time = datetime.time(2, int_value % 100, 0)
                        elif int_value >= 300 and int_value <= 359:
                            time = datetime.time(3, int_value % 300, 0)
                        elif int_value >= 700 and int_value <= 759:
                            time = datetime.time(19, int_value % 700, 0)
                        elif int_value >= 800 and int_value <= 859:
                            time = datetime.time(20, int_value % 800, 0)
                        elif int_value >= 900 and int_value <= 959:
                            time = datetime.time(21, int_value % 900, 0)
                        elif int_value >= 1000 and int_value <= 1059:
                            time = datetime.time(22, int_value % 1000, 0)
                        elif int_value >= 1100 and int_value <= 1159:
                            time = datetime.time(23, int_value % 1100, 0)
                        elif int_value >= 1200 and int_value <= 1259:
                            time = datetime.time(0, int_value % 1200, 0)
                        elif int_value >= 1800 and int_value <= 1859:
                            time = datetime.time(18, int_value % 1800, 0)
                        elif int_value >= 1900 and int_value <= 1959:
                            time = datetime.time(19, int_value % 1900, 0)
                        elif int_value >= 2000 and int_value <= 2059:
                            time = datetime.time(20, int_value % 2000, 0)
                        elif int_value >= 2100 and int_value <= 2159:
                            time = datetime.time(21, int_value % 2100, 0)
                        elif int_value >= 2200 and int_value <= 2259:
                            time = datetime.time(22, int_value % 2200, 0)
                        elif int_value >= 2300 and int_value <= 2359:
                            time = datetime.time(23, int_value % 2300, 0)
                        elif int_value == 2400:
                            time = datetime.time(0, 0, 0)
                        else:
                            continue

                    dic['intended_bedtime'] = time

                    if index not in df.index:
                        df = df.append(pd.Series(dic, name=index))
                    else:
                        df.set_value(index, 'intended_bedtime', time)
                        # print("intended_bedtime changed to", df['intended_bedtime'][index])
                        # print(df.to_string())


                elif "rise_reason" in event_info:
                    #print("Inside == > rise_reason")

                    dic['rise_reason'] = value

                    if index not in df.index:
                        df = df.append(pd.Series(dic, name=index))
                    else:
                        df.set_value(index, 'rise_reason', value)
                        # print("rise_reason changed to", df['rise_reason'][index])
                        # print(df.to_string())

                elif "fitness" in event_info:
                    # print("Inside == > fitness")

                    dic['fitness'] = value

                    if index not in df.index:
                        df = df.append(pd.Series(dic, name=index))
                    else:
                        df.set_value(index, 'fitness', value)
                        # print("fitness changed to", df['fitness'][index])
                        # print(df.to_string())

                elif "adherence_importance" in event_info:
                    # print("Inside == > adherence_importance")

                        dic['adherence_importance'] = value

                        if index not in df.index:
                            df = df.append(pd.Series(dic, name=index))
                        else:
                            df.set_value(index, 'adherence_importance', value)
                            # print("adherence_importance changed to", df['adherence_importance'][index])
                            # print(df.to_string())

                elif "nudge_time" in event_info:
                    #print("Inside == > in_experimental_group")
                    experiment_group_list.append(user_id)

            for index, row in df.iterrows():
                if index[1] in set(experiment_group_list):
                    df.set_value(index, 'in_experimental_group', True)

            # print(file)
            # print(df.to_string())
            # print(t.time() - start)
    return df

def to_mongodb(df):

    date_list = []
    for index in df.index:
        date_list.append(index[0])
    client = pymongo.MongoClient("localhost", 27017)
    db = client['BigData']
    sleepdata = db['sleepdata']
    sleepdata.delete_many({})
    for index in df.index:
        sleep_dur = "-"
        yesterday_tuple = (index[0]-datetime.timedelta(hours = 24), index[1])
        if yesterday_tuple in df.index:
            if index[0]-datetime.timedelta(hours = 24) in date_list:
                if df.get_value(yesterday_tuple, 'bedtime') is not None and df.get_value(index, 'risetime') is not None:
                    rise = datetime.datetime(index[0].year, index[0].month, index[0].day, df['risetime'][index].hour, df['risetime'][index].minute, df['risetime'][index].second)
                    bed = datetime.datetime(yesterday_tuple[0].year, yesterday_tuple[0].month, yesterday_tuple[0].day, df['bedtime'][yesterday_tuple].hour, df['bedtime'][yesterday_tuple].minute, df['bedtime'][yesterday_tuple].second)
                    sleep_dur = rise - bed
                    sleep_dur = int(sleep_dur.total_seconds()) % 86400
                    if sleep_dur > 43200:
                        sleep_dur = "-"
                    # print(rise, bed, "SLEEP DURATION:", str(sleep_dur))

        if not df['bedtime'][index] == None:
            bedtime_str = str('%02d' %df['bedtime'][index].hour) + ":" + str('%02d' %df['bedtime'][index].minute) + ":" + str('%02d' %df['bedtime'][index].second)
        else:
            bedtime_str = "-"

        if not df['intended_bedtime'][index] == None:
            intended_str = str('%02d' %df['intended_bedtime'][index].hour) + ":" + str('%02d' %df['intended_bedtime'][index].minute) + ":" + str('%02d' %df['intended_bedtime'][index].second)
        else:
            intended_str = "-"

        if not df['risetime'][index] == None:
            risetime_str = str('%02d' %df['risetime'][index].hour) + ":" + str('%02d' %df['risetime'][index].minute) + ":" + str('%02d' %df['risetime'][index].second)
        else:
            risetime_str = "-"

        if not df['fitness'][index] == None:
            fit_str = float(df['fitness'][index])
        else:
            fit_str = "-"

        if not df['rise_reason'][index] == "":
            reason_str = str(df['rise_reason'][index])
        else:
            reason_str = "-"

        if not df['adherence_importance'][index] == 0 and not df['adherence_importance'][index] == "0":
            ad_str = float(df['adherence_importance'][index])
        else:
            ad_str = "-"


        sleepdata.insert_one({  'date': index[0], 'user': index[1], 'bedtime': bedtime_str
                                          , 'intended': intended_str, 'risetime': risetime_str
                                          , 'reason': reason_str, 'fitness': fit_str
                                          , 'adh': str(ad_str), 'in_exp': str(df['in_experimental_group'][index])
                                          , 'sleep_duration' : str(sleep_dur)})

def read_mongodb(filter, sort):
    client = pymongo.MongoClient('localhost', 27017)
    db = client.BigData
    sleepdata = db['sleepdata']
    print("%20s\t%10s\t%10s\t%10s\t%10s\t%10s\t%10s\t%10s\t%10s\t%15s" % ("date", "user", "bedtime", "intended", "risetime", "reason", "fitness", "adh", "in_exp", "sleep_duration"))

    for doc in sleepdata.find(filter).sort(sort, pymongo.ASCENDING):
        print("%20s\t%10s\t%10s\t%10s\t%10s\t%10s\t%10s\t%10s\t%10s\t%15s" % (doc['date'], doc['user'], doc['bedtime'], doc['intended'], doc['risetime'], doc['reason'], doc['fitness'], doc['adh'], doc['in_exp'], doc['sleep_duration']))


# if __name__ == '__main__':

    # this code block is run if you run solution.py (instead of run_solution.py)
    # it is convenient for debugging

    # df = read_csv_data(["hue_upload.csv", "hue_upload2.csv"])
    # to_mongodb(df)
    # read_mongodb({}, '_id')
