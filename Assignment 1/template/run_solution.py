import os
import importlib
import sys
import codecs
import shutil
from subprocess import call

import solution

def header(str):
    print()
    print('-'*40)
    print(str)
    print('-'*40)
  

print('Running solution')
 
points = [0, 2, 5, 5, 3, 5, 5, 10, 10]
for i in range(1,9):
    cmd = solution.commands[i]
    header('Exercise ' + str(i) + ' (' + str(points[i]) + ' points)')
    print(cmd)


header('Exercise 9 (10 points)')
print('Enter a number')
solution.ex9()

header('Exercise 10 (10 points)')
outfile = 'data/outfile.txt'
solution.ex10('data/textfile1.txt', 'data/textfile2.txt', outfile)
if os.path.isfile(outfile):
    with open(outfile) as f:
        print(f.readlines())
    os.remove(outfile)


header('Exercise 11 (10 points)')
solution.ex11('data/dist_matrix.txt')

header('Exercise 12 (15 points)')
solution.ex12('data/draughts.txt')

