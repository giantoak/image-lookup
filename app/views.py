from __future__ import print_function
from app import app
import flask
from flask import render_template
import requests

@app.route('/')
def root():
    return render_template('upload_root.html')

@app.route('/upload', methods=['POST'])
def receive_upload():
    files = flask.request.files.getlist('file[]')

    print(files)

    return ''
