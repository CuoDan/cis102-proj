######################
# Import libraries
######################

import pandas as pd
import streamlit as st
from PIL import Image

import math
from datetime import datetime

import pandas as pd

import plotly.express as px
import folium
from streamlit_folium import folium_static

######################
# Page Title
######################

# PIL.Image
image = Image.open('free-airbnb.png')

#https://docs.streamlit.io/library/api-reference/media/st.image

st.image(image, output_format="PNG")
st.caption("license: https://creativecommons.org/licenses/by/4.0/", unsafe_allow_html=False)

#Welcome section
st.title("Welcome to AirBnB Shortcut!")

st.write("""
The purpose of this app is to help you find your right AirBnB in New York City faster and more efficiently!

Instructions:
         
    1. Choose which borough of NYC you want to stay in...
    2. Choose the neighborhood in that borough...
    3. Select a price range...

That's it!

You can also look at the table and map at the bottom of the page for more information.
""")

st.write('---')
@st.cache_data
def get_data():
    url = "https://cis102.guihang.org/data/AB_NYC_2019.csv"
    return pd.read_csv(url)
df = get_data()

st.subheader('AirBnB in NYC as of 2019-09-12')
st.dataframe(df.head(10))

st.write("---")

#######################
#####Select borough
#######################

boroughs = df["neighbourhood_group"]

borough = []
for x in boroughs:
    if x not in borough:
        borough.append(x)

st.subheader('Select the area for your AirBnB')

select_burough = st.selectbox("Your selected borough:", borough, 0)   

####################################
#Select neighborhood in the borough
####################################

neighbourhood = []

    # Loop through each row using iterrows()    
for index, row in df.iterrows():
    # Access data in the row using column names
    neighbourhoods = row['neighbourhood']
    neigh_group = row['neighbourhood_group']
    
    if neigh_group == select_burough:
        if neighbourhoods not in neighbourhood:
            neighbourhood.append(neighbourhoods)


select_neighbourhood = st.selectbox(f"Your selected neighborhood in {select_burough}:", neighbourhood, 0)

st.write("---")

###################
####Select price
###################

st.subheader('Choose a price range for your AirBnB')

min, max = st.slider("Price Range:", float(df.price.min()), 1000., (50., 300.))

st.write(f"The price range you selected is between {min} dollars and {max} dollars")

map_listing = df.query("@min <= price <= @max and neighbourhood_group == @select_burough and neighbourhood == @select_neighbourhood"
                        )[["name", "latitude", "longitude", "price"]]

info_listing = df.query("@min <= price <= @max and neighbourhood_group == @select_burough and neighbourhood == @select_neighbourhood"
                        )[["host_name", "room_type"]]

table_listing = df.query("@min <= price <= @max and neighbourhood_group == @select_burough and neighbourhood == @select_neighbourhood"
                        )[["name", "host_name", "room_type", "price"]]

listing_count = len(map_listing)

st.write("---")

st.write("The table below shows the housing rental(s) that match your requirements:")
st.write(table_listing)

st.subheader(f"Total {listing_count} housing rental(s) are found in {select_neighbourhood}, {select_burough} with price between {min} dollars and {max} dollars")

st.write("---")
####################
######## Map
####################
Top = map_listing.values[0,:]
m = folium.Map(location=Top[1:-1], zoom_start=16)

tooltip = "Tooltip"
for j in range(listing_count):
    name, lat, lon, price = map_listing.values[j,:]
    host_name, room_type = info_listing.values[j,:]
    folium.Marker(
            (lat,lon), popup=f"""
                        <div style="width: 150px;">
                            <p>Name: {name}</p>
                            <p>Host name: {host_name}</p>
                            <p>Room type: {room_type}</p>
                        </div>
                        """ , tooltip=f"Tooltip: ${price}"
                        ).add_to(m)

# call to render Folium map in Streamlit
folium_static(m)

st.write("This app is developed by Cuong Dang.")