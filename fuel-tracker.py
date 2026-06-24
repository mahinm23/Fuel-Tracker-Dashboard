import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Fuel Tracker")

# Import the trips database
@st.cache_data
def load_data(file):
    df = pd.read_csv(file)
    return df

df = load_data("Trips_cleaned.csv")
df['Travel Date'] = pd.to_datetime(df['Travel Date'])

st.write("Fuel Tracker Data:")
if st.checkbox("Show DF Head"):
    st.dataframe(df.head())

line = px.line(df, x='Travel Date', y='MPG', 
               title='MPG vs trips', 
               hover_data=['Location', 'Miles'])
st.plotly_chart(line)

per_trip_costs = px.scatter(df, x='Travel Date', y='Cost', 
                            title='Cost Per Trip', 
                            hover_data=['Location', 'Miles'])
st.plotly_chart(per_trip_costs)

df_weekly = df.groupby(pd.Grouper(key='Travel Date', freq='W'))\
    [['MPG', 'Miles', 'Cost']].mean().reset_index()

bar_weekly = px.bar(df_weekly, x='Travel Date', y='MPG', 
                    title="Weekly Average MPG:")
st.plotly_chart(bar_weekly)