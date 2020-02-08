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

app = Flask(__name__)


@app.route('/')
def index_page():

    ## save folium map to html file and then render
    return render_template('map.html')

    ## alternatively, call folium _repr_html_ directly
    # # create folium map object
    # folium_map = geoview.visualize()
    # return folium_map._repr_html_()

    # TODO: not shown correctly in browser


@app.route('/hello')
def home_page():
    return 'Singapore Corona Virus Cases'


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', debug=True, port=port)

