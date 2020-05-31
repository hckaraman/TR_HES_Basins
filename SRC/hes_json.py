import json
import os


# Opening JSON file

f = open('/home/cak/Desktop/TR_HES_Basins/Data/Hes.json', )
data = json.load(f)

for i in range(1000):
    name = data['results'][2]['attributes']['HES Adı']
