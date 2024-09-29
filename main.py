import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

from sklearn.datasets import fetch_california_housing

import folium
from folium import plugins

#meadian house value in area and size of house
data = fetch_california_housing(download_if_missing=True,as_frame=True).frame # to get as a data frame
#sklearn.datasets.fetch_california_housing(*, data_home=None, download_if_missing=True, return_X_y=False, as_frame=False, n_retries=3, delay=1.0)
# creates a map instance takes the avg of the longitude and an avg of the LAT to center it around those coordinates
m = folium.Map(location=[data['Latitude'].mean(), data['Longitude'].mean()],zoom_start=6)

# To visualize this by color
# normalize data to get a color difference of the value of the house 0=lowest 1=highest instead of using the raw values

price_min, price_max = data['MedHouseVal'].min(), data['MedHouseVal'].max()
size_min, size_max = data['AveRooms'].min(), data['AveRooms'].max()

for _, row in data.iterrows():
    normalized_price= (row['MedHouseVal'] - price_min) / (price_max - price_min)
    color = plt.cm.RdYlGn(1-normalized_price) # uses map of the plt cm= color map using red yellow green color map (1-normalize) price inverts the scale so green is lowest and red is the highest

    normalized_rooms = (row['AveRooms'] - size_min) / (size_max - size_min)

    popup_info = f"""Median House Value: ${row['MedHouseVal']:.2f}<br>
    Average Rooms: {row['AveRooms']}<br>
    Population: {row['Population']}<br>
    Median Income: ${row['MedInc']:.2f}"""

    folium.CircleMarker(
        location=[row['Latitude'], row['Longitude']],
        radius=5 + 20 * normalized_rooms,
        color=mcolors.to_hex(color[:3]),
        fill=True,
        fill_color=mcolors.to_hex(color[:3]),
        fill_opacity=0.7,
        popup=folium.Popup(popup_info, max_width=300)

        ).add_to(m)

    plugins.MiniMap().add_to(m)

    m.save('real_estate.html')
