#!/usr/bin/env python

"""
We truthfully declare:
- to have contributed approximately equally to this assignment [if this is not true, modify this sentence to disclose individual contributions so we can grade accordingly]
- that we have neither helped other students nor received help from other students
- that we provided references for all code that is not our own

Yasin Aydin yasinaydin@sabanciuniv.edu
Faruk Simsekli faruksimsekli.7@gmail.com
"""

# Include these lines without modifications
# Call the script as follows: ./<scriptname> <csv_filename> <mapper function> <reducer function>
# So, for example: ./template_assignment3.py hue_week_3_2017.csv mapper1 reducer1
# This will call the mapper1 function for each line of the data, sort the output, and feed the sorted output into reducer1
import sys
from io import StringIO
import traceback
from queue import Queue
import requests
import json
import threading

# Implement these mapper and reducer functions
count_bigger_50 = 0
current_count_fitness = 1
current_sum_fitness = 0
current_id = None

def mapper1(line):
    line_list = line.split(",")
    if line_list[5] is not "":
        print(line_list[5])
    
def reducer1(line):
    global count_bigger_50
    if line is not "":
        if float(line) > 50:
            count_bigger_50 += 1
    else:
        print(count_bigger_50)
    
def mapper2(line):
    line_list = line.split(",")
    print("{}\t{}".format(line_list[1], line_list[5]))

def reducer2(line):
    global current_id, current_count_fitness, current_sum_fitness    
    #print(line)
    if line is not "":
        user_id, fitness = line.split("\t")
        if user_id is not "" and fitness is not "":
            fitness = float(fitness)
            #print(current_id, user_id, fitness)
            #print(current_id == user_id)
            if current_id == user_id:
                current_count_fitness += 1
                current_sum_fitness += fitness
                #print(current_id, user_id, current_sum_fitness)
            else:
                #print("AT")
                if current_id is not None:
                    #print(current_id, current_sum_fitness, current_count_fitness)
                    print("{}\t{}".format('%7s' % current_id, "%.2f" % (current_sum_fitness/current_count_fitness)))
                current_count_fitness = 1
                current_sum_fitness = fitness
                current_id = user_id


if(len(sys.argv) == 4):
    data = sys.argv[1]
    mapper = sys.argv[2]
    reducer = sys.argv[3]
else:
    data = 'map_reduce_hue.csv'
    mapper = 'mapper1'
    reducer = 'reducer1'

# Include these lines without modifications
 
if 'old_stdout' not in globals():
    old_stdout = sys.stdout
mystdout = StringIO()
sys.stdout = mystdout


with open(data) as file:
    try:
        for index, line in enumerate(file):
            if index == 0:
                continue
            line = line.strip()
            locals()[mapper](line)
        locals()[mapper](',,,,,,,') 
    except:
        sys.stdout = old_stdout
        print('Error in ' + mapper)
        print('The mapper produced the following output before the error:')
        print(mystdout.getvalue())
        traceback.print_exc()

    sys.stdout = old_stdout
    mapper_lines = mystdout.getvalue().split("\n")

    for index, line in enumerate(sorted(mapper_lines)):
        if index == 0:
            continue
        locals()[reducer](line)
    locals()[reducer]('')

mystdout.close()
