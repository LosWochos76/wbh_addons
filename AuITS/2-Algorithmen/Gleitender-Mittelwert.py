import pandas as pd 
import matplotlib.pyplot as plt
import os.path

# Run the Script 'Create-Artificial-Data.py' first:
if not os.path.isfile('komponenten.csv'):
    print("Bitte lassen Sie zunächst das Python-Script 'Create-Artificial-Data' laufen!")
    quit()

df = pd.read_csv('komponenten.csv', delimiter=";", decimal=",")
df['timestamp'] = pd.to_datetime(df['timestamp'])

df["ma"] = df["data"].rolling(window=24, center=True).mean()
df.plot(x="timestamp", y=["data", "ma"])
plt.show()