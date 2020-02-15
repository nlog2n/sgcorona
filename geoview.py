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
from folium.features import DivIcon
print(folium.__version__)

# import pandas_bokeh
# print(pandas_bokeh.__version__)
# pandas_bokeh.output_file("mapplot.html")

# center of singapore map
latitude = 1.360920
longitude = 103.832512

# generated geojson file
SINGAPORE_CORONA_GEOJSON_FILE = 'singapore.imposm-geojson/singapore_corona.geojson'


def get_virus_data():
    """
    get geodataframe for singapore virus data
    :return:
    """
    # ## read from the generated geojson file
    # gdf = gpd.GeoDataFrame.from_file(SINGAPORE_CORONA_GEOJSON_FILE)
    # return gdf

    ## alternatively
    ## read from my excel file and get geopandas GeoDataFrame
    import read_excel
    geojsonObj = read_excel.read_rawdata()

    import convert_geojson
    gdf = convert_geojson.geojson_to_gdf(geojsonObj)
    print(gdf)
    return gdf


def draw_base_map():
    # Data Visualization using Folium and GeoPandas
    singapore_map = folium.Map(
                    #tiles="nlog2n",
                    #attr="<a href=https://github.com/nlog2n>nlog2n</a>",
                    location=[latitude, longitude],
                    zoom_start=11)

    return singapore_map


def draw_map_legend(m):
    title_html = """
        <title>Corona Viruses in Singapore</title>
    """
    m.get_root().html.add_child(folium.Element(title_html))

    from datetime import datetime
    dt = datetime.now()
    dtStr = dt.strftime("%Y %b %d")
    legend_html = """
     <div style="position: fixed; 
     bottom: 20px; right: 10px; width: 110px; height: 120px; 
     border:2px solid grey; z-index:9999; font-size:12px;">
     &nbsp; %s <br>
     &nbsp; <i class="fa fa-map-marker fa-2x"
                  style="color:orange"></i>&nbsp; imported<br>
     &nbsp; <i class="fa fa-map-marker fa-2x"
                  style="color:red"></i>&nbsp; infected<br>
     &nbsp; <i class="fa fa-map-marker fa-2x"
                  style="color:green"></i>&nbsp; recovered
      </div>
    """ % dtStr

    m.get_root().html.add_child(folium.Element(legend_html))


def draw_stats(m):
    cx, cy = (1.301268, 103.970763)

    width, height = 0.05/2, 0.05
    # points = [(cx-width/2, cy-height/2), (cx+width/2, cy-height/2), (cx+width/2, cy+height/2), (cx-width/2, cy+height/2)]
    # color = 'yellow'
    # rect = folium.Rectangle(bounds=points, color='#ff7800', fill=True, fill_color='#ffff00', fill_opacity=0.9)
    # rect.add_to(m)

    #folium.Circle([cx, cy], 1200, color='#ff7800', fill=True, fill_color='#ffff00', fill_opacity=0.9).add_to(m)


    text = '33'
    folium.map.Marker(
        [cx, cy],
        icon=DivIcon(
            icon_size=(36, 36),
            icon_anchor=(0, 0),
            html='<div style="font-family:Courier; color:Orange; font-size: 24px;">33 CASES</div>',
        )
    ).add_to(m)


def draw_virus_places(m, gdf):

    group0 = folium.FeatureGroup(name='<span style="color: red;">{} infected</span>')
    group1 = folium.FeatureGroup(name='<span style="color: orange;">{} imported</span>')
    group2 = folium.FeatureGroup(name='<span style="color: green;">{} recovered</span>')

    cnt_red, cnt_orange, cnt_green = 0, 0, 0

    for i, row in gdf.iterrows():
        geo = row.geometry
        lat, lng = geo.y, geo.x

        caseno = "#" + str(int(row.id))
        date = row.date
        age = str(row.age)
        gender = row.gender
        occupation = row.occupation
        stay = row.stay
        visited = row.visited
        from_place = row.infected
        linked_to = row.linked_to
        status = row.status

        nationality = row.nationality
        symptom_date = row.symptom_date
        discharge_date = row.discharge_date
        cluster = row.cluster

        # in html view
        label = "<b>" + caseno + "</b>, " + date \
                + "<br>" + age + "yr " + gender + " " + nationality + " " + occupation
        if stay != "" and stay is not None:
            label += "<br>" + "<b>Stay:</b> " + stay
        if visited != "" and visited is not None:
            label += "<br>" + "<b>Visited:</b> " + visited
        if linked_to != "" and linked_to is not None:
            label += "<br>" + "<b>Linked to:</b> " + linked_to
        if cluster != "" and cluster is not None:
            label += "<br>" + "<b>Cluster:</b> " + cluster
        if symptom_date != "" and symptom_date is not None:
            label += "<br>" + "<b>Symptom Start:</b> " + symptom_date
        if status != "" and status is not None:
            label += "<br>" + "<b>Status:</b> " + status
            if status == "Discharged":
                if discharge_date != "" and discharge_date is not None:
                    label += " on " + discharge_date

        test_html = folium.Html(label, script=True)
        popup = folium.Popup(test_html, max_width=300)

        # using iframe not supported inside Wechat app
        # iframe = IFrame(html=label, width=300, height=100)
        # popup = folium.Popup(iframe,  parse_html=True)

        grp = None
        if status == "Discharged": # green
            color = 'green'
            grp = group2
            cnt_green += 1
        elif from_place == "Singapore": #red
            color = 'red'
            grp = group0
            cnt_red += 1
        else:
            color = 'orange'
            grp = group1
            cnt_orange += 1

        marker = folium.Marker(
            location=[lat, lng],
            popup=popup,
            icon=folium.Icon(color=color, prefix='fa', icon='circle')
        )
        marker.add_to(grp)

    group0.layer_name = group0.layer_name.format(cnt_red)
    group1.layer_name = group1.layer_name.format(cnt_orange)
    group2.layer_name = group2.layer_name.format(cnt_green)

    m.add_child(group0)
    m.add_child(group1)
    m.add_child(group2)

    folium.map.LayerControl('topright', collapsed=True).add_to(m)


def visualize():
    """
    visualize using folium
    :return:
    """
    singapore_map = draw_base_map()

    gdf = get_virus_data()

    draw_virus_places(singapore_map, gdf)

    #draw_stats(singapore_map)

    draw_map_legend(singapore_map)

    return singapore_map


def save_folium_map(m):
    # output html file and rely on flask to render the web page
    OUTPUT_HTML_FILE = 'templates/map.html'

    m.save(OUTPUT_HTML_FILE)


def gen_map_html(OUTPUT_HTML_FILE):
    """
    visualize using mplleaflet
    Map data can be downloaded at: mapzen/metro-extracts, https://www.interline.io/osm/extracts/
    in imposm-geojson format.
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

    mplleaflet.save_html(fig=ax.figure, fileobj=OUTPUT_HTML_FILE)


if __name__ == '__main__':
    m = visualize()
    save_folium_map(m)
