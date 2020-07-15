import os,glob
import pandas as pd

folder = '/home/cak/Desktop/TR_HES_Basins/Data/Results/old'

os.chdir(folder)

files = glob.glob('*.csv')
df_all = pd.DataFrame()

for file in files:
    df = pd.read_csv(file)
    df_all = df_all.append(df)

df_all.to_csv('Results.csv')