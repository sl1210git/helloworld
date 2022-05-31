from matplotlib import pyplot as plt
import numpy as np
import seaborn as sb
from statsmodels.graphics.tsaplots import plot_acf
import pandas as pd
import plotly.express as px

#Load Dataset
df = pd.read_csv("../dataset.csv", parse_dates=["Date"])
df.head()

#Preprocessing of the data
df.set_index("Date", drop=False, inplace=True)
df.head()
new_idx = pd.date_range("2008-05-26", "2021-04-30", freq="1D")
df = df.reindex(new_idx)
df.head()

#Date vs Volume plot
sb.set_theme()
sb.set(rc={'figure.figsize':(15,8)})
fig = px.line(df, x='Date', y="Volume")
fig.show()

#Date vs High price of the day plot
fig = px.line(df, x='Date', y="High")
fig.show()

#Simple Moving Average (SMA) for 10 and 20 days
df_sma=df.copy()
df_sma['SMA_10']=df_sma.VWAP.rolling(10, min_periods=1).mean()
df_sma['SMA_20']=df_sma.VWAP.rolling(20, min_periods=1).mean()
plt.plot(df_sma['Date'], df_sma['VWAP'], color='blue')
plt.plot(df_sma['Date'], df_sma['SMA_10'], color='red')
plt.plot(df_sma['Date'], df_sma['SMA_20'], color='green')
plt.show()

#Autocorrelation plot
df.isnull().sum()
df['VWAP'].interpolate(method='linear',axis=0,inplace=True)
plot_acf(df['VWAP'], lags=50)
plt.show()

#Headmap
df_temp=df.copy()
df_temp['day'] = df_temp.index.day
df_temp['month'] = df_temp.index.month
df_temp['year'] = df_temp.index.year
df_m=df_temp.groupby(['month','year']).mean()
df_m
df_m=df_m.unstack(level=0)
fig, ax=plt.subplots(figsize=(11,9))
sb.heatmap(df_m['VWAP'])
plt.show()
