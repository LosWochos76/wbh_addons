#!/usr/bin/python3
# import the list of renewable powerplants in germany into a postgres database

import os
import pandas as pd
from sqlalchemy import create_engine
import wget
import sys

engine = create_engine('postgresql://postgres:secret@localhost:5432/postgres')

try:
	print("Lösche alte Daten in der Datenbank...")
	with engine.connect() as con:
		con.execute('drop table if exists renewable_power_plants;')
except:
	print("Die Tabelle in der Datenbank konnten nicht gelöscht werden!")
	sys.exit()

if not os.path.exists("renewable_power_plants_DE.csv"):
	zipurl = 'https://data.open-power-system-data.org/renewable_power_plants/2020-08-25/renewable_power_plants_DE.csv'
	try:
		print("Lade CSV-Datei herunter...")
		response = wget.download(zipurl, "renewable_power_plants_DE.csv")
	except:
		print("Datei konnte nicht heruntergeladen werden!")
		sys.exit()

try:
	print("Lade Daten...")
	df = pd.read_csv('renewable_power_plants_DE.csv', sep=',', low_memory=False)
	df['commissioning_date'] = pd.to_datetime(df['commissioning_date'])
	df['decommissioning_date'] = pd.to_datetime(df['decommissioning_date'])

	print("Schreibe Daten in Datenbank...")
	df.to_sql('renewable_power_plants', engine, index=False, if_exists='append', chunksize=100)
except:
	print("Konnte die Daten nicht in die Datenbank importieren")
	sys.exit()

try:
	print("Passe geographische Datentypen an...")
	with engine.connect() as con:
		con.execute('ALTER TABLE renewable_power_plants ADD loc geography;')
		con.execute('update renewable_power_plants set loc=ST_SetSRID(ST_Point(lon, lat)::geography, 4326);')
		con.execute('ALTER TABLE renewable_power_plants DROP COLUMN lon, drop column lat;')
except:
	print("Konnte geographische Datentypen nicht anpassen!")