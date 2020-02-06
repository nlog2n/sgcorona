

import geopandas as gpd
import mplleaflet

# import pandas_bokeh
# print(pandas_bokeh.__version__)
# pandas_bokeh.output_file("mapplot.html")

# overlay map
admin = gpd.GeoDataFrame.from_file('singapore.imposm-geojson/singapore_admin.geojson')
singapore = admin.iloc[0]
print(singapore)

# draw
gpd.GeoSeries(singapore.geometry).plot()


# places of interest
roads = gpd.GeoDataFrame.from_file('singapore.imposm-geojson/singapore_corona.geojson')


# bounded inside the map
roads = roads[roads.geometry.within(singapore.geometry)]
print(roads)

# draw places
ax = roads.geometry.plot()

#mplleaflet.display(fig=ax.figure) # To display it right at the notebook.

#mplleaflet.show(fig=ax.figure) # To output _map.html file and display it in your browser.

mplleaflet.save_html(fig=ax.figure, fileobj='map.html')

# TODO: output html file and rely on flask to render the web page?
