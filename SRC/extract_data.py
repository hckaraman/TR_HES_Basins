from sqlalchemy import create_engine
import pandas as pd
import matplotlib.pyplot as plt
import datetime
from dateutil.relativedelta import relativedelta
import os, time, glob

folder = os.path.abspath(__file__ + '/../..')
result_folder = os.path.join(folder, 'Data', 'Results')
start = time.time()

engine = create_engine('postgresql://postgres:kalman@localhost:5432/clima')

date = datetime.datetime(2015, 1, 1)

# models = ['MPI-ESM-MR', 'CNRM-CM5']

models = ['HadGEM2-ES']

# senaryos = ['RCP4.5', 'RCP8.5']
senaryos = ['RCP8.5']

query = """select  distinct (bid) from basin b"""
basins = pd.read_sql(query, engine)
basins = basins['bid'].values.tolist()

rows_list = []

id = 1


d_file = os.path.join(folder,'Done.csv')

done_stations = []
with open(d_file) as f:
    for line in f.readlines():
        line = line.replace('\n', '')
        done_stations.append(line)

for model in models:
    for senaryo in senaryos:
        for basin in basins:

            if basin not in done_stations:

                rows_list = []

                # havza = h.strip(".shp")[1:]
                for y in range(2015, 2090):
                    for m in range(1, 13):
                        res = []

                        query = f"""select sum(d.discharge) from discharge d where d.yil = {y} and d.ay = {m} and d.model  = '{model}' and d.senaryo  = '{senaryo}' and d.drenajno  in (select hp.hydroid from hru_points hp join basin_points on ST_Contains(basin_points.geom,hp.p_geom) WHERE basin_points.bid  = '{basin}')"""
                        df = pd.read_sql(query, engine)

                        data = {'id': id, 'Drenaj_No': basin, 'Ay': m, 'Yil': y,
                                'Discharge': df['sum'].values[0],
                                'Model': model, 'Senaryo': senaryo}
                        rows_list.append(data)
                        print(id, m, y, senaryo, model, basin)
                        id += 1
                csv_name = basin + '_' + model + '_' + senaryo + '_.csv'
                df = pd.DataFrame(rows_list)
                df.to_csv(os.path.join(result_folder, csv_name))
            else:
                pass
# df = pd.DataFrame(rows_list)

end = time.time()
hours, rem = divmod(end - start, 3600)
minutes, seconds = divmod(rem, 60)
print("Elapsed Time : {:0>2}:{:0>2}:{:05.2f}".format(int(hours), int(minutes), seconds))
