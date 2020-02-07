#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on June 26 09:48:12 2018
@author: nlog2n

  Flask server
"""

import os
from flask import Flask, request, render_template

import geoview

UPLOAD_FOLDER = './static/uploads/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

# output html file and rely on flask to render the web page
OUTPUT_HTML_FILE = 'templates/map.html'


app = Flask(__name__)

# create folium map object
folium_map = geoview.visualize()

# folium_map.save(OUTPUT_HTML_FILE)


@app.route('/')
def index_page():

    ## save folium map to html file and then render
    # return render_template('map.html')

    ## alternatively, call folium _repr_html_ directly
    return folium_map._repr_html_()


@app.route('/hello')
def home_page():
    return 'Singapore Corona Virus Cases'


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', debug=True, port=port)

