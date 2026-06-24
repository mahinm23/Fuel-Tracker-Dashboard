import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout='wide')
st.title("Fuel Tracker")

# Import the trips database
@st.cache_data
def load_data(file):
    df = pd.read_csv(file)
    return df

df = load_data("Trips_cleaned.csv")
df['Travel Date'] = pd.to_datetime(df['Travel Date'])

# High view metrics
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric('Average MPG', f"{df['MPG'].mean():.1f}", 'MPG')
col2.metric('Average Distance', f"{df['Miles'].mean():.1f}", 'Miles')
col3.metric('Average Trip Cost', f"£{df['Cost'].mean():.2f}", '£ (GBP)')
col4.metric('Total Saved (TFL - fuel cost)', f"£{df['Estimated TFL'].sum() - df['Cost'].sum():.2f}", '£ (GBP)')
col5.metric('Total Miles Covered', f"{df['Mileage'].iloc[-1]-df['Mileage'].iloc[0]:.0f}", 'Miles')


# Checkbox to display the first 5 rows of the df
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