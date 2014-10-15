# Views for an app that saves uploaded files into a temporary directory,
# then calls reverse image search APIs on them, then routes the results
# back.

from __future__ import print_function
from app import app
import flask
from flask import render_template
import requests
from werkzeug import secure_filename
import os
import sys

from imgsearch import ImgSearch

@app.route('/')
def root():
    return render_template('upload_root.html')

@app.route('/upload', methods=['POST'])
def receive_upload():
    files = flask.request.files.getlist('file[]')
    imgsch = ImgSearch()

    for f in files:
        try:
            sf = secure_filename(f.filename)
            obscured_fn = imgsch.get_filename(sf)
        except TypeError:
            # handle bad file extension here
            print('Bad file extension in {}'.format(sf), file=sys.stderr)
            continue

        dest = os.path.join(app.config['UPLOAD_DIR'], obscured_fn)
        f.save(dest)
        print('saved {}'.format(dest))

        # call reverse image search on dest


    return ''
