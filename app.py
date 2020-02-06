#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on June 26 09:48:12 2018
@author: nlog2n

  Flask server
"""

import os
from flask import Flask, request, render_template, redirect, url_for
from werkzeug.utils import secure_filename

# UPLOAD_FOLDER = os.path.basename('uploads')
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

UPLOAD_FOLDER = './static/uploads/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_pretty_json_str(result):
    import json
    return json.dumps(result, sort_keys=False, ensure_ascii=False, indent=4)


@app.route('/')
def index_page():
    return render_template('map.html')


@app.route('/hello')
def home_page():
    return 'Singapore Corona Virus Cases'


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', debug=True, port=port)

