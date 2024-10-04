import streamlit as st
import pandas as pd

from dbmanager import make_connection, make_select_sql
from config import CHANNELS, DB_NAME


st.set_page_config(layout="wide")
st.write('Raspored tv programa do 7 dana unazad')

channel = st.selectbox('Izaberi kanal', CHANNELS)

connection = make_connection(DB_NAME)
table_name = channel.replace('-', '_').capitalize()
select_sql = make_select_sql(table_name)
df = pd.read_sql(select_sql, connection, parse_dates='datetime')
df.sort_values('datetime', inplace=True)
mask = [(d1 - d2).seconds < 301 for d1, d2 in
        zip(df.datetime[1:], df.datetime[:-1])] + [False]
df.drop(df[mask].index, inplace=True)

df['days'] = df.datetime.dt.date
df['time'] = df.datetime.dt.strftime('%H:%M')
df['display'] = df.time + ' ' + df.genre.str.rjust(7, ' ') + '   ' + df.title

start = pd.Timestamp.today() - pd.Timedelta(days=7)
end = pd.Timestamp.today()
date_range = pd.date_range(start, end)
dfs = []
for ts in date_range:
    d = df[df.days == ts.date()][['display']]
    d.reset_index(inplace=True, drop=True)
    dfs.append(d)
n_rows = max(dfs, key=len).shape[0]

date_display = [ts.strftime('%d. %h') for ts in date_range]
nd = pd.DataFrame({dt: d['display'] for dt, d in zip(date_display, dfs)})
nd.fillna('', inplace=True)


st.dataframe(nd, width=3000, height=740, hide_index=True)
