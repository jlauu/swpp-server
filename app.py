import os
from flask import Flask, request, json, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, static_folder='static', static_url_path='')
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.last = ""

from models import *

@app.route('/', methods=['GET'])
def index():
    return app.last

@app.route('/graph', methods=['GET'])
def graph():
   return render_template('graph.html')

@app.route('/send', methods=['POST'])
def send():
    if request.headers['Content-type'] == 'application/json':
        msg = request.get_json()
        ty = msg['type']
        data = msg['data']
        app.last = json.dumps(data, indent=4, separators=(',',': '))
        if ty == 'pages':
            [db.session.add(pv) for pv in map(PageVisit, data)]
            db.session.commit()
        elif ty == 'links':
            [db.session.add(l) for l in map(LinkClick, data)]
            db.session.commit()
        elif ty == 'interactions':
            [db.session.add(i) for i in map(InteractionEvent, data)]
            db.session.commit()
        else:
            return "Bad request"
        return "Received: " + app.last
    else:
        return "Bad request"

## DEPRECATED API BELOW

@app.route('/sendLinks',methods=['POST'])
def sendLinks():
    if request.headers['Content-Type'] == 'application/json':
        data = request.get_json()
        app.last = json.dumps(data, indent=4, separators=(',',': '))
        for lc in map(LinkClick, data):
            db.session.add(lc)
        db.session.commit()

        return "Recieved: " + app.last
    else:
        return "Bad request"

@app.route('/sendVisits',methods=['POST'])
def sendVisits():
    if request.headers['Content-Type'] == 'application/json':
        data = request.get_json()
        app.last = json.dumps(data, indent=4, separators=(',',': '))
        for pv in map(PageVisit, data):
            print(pv)
            db.session.add(pv)
        db.session.commit()

        return "Recieved: " + app.last
    else:
        return "Bad request"

if __name__ == '__main__':
    app.run()
