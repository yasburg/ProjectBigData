import os
import importlib
import sys

import solution

def header(str):
    print()
    print('-'*40)
    print(str)
    print('-'*40)

print('Running solution')

header('Reading csv file')
df = solution.read_csv_data(["hue_upload.csv","hue_upload2.csv"])
header('Inserting into mongodb')
solution.to_mongodb(df)
header('Reading from mongodb')
solution.read_mongodb({},'_id')
