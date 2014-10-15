from app import app, socketio
import os

if __name__ == '__main__':
    port = os.getenv('PORT', 8080)
    app.debug = True
    socketio.run(app, host='0.0.0.0', port=port)
