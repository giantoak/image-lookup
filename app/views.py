# Views for an app that saves uploaded files into a temporary directory,
# then calls reverse image search APIs on them, then routes the results
# back.

from __future__ import print_function
from app import app, socketio, socklogger, logger, imgsch
import flask
from flask import render_template, url_for, g, send_from_directory,\
request, session
from flask.ext.socketio import send, emit
from werkzeug import secure_filename

import json
import os
import sys
import requests
from urlparse import urljoin
from threading import Timer

@app.route('/')
def root():
    return render_template('upload_root.html')

@app.route('/upload', methods=['POST'])
def receive_upload():
    """
    Architecture design notes: /upload uploads all of the posted
    files to the server, saves the file names in the global sesion
    variable (g), and renders the client results page.

    On load, the client results page connects to a websocket, which
    triggers the API calls. Results are streamed back to the client
    as they come in.

    """
    files = flask.request.files.getlist('file[]')
    d = {}
    for f in files:
        try:
            sf = secure_filename(f.filename)
            obscured_fn = imgsch.get_filename(sf)
        except TypeError:
            print('Bad file extension in {}'.format(sf), file=sys.stderr)
            #TODO: handle bad file extensions more formally
            continue

        dest = os.path.join(app.config['UPLOAD_DIR'], obscured_fn)
        f.save(dest)
        print('saved {}'.format(dest))
        d[obscured_fn] = f.filename

    session['file_dict'] = d
    
    return render_template('results_gallery.html')

@app.route('/_/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_DIR'], filename)

@socketio.on('connect', namespace='/gallery')
def stream_results():
    print('Connected to /gallery')
    

    my_url = request.host_url

    # request results from Google
    headers = {}
    headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"

    # loop through objects in flask global object
    for filename, actual_name in session['file_dict'].iteritems():
        local_image_url = url_for('uploaded_file', filename=filename)
        public_url = urljoin(my_url, local_image_url)
        print('Requesting ' + public_url)

        google_url = 'http://www.google.com/searchbyimage?image_url=' + public_url
        r = requests.get(google_url, headers=headers)
        result = imgsch.parse_google_query(r.text)
        result.update({
            'url': google_url,
            'img': public_url,
            'filename': actual_name
        })

        if r.ok:
            emit('result', json.dumps(result))
    
        else:
            logging.warn('Google API query returned code\
                         {}'.format(r.code))

        # allow images to live for 5 minutes
        t = Timer(600.0, delete_file, [filename])
        t.start()

def delete_file(f):
    os.remove(os.path.join(app.config['UPLOAD_DIR'], f))
