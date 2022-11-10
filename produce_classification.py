'''Script to produce .csv files for all classified points

The program will take a number of .csv files for individual point classifications.
It will then concatenate them, (randomise the order?) and save them into a master .csv file for classification data points.
'''

import pandas as pd

load_csv_folder = ''
load_csv_files = ['initTest.csv']*3
save_csv_folder = load_csv_folder
save_csv_filename = 'master_classification.csv'

df_master = pd.DataFrame(data = {})
print(df_master)

for f in load_csv_files:
    df = pd.read_csv(load_csv_folder + f)
    df_master = pd.concat([df_master, df],ignore_index=True)

print(df_master)
df_master.to_csv(save_csv_folder + save_csv_filename)

