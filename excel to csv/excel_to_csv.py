import os
import pandas as pd

current_directory = os.getcwd()
files = [f for f in os.listdir(current_directory) if os.path.isfile(os.path.join(current_directory, f))]
filename = []

for i in files:
    if i.endswith('xlsx'):
        filename.append(i)
        print(i)

for i in filename:
    df = pd.read_excel(i)
    c = i.replace('xlsx','csv')
    df.to_csv(c,index=False)