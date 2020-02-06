# !/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on January 25 09:48:12 2020
@author: nlog2n

 Data Visualization using Folium and GeoPandas

"""

import geopandas as gpd
import mplleaflet

import folium
from folium import IFrame

# import pandas_bokeh
# print(pandas_bokeh.__version__)
# pandas_bokeh.output_file("mapplot.html")


def visualize():
    """
    visualize using folium
    :return:
    """
    # center of singapore map
    latitude = 1.360920
    longitude = 103.832512

    # Data Visualization using Folium and GeoPandas
    singapore_map = folium.Map(
                    #tiles = "nlog2n",
                    location = [latitude, longitude],
                    zoom_start = 12)

    places = gpd.GeoDataFrame.from_file('singapore.imposm-geojson/singapore_corona.geojson')
    for i in range(0, len(places)):
        geo = places.geometry[i]
        lat, lng = geo.y, geo.x
        caseno = "#" + str(int(places.id[i]))
        date = places.date[i]
        age = places.age[i]
        gender = places.gender[i]
        visited = places.visited[i]
        from_country = places.home[i]
        related = places.related[i]
        status = places.status[i]

        label = caseno +"," + date + "<br>" + from_country + "<br>" \
               + str(age) + ", " + gender + "<br>" + visited
        popup = label # IFrame(label, width=300, height=100)

        if status == "recovered": # green
            color = 'green'
        elif from_country == "Singapore": #red
            color = 'red'
        else:
            color = 'orange'

        folium.Marker(
            location=[lat, lng],
            popup=popup,
            icon=folium.Icon(color=color, icon='info-sign')
        ).add_to(singapore_map)

    incidents_accident = folium.map.FeatureGroup()
    singapore_map.add_child(incidents_accident)

    singapore_map.save('templates/map.html')


def gen_map_html():
    """
    visualize using mplleaflet
    :return:
    """
    # overlay map
    admin = gpd.GeoDataFrame.from_file('singapore.imposm-geojson/singapore_admin.geojson')
    singapore = admin.iloc[0]
    print(singapore)
    print("done")

    # draw base map
    gpd.GeoSeries(singapore.geometry).plot()


    # places of interest
    places = gpd.GeoDataFrame.from_file('singapore.imposm-geojson/singapore_corona.geojson')
    print(places)
    print("done")

    # bounded inside the map
    places = places[places.geometry.within(singapore.geometry)]
    print(places)

    # draw places
    ax = places.geometry.plot(color='red')

    #### Output

    #mplleaflet.display(fig=ax.figure) # To display it right at the notebook.

    #mplleaflet.show(fig=ax.figure) # To output _map.html file and display it in your browser.

    mplleaflet.save_html(fig=ax.figure, fileobj='map.html')

    # TODO: output html file and rely on flask to render the web page?


if __name__ == '__main__':
    visualize()
