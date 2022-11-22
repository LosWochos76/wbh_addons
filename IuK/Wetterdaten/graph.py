import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt

engine = create_engine('postgresql://postgres:secret@localhost:5432')
sql = 'select datum, min_2m, max_2m from wettermessung where stations_id=1078 order by Datum;'

df = pd.read_sql(sql, engine)
df.plot(x='datum', y=['min_2m', 'max_2m'])
plt.show()