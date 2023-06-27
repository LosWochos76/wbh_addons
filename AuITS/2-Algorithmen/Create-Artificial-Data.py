import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt

df = pd.DataFrame(columns=["timestamp", "data"])
df["timestamp"] = pd.date_range(start='2020-11-01', end='2020-11-30 23:00:00', freq="h")
rows = df.shape[0]

season = (np.cos(np.linspace(-np.pi, 61*np.pi, rows))+1.5)*50
f = lambda x: x*3
trend = f(np.linspace(0, 20, rows)) 
residuals = np.random.normal(0, 10, rows)

df["data"] = season + trend + residuals
df.to_csv('komponenten.csv', index=False, decimal=',', sep=';')

df.plot(x='timestamp', y='data')
plt.show()