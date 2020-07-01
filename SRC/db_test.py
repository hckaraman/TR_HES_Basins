from sqlalchemy import create_engine
import pandas as pd
import matplotlib.pyplot as plt
import datetime

engine = create_engine('postgresql://postgres:kalman@localhost:5432/test')

query = """select s."Enlem" ,s."Boylam" ,s."Ortalama_Sıcaklık" from "Sicaklik" s where s."Model" = 'HadGEM2-ES' and s."Senaryo" ='RCP8.5' and s."Ay" =1 and s."Yıl" =2020;"""
df = pd.read_sql(query, engine)
lon = df['Boylam'].values
lat = df['Enlem'].values
temp_ = df['Ortalama_Sıcaklık'].values

print("a")