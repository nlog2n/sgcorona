# sgcorona
Find out corona viruses in Singapore

## required
```bash
pipenv --python 3
pipenv install geopandas
pipenv install mplleaflet
# pipenv install mplexporter
pipenv install ipython
pipenv install matplotlib
pipenv install descartes
# pipenv install pandas-bokeh
pipenv install folium
pipenv install xlrd
pipenv install flask
```

## quick start

```bash
pipenv shell
python read_excel.py > singapore.imposm-geojson/singapore_corona.geojson
python geoview.py
python app.py
```




