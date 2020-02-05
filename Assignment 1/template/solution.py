"""
We truthfully declare:
- to have contributed approximately equally to this assignment [if this is not true, modify this sentence to disclose individual contributions so we can grade accordingly]
- that we have neither helped other students nor received help from other students
- that we provided references for all code that is not our own

Yasin Aydin yasinaydin@sabanciuniv.edu
Faruk Simsekli faruksimsekli.7@gmail.com
"""

import re
import sys

# replace "grep" in the following lines with the correct commands for exercises 1-8
#In Linux the commands are like this
commands = {
1 : """cat hue_upload.csv hue_upload2.csv > hue_combined.csv""",
2 : """cat hue_combined.csv | tr -d '"' | cut -d';' -f2- > hue_combined_cleaned.csv""",
3 : """sort hue_combined_cleaned.csv | uniq > hue.csv""",
4 : """grep -F "lamp_change" hue.csv | wc -l""",
5 : """grep -F "adherence_importance" hue.csv | cut -d';' -f3- | sort -n | uniq""",
6 : """cut -d';' -f1 hue.csv | sort | uniq -c""",
7 : """cut -d';' -f2 hue.csv |  grep -o -P  "([a-z]+(_[a-z]+)*)" | sort | uniq""",
8 : """cut -d';' -f2 hue.csv | grep -F "lamp_change" | grep -o -P "[0-9]{2}_[a-zA-Z]+_[0-9]{4}" | sort | uniq -c"""
}
#In windows the commands are like this
#commands = {
#1 : """cat hue_upload.csv hue_upload2.csv > hue_combined.csv""",
#2 : """cat hue_combined.csv | tr -d ^\^" | cut -d";" -f2- > hue_combined_cleaned.csv""",
#3 : """sort hue_combined_cleaned.csv | uniq > hue.csv""",
#4 : """grep -F "lamp_change" hue.csv | wc -l""",
#5 : """grep -F "adherence_importance" hue.csv | cut -d ';' -f3- | sort -n | uniq""",
#6 : """cut -d";" -f1 hue.csv | sort | uniq -c""",
#7 : """cut -d";" -f2 hue.csv | grep -E([a-z]+(?:_[a-z]+)*) | sort | uniq""",
#8 : """cut -d';' -f2 hue.csv | grep -E "lamp_change" | grep -o -P "[0-9]{2}[a-zA-Z]+[0-9]{4}" | sort | uniq -c"""}

def ex9(): # for exercise 9

    next_input = input()

    # While loop checks if the input is not a digit or has more than 1 digit
    # keeps looping until it got integer with more than 1 digit.
    while (not next_input.isdigit() or int(next_input) < 10):
        next_input = input("Please enter a integer bigger than 9: ")

    # to get the number of digits
    count = 0
    input_as_integer = int(next_input)
    while (input_as_integer > 0):
        count = count + 1
        input_as_integer = input_as_integer // 10
    print(count)

    # number of distinct digits can be found by using set function.
    print(len(set(next_input)))

    # the largest sum of two consecutive digits
    # for every digit but the last one the for loop will sum and change the
    # biggest sum if necessary
    largest_sum = 0
    number_as_string = str(next_input)
    for i in range(len(number_as_string) - 1):
        current_consecutive_sum = int(number_as_string[i]) + int(number_as_string[i + 1])
        if current_consecutive_sum > largest_sum:
            largest_sum = current_consecutive_sum
    print(largest_sum)

    from math import sqrt

    #list to hold primes
    primes = []

    #Following piece of code is inspired from : https://discuss.codecademy.com/t/challenge-sum-of-prime-factors/81035/2
    ###############
    n = int(next_input)
    while n % 2 == 0:  #dividing until we find an odd number.
        primes.append(2)
        n = n // 2
    i = 3
    while i <= sqrt(n):
        while n % i == 0:  #dividing it until it is irreducible.
            primes.append(i)
            n = n // i
        i += 2
    if n > 2:  #appending the last factor.
        primes.append(n)
    ################

    sum = 0
    #summing the different primes
    differen_primes = set(primes)
    for x in differen_primes:
       sum += x
    print (sum)

