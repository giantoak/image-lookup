from flask import Flask
import os
from flask.ext.socketio import SocketIO
import logging
from imgsearch import ImgSearch

app = Flask(__name__)
app.config['APP_ROOT'] = os.path.dirname(os.path.abspath(__file__))
app.config['UPLOAD_DIR'] = os.path.join(app.config['APP_ROOT'], 'uploads')

app.secret_key = 'YS16RS8J3KNPOQF6O65J5CQQ35S0B4H1OC7EIIDZ4TA1KITZQ'
socketio = SocketIO(app)

imgsch = ImgSearch()

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
socklogger = logging.getLogger('socketio.virtsocket')
socklogger.debug('test')
from app import views
