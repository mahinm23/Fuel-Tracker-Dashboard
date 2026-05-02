import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Fuel Tracker")

# Import the trips database
df = pd.read_csv("Trips.csv")
df['Tank'] = df['Tank'].str.split(' ()').str[0]

st.write("Fuel Tracker Data:")
st.dataframe(df.head())

