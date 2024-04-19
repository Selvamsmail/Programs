import pandas as pd 
import os 
import datetime

naufile_names = [i for i in os.listdir() if 'Naukri_raw' in i]
df = pd.DataFrame()
for i in naufile_names:
    if 'bak' not in i:    
        tdf = pd.read_parquet(i)
        df = pd.concat([df,tdf],ignore_index=True)
current_date = datetime.datetime.now().date()
df.to_parquet('completed extracts/Naukri_Extract_'+str(current_date)+'.parquet',index=False)
for i in naufile_names:
    os.remove(i)

linfile_names = [i for i in os.listdir() if 'links.par' in i]
df = pd.DataFrame()

for i in linfile_names:
    if 'bak' not in i:    
        tdf = pd.read_parquet(i)
        df = pd.concat([df,tdf],ignore_index=True)
current_date = datetime.datetime.now().date()
df.to_parquet('completed extracts/links_Extract_'+str(current_date)+'.parquet',index=False)
for i in linfile_names:
    os.remove(i)

jsonvariables = [i for i in os.listdir() if '.json' in i]
for i in jsonvariables:
    os.remove(i)