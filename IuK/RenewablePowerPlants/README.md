# Anleitung zum Import der EE-Anlagen in die PostGIS-Datenbank

1. Als Voraussetzung für diese Schritte muss auf dem Rechner eine PostGIS-Datenbank laufen. Eine Anleitung dazu finden Sie [hier](https://github.com/LosWochos76/wbh_addons/blob/main/IuK/DockerInstallation/README.md).

2. Laden Sie die Datei ```renewable_power_plants_DE.csv``` von der Web-Seite der [Open Power System Data Intitative](https://open-power-system-data.org/) herunter. Die Datei finden Sie unter "Renewable Power Plants". Die Datei ist aktuell ca. 330 MB groß.s

3. Öffnen Sie in ihrer lokalen [pgAdmin-Installation](http://localhost:8080) das Query-Tool. Geben Sie den folgenden SQL-Befehl ein: <br><br> 
```
CREATE TABLE renewable_power_plants
(
    commissioning_date timestamp without time zone,
    decommissioning_date timestamp without time zone,
    energy_source_level_1 text,
    energy_source_level_2 text,
    energy_source_level_3 text,
    technology text,
    electrical_capacity double precision,
    voltage_level text,
    tso text,
    dso text,
    dso_id double precision,
    eeg_id text,
    federal_state text,
    postcode double precision,
    municipality_code double precision,
    municipality text,
    address text,
    data_source text,
    comment text,
    lon double precision,
	lat double precision
);
```