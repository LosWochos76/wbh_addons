import pandas as pd 
import matplotlib.pyplot as plt
import os.path
from statsmodels.tsa.seasonal import seasonal_decompose

# Run the Script 'Create-Artificial-Data.py' first:
if not os.path.isfile('komponenten.csv'):
    print("Bitte lassen Sie zunächst das Python-Script 'Create-Artificial-Data' laufen!")
    quit()

df = pd.read_csv('komponenten.csv', delimiter=";", decimal=",")
df['timestamp'] = pd.to_datetime(df['timestamp'])

df = df.set_index("timestamp")
result = seasonal_decompose(df, model='additive', period=24)

result.plot()
plt.show()