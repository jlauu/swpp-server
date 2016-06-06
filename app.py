import os
from flask import Flask, request, json, jsonify
from flask_sqlalchemy import SQLAlchemy

from models import *

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.last = ""

@app.route('/', methods=['GET'])
def index():
    return "Last message received: " + app.last

@app.route('/send',methods=['POST'])
def send():
    if request.headers['Content-Type'] == 'application/json':
        data = json.dumps(request.json)
        app.last = data
        for pv in map(PageVisit, data):
            db.session.add(pv)
        db.session.commit()

        return "Recieved: " + data
    else:
        return "Bad request"

if __name__ == '__main__':
    app.run()
