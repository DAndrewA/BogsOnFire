'''Script to produce .csv files for all classified points

The program will take a number of .csv files for individual point classifications.
It will then concatenate them, (randomise the order?) and save them into a master .csv file for classification data points.
'''

import pandas as pd
import json

load_csv_folder = 'data/classification/'
load_csv_files = ['PeatlandData.csv','BurntData.csv','ClearedData.csv','AgricultureData.csv','PlantationData.csv']
save_csv_folder = load_csv_folder
save_csv_filename = 'master_classification.csv'

df_master = pd.DataFrame(data = {})

for i, f in enumerate(load_csv_files):
    df = pd.read_csv(load_csv_folder + f)
    #print(df['.geo'])
    #print(df['.geo'].values)
    json_vals = df['.geo'].values[0]
    vals = json.loads(json_vals)
    
    coords = vals['coordinates']
    classification = [i+1] * len(coords)

    df = pd.DataFrame(data = {'coords':coords, 'classification': classification})

    df_master = pd.concat([df_master, df],ignore_index=True)


#print(df_master)
df_master.to_csv(save_csv_folder + save_csv_filename)

