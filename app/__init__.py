from flask import Flask
import os

app = Flask(__name__)
app.config['APP_ROOT'] = os.path.dirname(os.path.abspath(__file__))
app.config['UPLOAD_DIR'] = os.path.join(app.config['APP_ROOT'], 'uploads')

from app import views
