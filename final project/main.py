import streamlit as st
import yfinance as yf
import datetime as dt
import pandas as pd
import numpy as np
import plotly.express as px
import requests as req
import plotly.graph_objects as go
import pycountry_convert as pcconvert

st.write("# Our Final Project: Nike Factory Locations")   # this is markdown

# show all columns when printed
pd.set_option('display.max_columns', None)

# read dataframe from the excel file
df = pd.read_excel('NikeFactoryLocations1.xlsx')

# drop the unnecessary column
df = df.drop(['Operating Region'], axis=1)

# change float column to int
def float_to_int(df, cols):
    df[cols] = df[cols].fillna(0.0).astype(int)

# change float columns to int (to original type)
cols = ['Total Workers', 'Line Workers']
float_to_int(df, cols)

# create Female Worker and Migrant Worker count columns
df['Female Worker Count'] = df['Total Workers'] * df['% Female Workers']
df['Migrant Worker Count'] = df['Total Workers'] * df['% Migrant Workers']
cols = ['Female Worker Count', 'Migrant Worker Count']
float_to_int(df, cols)
def country_to_continent(country_name):
    country_alpha2 = pcconvert.country_name_to_country_alpha2(country_name)
    country_continent_code = pcconvert.country_alpha2_to_continent_code(country_alpha2)
    country_continent_name = pcconvert.convert_continent_code_to_continent_name(country_continent_code)
    return country_continent_name
country_to_continent('Bosnia and Herzegovina')


# API key for OpenWeatherMap - is not stored as an enviroment variable to be able to
# produce the same result from different systems as well
API_KEY='26d87b67e9196fced6ce50d77eb89968'
# create 2 new columns
df['Longitude'], df['Latitude'] = np.nan, np.nan

# get the geolocation info via OpenWeatherMap API
for i in range(len(df)):
    city = df['City'][i]
    res = req.get(f'https://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={API_KEY}')
    if len(res.json()) > 0:
        df['Longitude'].iloc[i] = res.json()[0]['lon']
        df['Latitude'][i] = res.json()[0]['lat']
    else:
        pass
# save df into a new file in case if API doesn't work
df.to_csv('NikeUpdatedCopy.csv')
# geomap of factories
fig4 = go.Figure(data=go.Scattergeo(
        lon = df['Longitude'],
        lat = df['Latitude'],
        text = df['City'],
        mode = 'markers'
        ))

fig4.update_layout(
        title = 'Nike Factory Locations all around the World',
        geo_scope='world',
    )

# bubble chart
fig3 = px.scatter(df, x="Total Workers", y="Country", color="Continent", size="Total Workers",
                 hover_name="State", log_x=True, size_max=60, title='Total Workers by Country sized by Worker Count on Sized Scatter Chart')

# pie chart
fig2 = px.pie(df, values='Total Workers', names='Country', title='Total Worker Distrubution by Country Presented in Pie Chart')
fig2.update_traces(textposition='inside', textinfo='percent')

# bar chart
fig1 = px.bar(df, x="Product Type", y="Country", color="Country",
      title="Product Type by Countries in a Sliced Bar Chart"
)


st.write("## Here's our first attempt at showing a chart:")
fig1






#showing the table
st.write("## Here's our first attempt at using data to create a table:")
df

