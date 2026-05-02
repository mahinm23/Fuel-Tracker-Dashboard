import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Fuel Tracker")

# Import the trips database
df = pd.read_csv("Trips.csv")
df['Tank'] = df['Tank'].str.split(' ()').str[0]
df = df.dropna()
df['Travel Date'] = pd.to_datetime(df['Travel Date'], format='%d/%m/%Y')

st.write("Fuel Tracker Data:")
st.dataframe(df.head())

line = px.line(df, x='Travel Date', y='MPG', title='MPG vs trips', hover_data=['Location', 'Miles'])
st.plotly_chart(line)

df_weekly = df.groupby(pd.Grouper(key='Travel Date', freq='W'))[['MPG', 'Miles', 'Cost']].mean().reset_index()

bar_weekly = px.bar(df_weekly, x='Travel Date', y='MPG', title="Weekly Average MPG:")
st.plotly_chart(bar_weekly)