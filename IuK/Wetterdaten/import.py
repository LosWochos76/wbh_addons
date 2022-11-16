#!/usr/bin/python3
# Import weather-data from uni bayreuth into a postgres-database

from datetime import date
import os, ssl
import pandas as pd
from pandas.io import sql
from sqlalchemy import create_engine
from io import BytesIO
from urllib.request import urlopen
from zipfile import ZipFile
import sys
import wget

def makeInt(df, name):
    df[name] = df[name].astype(int)

if (not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None)):
	ssl._create_default_https_context = ssl._create_unverified_context

engine = create_engine('postgresql://postgres:secret@localhost:5432/postgres')

try:
	with engine.connect() as con:
		con.execute('drop table if exists wetterstation;')
		con.execute('drop table if exists wettermessung;')
except:
	print("Die Tabelle in der Datenbank konnten nicht gelöscht werden!")
	sys.exit()

if not os.path.exists("wetterdaten.zip"):
	today = date.today()
	d = today.strftime("%Y-%m-%d")
	zipurl = 'https://dbup2date.uni-bayreuth.de/downloads/wetterdaten/{}_wetterdaten_CSV.zip'.format(d)
	print("Lade ZIP-Datei herunter...")
	response = wget.download(zipurl, "wetterdaten.zip")

try:
	print("Entpacke ZIP-Datei...")
	with ZipFile("wetterdaten.zip", 'r') as zip_ref:
		zip_ref.extractall()
except:
	print("Die ZIP-Datei konnte nicht entpackt werden!")
	sys.exit()

try:
	print("Importiere Wetterstationen...")
	cols = ['S_ID', 'Standort', 'Geo_Breite', 'Geo_Laenge', 'Hoehe', 'Betreiber']
	df = pd.read_csv("wetterdaten_Wetterstation.csv", sep=";", encoding = "ISO-8859-1", decimal=",", usecols=cols)
	df.columns = ['s_id','standort','geo_breite','geo_laenge','hoehe','betreiber']
	df['s_id'] = df['s_id'].astype(int)
	df['geo_breite'] = df['geo_breite'].astype(float)
	df['geo_laenge'] = df['geo_laenge'].astype(float)
	df['hoehe'] = df['hoehe'].astype(float)
	df.to_sql('wetterstation', engine, index=False, if_exists='replace')
except:
	print("Import der Wetterstationen fehlgeschlagen!")
	sys.exit()

try:
	print("Importiere Wettermessungen...")
	df = pd.read_csv("wetterdaten_Wettermessung.csv", sep=";",
		encoding = "ISO-8859-1", decimal=",", 
		usecols={"Stations_ID", "Datum", "Qualitaet", "Min_5cm", "Min_2m", "Mittel_2m",
		"Max_2m","Relative_Feuchte","Mittel_Windstaerke","Max_Windgeschwindigkeit",
		"Sonnenscheindauer","Mittel_Bedeckungsgrad","Niederschlagshoehe","Mittel_Luftdruck"})
	df.columns = ['stations_id','datum','qualitaet','min_5cm','min_2m','mittel_2m',
		"max_2m","relative_feuchte","mittel_windstaerke","max_windgeschwindigkeit",
		"sonnenscheindauer","mittel_bedeckungsgrad","niederschlagshoehe","mittel_luftdruck"]
	df['stations_id'] = df['stations_id'].astype(int)
	df['datum'] = pd.to_datetime(df['datum'])
	df['qualitaet'] = df['qualitaet'].astype(pd.Int32Dtype())
	df['min_5cm'] = df['min_5cm'].astype(float)
	df['min_2m'] = df['min_2m'].astype(float)
	df['mittel_2m'] = df['mittel_2m'].astype(float)
	df['max_2m'] = df['max_2m'].astype(float)
	df['relative_feuchte'] = df['relative_feuchte'].astype(float)
	df['mittel_windstaerke'] = df['mittel_windstaerke'].astype(float)
	df['max_windgeschwindigkeit'] = df['max_windgeschwindigkeit'].astype(float)
	df['sonnenscheindauer'] = df['sonnenscheindauer'].astype(float)
	df['mittel_bedeckungsgrad'] = df['mittel_bedeckungsgrad'].astype(float)
	df['niederschlagshoehe'] = df['niederschlagshoehe'].astype(float)
	df['mittel_luftdruck'] = df['mittel_luftdruck'].astype(float)
	df.to_sql('wettermessung', engine, index=False, if_exists='replace')
except:
	print("Import der Wettermessungen fehlgeschlagen!")
	sys.exit()

try:
	with engine.connect() as con:
		print("Passe geographische Daten an...")
		con.execute('alter table wetterstation add column location geography;')
		con.execute('update wetterstation set location=ST_SetSRID(ST_MakePoint(Geo_Laenge, Geo_Breite), 4326);')
		con.execute('ALTER TABLE wetterstation DROP COLUMN Geo_Laenge;')
		con.execute('ALTER TABLE wetterstation DROP COLUMN Geo_Breite;')
except:
	print("Konnte geographische Daten nicht anpassen!")
	sys.exit()

print("Fertig!")