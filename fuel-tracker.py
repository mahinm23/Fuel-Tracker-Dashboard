import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Fuel Tracker")

# Import the trips database
df = pd.read_csv("Trips.csv")
df['Tank'] = df['Tank'].str.split(' ()').str[0]
df = df.dropna()

st.write("Fuel Tracker Data:")
st.dataframe(df.head())

fig = px.line(df, x='Travel Date', y='MPG', title='MPG vs trips')
st.plotly_chart(fig)