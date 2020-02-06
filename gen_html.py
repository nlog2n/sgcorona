

import geopandas as gpd
import mplleaflet

import folium

# import pandas_bokeh
# print(pandas_bokeh.__version__)
# pandas_bokeh.output_file("mapplot.html")


# center of singapore map
latitude = 1.359182
longitude = 103.809187

# Data Visualization using Folium and GeoPandas
singapore_map = folium.Map(
                location = [latitude, longitude], 
                zoom_start = 12)

places = gpd.GeoDataFrame.from_file('singapore.imposm-geojson/singapore_corona.geojson')
for i in range(0, len(places)):
    geo = places.geometry[i]
    lat, lng = geo.y, geo.x
    caseno = "#" + str(places.id[i])
    date = places.date[i]
    age = places.age[i]
    gender = places.gender[i]
    visited = places.visited[i]
    from_country = places.home[i]
    info = caseno +"," + date + " " + from_country + "\n" + str(age) + ", " + gender + "\n" + visited
    if from_country == "Singapore": #red
        folium.Marker(
            location=[lat, lng],
            popup=info,
            icon=folium.Icon(color='red', icon='info-sign')
        ).add_to(singapore_map)
    else:
        folium.Marker(
            location=[lat, lng],
            popup=info,
            icon=folium.Icon(color='orange', icon='info-sign')
        ).add_to(singapore_map)

incidents_accident = folium.map.FeatureGroup()
singapore_map.add_child(incidents_accident)

singapore_map.save('templates/map.html')


def gen_map_html():
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
