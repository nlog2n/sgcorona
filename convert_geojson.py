# !/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on January 25 09:48:12 2020
@author: nlog2n

   raw data to geojson data format, and to geopandas GeoDataFrame format if required
   like
   geom = [ Point(...) ,...]
   gpd.GeoDataFrame({'geometry':geom})

"""

from geojson import Feature, Point, FeatureCollection
import geopandas as gpd


def raw_to_geojson(raw):
    # sample
    my_feature = Feature(geometry=Point((1.6432, -19.123)), properties={"country": "Spain"})
    my_other_feature = Feature(geometry=Point((-80.234, -22.532)), properties={'country': 'Brazil'})
    collection = FeatureCollection([my_feature, my_other_feature])

    gdf = gpd.GeoDataFrame.from_features(collection['features'])
    return gdf


def geojson_to_gdf(gjsonObj):
    # refer to: https://medium.com/@maptastik/remote-geojson-to-geodataframe-19c3c1282a64
    gdf = gpd.GeoDataFrame.from_features(gjsonObj['features'])
    return gdf


if __name__ == '__main__':
    import read_excel
    geojsonObj = read_excel.read_rawdata()

    gdf = geojson_to_gdf(geojsonObj)
    print(gdf)

    import matplotlib.pyplot as plt
    gdf.plot()
    plt.show()
