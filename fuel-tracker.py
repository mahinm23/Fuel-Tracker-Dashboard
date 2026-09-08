import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.io as pio
from plotly.subplots import make_subplots
import plotly.graph_objects as go

st.set_page_config(layout='wide')
st.title("Fuel Tracker")

# Import the trips database
@st.cache_data
def load_data(file):
    try:
        df = pd.read_csv(file)
        # Date time does not persist in the csv
        # Moved here so that it doesn't get converted 
        # again every time the app is re run
        df['Travel Date'] = pd.to_datetime(df['Travel Date'])
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        st.stop()
        # Stops error messages displayed in the app,
        # prevents app from running if file not found or otherwise

df = load_data("Trips_cleaned.csv")

pio.templates.default = "ggplot2"

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


# Line chart for trips and mpg in order of date
line = px.line(df, x='Travel Date', y='MPG', 
               title='MPG vs trips', 
               hover_data=['Location', 'Miles'])
st.plotly_chart(line)


# Scatter plot for the cost of each trip in order of date
per_trip_costs = px.scatter(df, x='Travel Date', y='Cost', 
                            title='Cost Per Trip', 
                            hover_data=['Location', 'Miles'])
st.plotly_chart(per_trip_costs)


# Bar chart for average weekly fuel mpg
df_weekly = df.groupby(pd.Grouper(key='Travel Date', freq='W'))\
    [['MPG', 'Miles', 'Cost']].mean().reset_index()

bar_weekly = px.bar(df_weekly, x='Travel Date', y='MPG', title="Weekly Average MPG:")
st.plotly_chart(bar_weekly)


# Bar chart for average metric grouped by the type of trip

# Create the bins for the trip types
# Short trips are 0-5, medium 5-15, 
# Everything above is a long trip
bins = [0, 5, 15, float('inf')]
labels = ['Short', 'Medium', 'Long']

# Applies the grouping to the df by creating a new column called Trip Type
df['Trip Type'] = pd.cut(x = df['Miles'], bins=bins, labels=labels)

by_trip_type = df.groupby('Trip Type')[['MPG', 'Miles', 'Cost']].mean().reset_index()

# Create subplots for each metric by trip type
# Enables a shared X axis and their own Y axis
fig = make_subplots(rows=4, cols=1, 
                              subplot_titles=['Avg MPG', 'Avg Miles', 'Avg Cost', 'Trip Count'])

fig.add_trace(go.Bar(x=by_trip_type['Trip Type'], y=by_trip_type['MPG']), row=1, col=1)
fig.add_trace(go.Bar(x=by_trip_type['Trip Type'], y=by_trip_type['Miles']), row=2, col=1)
fig.add_trace(go.Bar(x=by_trip_type['Trip Type'], y=by_trip_type['Cost']), row=3, col=1)
fig.add_trace(go.Bar(x=by_trip_type['Trip Type'], y=df['Trip Type'].value_counts()), row=4, col=1)

fig.update_layout(title_text='Avg Metric by Trip Type', height = 1000)

st.plotly_chart(fig)