def ex10(filename1,filename2,outfilename):
    # for file 1 we create list to hold everyline separately
    file1_list = []
    # reading the fileW
    file1 = open(filename1, "r")
    # add each line to the list
    for i in file1:
        file1_list.append(i.strip('\n'))  # removing \n in the string

    # for file 2 same operations
    file2_list = []
    file2 = open(filename2, "r")
    for n in file2:
        file2_list.append(n.strip('\n'))

    # we will user the set to get rid of the duplicates and get the difference
    difference_list = set(file1_list) - set(file2_list)

    # soring the set alphabeticaly
    difference_list = sorted(difference_list)

    output_file = open(outfilename, "a")
    # appending every item in the difference_list to the new file line by line
    for x in difference_list:
        output_file.write(x + "\n")


def minDistance(distance_list, queue):
    minimum = sys.maxsize
    min_index = -1

    for i in range(len(distance_list)):
        if distance_list[i] < minimum and i in queue:
            minimum = distance_list[i]
            min_index = i
    return min_index


def printPath(parent, target):
    x = parent[target - 1]
    the_path = [target - 1]

    while x is not 0:
        the_path.append(x)
        x = parent[x]
    the_path.append(0)

    final_result = "0"
    the_path = list(reversed(the_path))
    for i in range(1, len(the_path)):
        final_result += " > " + str(the_path[i])
    print(final_result)


def ex11(filename):
    inf = sys.maxsize
    inf_string = str(inf)
    source_vertex = 0
    # https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm#Pseudocode
    # https://www.geeksforgeeks.org/printing-paths-dijkstras-shortest-path-algorithm/

    with open(filename, 'r') as f:
        adjacency_matrix = [[num.strip('\n') for num in line.split(' ')] for line in f]

    vertex_number = len(adjacency_matrix[0])
    for i in range(vertex_number):
        for j in range(vertex_number):
            if adjacency_matrix[i][j] == "-":
                adjacency_matrix[i][j] = inf_string

    target = vertex_number
    queue = []
    distance = [inf] * vertex_number
    distance[source_vertex] = 0
    parent_list = [-1] * vertex_number
    for vertex in range(vertex_number):
        queue.append(vertex)

    while queue:
        u = minDistance(distance, queue)
        queue.remove(u)
        for i in range(vertex_number):

            if (adjacency_matrix[u][i] != inf) and i in queue:
                if distance[u] + int(adjacency_matrix[u][i]) < distance[i]:
                    distance[i] = distance[u] + int(adjacency_matrix[u][i])
                    parent_list[i] = u
    final_path = ""
    print(distance[target - 1])
    printPath(parent_list, target)


def ex12(filename):
    width = 10
    height = 10
    # matrix[row number][column number]
    matrix = [[" " for x in range(width)] for y in range(height)]

    file = open(filename, "r")
    xPos = 0
    yPos = 0
    typePiece = ""
    for i in file:
        matches = re.search("\(([0-9]+,[0-9]+)\)\t+[w|W|b|B]", i)
        if matches:
            if i[1].isdigit():
                coor = re.search('([^(^)]+)', i).group(1)
                lst = coor.split(",")
                xPos = int(lst[0])
                yPos = int(lst[1])
                if xPos > 10 or yPos > 10 or 1 > xPos or 1 > yPos:  # the position values should be in range 1-10
                    continue

                typePiece = matches.group(0).split("\t")[len(matches.group(0).split("\t")) - 1]  # extract the type
                # only black squares have piece
                if (abs(xPos - yPos) % 2) == 0:
                    matrix[height - yPos][xPos - 1] = typePiece

    #################STRUCTURE###############
    top_of_matrix = " _______________________________________"
    empty_line_matrix = "|   |   |   |   |   |   |   |   |   |   |"
    #      values will be here |   |   |   |
    bottom_of_cells = "|___|___|___|___|___|___|___|___|___|___|"
    #########################################

    # This will be the one loop of for loop and
    # we will add pieces here for that ROW!
    # since the  print process is row by row
    # "|   |   |   |"
    # "|   |   |   |"
    # "|___|___|___|"

    # printing matrix with values
    print(top_of_matrix)
    current_row = 0
    while current_row < height:
        print(empty_line_matrix)
        pieces_in_cells = ""
        current_column = 0
        while current_column < width:
            # adding 1 cell to the string like this: "| piecetype " for each column
            pieces_in_cells += "| " + matrix[current_row][current_column] + " "
            current_column += 1
        pieces_in_cells += "|"  # adding last missing pipe to the end of string
        print(pieces_in_cells)
        print(bottom_of_cells)
        current_row += 1
