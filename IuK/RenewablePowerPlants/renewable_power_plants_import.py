#!/usr/bin/python3
# import the list of renewable powerplants in germany into a postgres database

from datetime import date
import os
import pandas as pd
from sqlalchemy import create_engine
import wget

engine = create_engine('postgresql://postgres:secret@localhost:5432/postgres')

try:
	print("Lösche alte Daten in der Datenbank...")
	with engine.connect() as con:
		con.execute('drop table renewable_power_plants;')
except:
	print("Einige Tabellen konnten nicht gelöscht werden!");

today = date.today()
d = today.strftime("%Y-%m-%d")
zipurl = 'https://data.open-power-system-data.org/renewable_power_plants/{}/renewable_power_plants_DE.csv'.format(d)

try:
	response = wget.download(zipurl, "renewable_power_plants_DE.csv")
except:
	print("Datei konnte nicht heruntergeladen werden!");

#try:
print("Lade Daten...")
df = pd.read_csv('renewable_power_plants_DE.csv', sep=',')
#df['commissioning_date'] = pd.to_datetime(df['commissioning_date'])
#df['decommissioning_date'] = pd.to_datetime(df['decommissioning_date'])

print("Schreibe Daten in Datenbank...")
df.to_sql('renewable_power_plants', engine, index=False, if_exists='append', chunksize=100)
#except:
#	print("Konnte die Daten nicht in die Datenbank importieren")

try:
	print("Lösche CSV-Dateien...")
	os.remove("renewable_power_plants_DE.csv")
except:
	print("Die heruntergeladene Datei konnten nicht gelöscht werden!")