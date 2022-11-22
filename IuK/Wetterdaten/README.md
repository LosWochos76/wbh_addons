# Anleitung zum Import von Wetterdaten in die PostGIS-Datenbank

1. Als Voraussetzung für den Import der Wetterdaten muss auf dem Rechner eine PostGIS-Datenbank installiert sein und aktuell laufen. Eine Anleitung dazu finden Sie [hier](https://github.com/LosWochos76/wbh_addons/blob/main/IuK/DockerInstallation/README.md).

2. Erstellen Sie auf Ihrem Desktop ein neues Verzeichnis *Wetterdaten*.

3. Laden Sie die das Python-Script [import.py](https://raw.githubusercontent.com/LosWochos76/wbh_addons/main/IuK/Wetterdaten/import.py) herunter und speichern Sie es im zuvor erstellten Verzeichnis. Dafür können Sie im Browser mit der rechten Maustaste auf den Inhalt klicken und "Speichern unter..." auswählen.

4. Für die weiteren Schritte benötigen Sie eine Python-Umgebung auf Ihrem Rechner. Sollte diese bereits installiert sein, können Sie diesen Schritt überspringen. Laden Sie [Miniconda](https://docs.conda.io/en/latest/miniconda.html) für Ihr Betriebssystem herunter und installieren Sie es. Alle Voreinstellungen des Installationsassistenten können Sie auf den Standardwerten belassen.

5. Nach erfolgreicher Installation von Python können Sie im Startmenü von Windows das Wort "miniconda" eingeben. Es sollte dann der Eintrag "Miniconda Prompt" angezeigt werden. Durch Klicken auf den Eintrag öffnet sich ein Fenster mit schwarzem Hintergrund und weiß blinkendem Cursor.

6. Wechseln Sie in das Verzeichnis *Wetterdaten*. Dazu nutzen Sie den Befehl ```cd Desktop\Wetterdaten```. Zur Kontrolle können Sie sich den Inhalt des Verzeichnisses ansehen. Dies geschieht mit dem Befehl ```dir```. Das Ergebnis sollte wie folgt aussehen: <br> ![Konsole](./1-console.png)

7. Sollte die Datei *import.py* eine Dateiendung *.txt* besitzen, müssen Sie die Datei noch umbenennen. Die geschieht über den folgenden Befehl: ```ren import.py.txt import.py```

8. Nun müssen einige Python-Pakete installiert werden. Dazu müssen die folgenden Befehle eingegeben werden (die Reihenfolge ist dabei unwichtig):
- ```conda install -c anaconda pandas```
- ```conda install -c anaconda sqlalchemy```
- ```conda install -c anaconda pywget```
- ```conda install -c conda-forge psycopg2```<br><br>
Rückfragen können mit "y" (yes) beantwortet werden.

9. Nun kann das eigentliche Import-Script gestartet werden. Dazu wird der folgende Befehl ausgeführt: ```python import.py```. Das Herunterladen und der Import in die Datenbank dauern eine Weile. Nach erfolgreichem Import sollten Sie in pgAdmin die beiden neuen Tabellen *wetterstation* und *wettermessung* sehen und mithilfe von SQL abfragen können.

