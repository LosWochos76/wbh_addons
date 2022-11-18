#!/usr/bin/python3
# Import weather-data from uni bayreuth into a postgres-database

from datetime import date
import os, ssl, time, sys, wget, math
import pandas as pd
from pandas.io import sql
from io import BytesIO
from urllib.request import urlopen
from zipfile import ZipFile
from influxdb_client import WritePrecision, InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

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
	print("Importiere Wetterstationen...")
	cols = ['S_ID', 'Standort', 'Geo_Breite', 'Geo_Laenge', 'Hoehe', 'Betreiber']
	df = pd.read_csv("wetterdaten_Wetterstation.csv", sep=";", encoding="ISO-8859-1", decimal=",", usecols=cols)
	stationen = df.set_index('S_ID').T.to_dict('dict')
except:
	print("Import der Wetterstationen fehlgeschlagen!")
	sys.exit()

#try:
print("Importiere Wettermessungen...")
df = pd.read_csv("wetterdaten_Wettermessung.csv", sep=";", encoding = "ISO-8859-1", decimal=",")
df = df.iloc[: , :-1]
df['Datum'] = pd.to_datetime(df['Datum'])
messungen = df.T.to_dict('dict')
data = []

client = InfluxDBClient(url="http://localhost:8086", org="WBH", username="wbh", password="secret123")
query_api = client.query_api()
write_api = client.write_api(write_options=SYNCHRONOUS)

for key in messungen:
	messung = messungen[key]
	station = stationen[messung['Stations_ID']]
	point = "wetterdaten,s_id=" + str(key) + " "

	if not math.isnan(messung['Qualitaet']):
		point += "qualitaet=" + str(messung['Qualitaet']) + ","
	
	if not math.isnan(messung['Min_5cm']):
		point += "min_5cm=" + str(messung['Min_5cm']) + ","
	
	if not math.isnan(messung['Min_2m']):
		point += "min_2m=" + str(messung['Min_2m']) + ","
		
	if not math.isnan(messung['Mittel_2m']):
		point += "mittel_2m=" + str(messung['Mittel_2m']) + ","

	if not math.isnan(messung['Max_2m']):
		point += "max_2m=" + str(messung['Max_2m']) + ","

	if not math.isnan(messung['Relative_Feuchte']):
		point += "relative_feuchte=" + str(messung['Relative_Feuchte']) + ","
	
	if not math.isnan(messung['Mittel_Windstaerke']):
		point += "mittel_windstaerke=" + str(messung['Mittel_Windstaerke']) + ","

	if not math.isnan(messung['Max_Windgeschwindigkeit']):
		point += "max_windstaerke=" + str(messung['Max_Windgeschwindigkeit']) + ","
		
	if not math.isnan(messung['Sonnenscheindauer']):
		point += "sonnenscheindauer=" + str(messung['Sonnenscheindauer']) + ","
	
	if not math.isnan(messung['Mittel_Bedeckungsgrad']):
		point += "mittel_bedeckungsgrad=" + str(messung['Mittel_Bedeckungsgrad']) + ","
	
	if not math.isnan(messung['Niederschlagshoehe']):
		point += "niederschlagshoehe=" + str(messung['Niederschlagshoehe']) + ","
	if not math.isnan(messung['Mittel_Luftdruck']):
		point += "mittel_luftdruck=" + str(messung['Mittel_Luftdruck']) + ","
		
	if point.endswith(","):
		point = point[:-1]
	
	point += " " + str(int(time.mktime(messung['Datum'].timetuple())))
	try:
		write_api.write(bucket="wetterdaten", record=point)
	except:
		pass

print("Fertig!")