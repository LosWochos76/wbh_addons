#!/usr/bin/python3
# Import weather-data from uni bayreuth into a postgres-database

from datetime import date
import os, ssl, sys, math, wget
import pandas as pd	
from urllib.request import urlopen
from zipfile import ZipFile
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from progress.bar import Bar

if (not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None)):
	ssl._create_default_https_context = ssl._create_unverified_context

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
	print("Importiere Wettermessungen...")
	df = pd.read_csv("wetterdaten_Wettermessung.csv", \
		sep=";", encoding = "ISO-8859-1", decimal=",")
	df = df.iloc[: , :-1]
	df['Datum'] = pd.to_datetime(df['Datum'])
	messungen = df.T.to_dict('dict')
	data = []

	client = InfluxDBClient(url="http://localhost:8086", \
		token="tokentoken", org="wbh")
	write_api = client.write_api(write_options=SYNCHRONOUS)

	bar = Bar('Importiere', max=len(messungen.keys()))
	for key in messungen:
		messung = messungen[key]
		point = Point("wettermessung") \
			.tag("s_id", messung["Stations_ID"]) \
			.time(messung["Datum"])

		fields = []
		for key in messung.keys():
			if key != "Stations_ID" and key != "Datum":
				fields.append(key)

		for key in fields:
			if not math.isnan(messung[key]):
				point = point.field(key, messung[key])

		write_api.write("wbh", "wbh", point)
		bar.next()

	print("Fertig!")
	bar.finish()
except:
	print("Konnte Wetterdataten nicht importieren!")
