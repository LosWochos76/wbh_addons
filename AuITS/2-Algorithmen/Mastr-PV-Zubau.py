from open_mastr import Mastr
import pandas as pd
import os
import sqlite3
import matplotlib.pyplot as plt

#pd.set_option('display.max_rows', None)
#pd.set_option('display.float_format', '{:.2f}'.format)

filename = os.path.expanduser("~") + "/.open-MaStR/data/sqlite/open-mastr.db"

if not os.path.exists(filename):
    db = Mastr()
    db.download()

conn = sqlite3.connect(filename)

query = "SELECT strftime('%Y', Inbetriebnahmedatum) as Jahr, sum(Nettonennleistung)/1000 as Zubau FROM solar_extended where Inbetriebnahmedatum>='2000-01-01' and Inbetriebnahmedatum<='2022-12-31' and Ort='Darmstadt' group by Jahr order by Jahr;"
df = pd.read_sql_query(query, conn)
df.plot.bar(x='Jahr', y='Zubau')
plt.title("Jährlicher Zubau von PV-Anlagen in Darmstadt MWp")
plt.show()

conn.close()