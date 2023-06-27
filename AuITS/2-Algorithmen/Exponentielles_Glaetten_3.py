import pandas as pd
import matplotlib.pyplot as plt
import os.path
from statsmodels.tsa.holtwinters import ExponentialSmoothing

# Run the Script 'Create-Artificial-Data.py' first:
if not os.path.isfile('komponenten.csv'):
    print("Bitte lassen Sie zunächst das Python-Script 'Create-Artificial-Data' laufen!")
    quit()

df = pd.read_csv('komponenten.csv', delimiter=";", decimal=",")
df['timestamp'] = pd.to_datetime(df['timestamp'])

fit = ExponentialSmoothing(df["data"], trend='add', \
    seasonal='add', seasonal_periods=24).fit()
fcast = fit.forecast(48)

fcast.plot()
fit.fittedvalues.plot()
plt.show()