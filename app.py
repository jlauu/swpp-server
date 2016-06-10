import os
from flask import Flask, request, json, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.last = ""

class LinkClick(db.Model):
    __tablename__ = 'linkclicks'
    id = db.Column(db.Integer, primary_key=True)
    src = db.Column(db.String())
    dest = db.Column(db.String())
    time = db.Column(db.BigInteger());
    userid = db.Column(db.String());

    def __init__(self, json):
        self.src = json['from']
        self.dest = json['to']
        self.time = json['time']
        self.userid = json['userID']

class PageVisit(db.Model):
    __tablename__ = 'pagevisits'
    id = db.Column(db.Integer, primary_key=True)
    sessionid = db.Column(db.String())
    tabid = db.Column(db.Integer)
    windowid = db.Column(db.Integer)
    srcid = db.Column(db.Integer)
    url = db.Column(db.String())
    time = db.Column(db.Float())
    transition = db.Column(db.String())

    def __init__(self, json):
        self.sessionid = json['sessionID']
        self.tabid = json['tabID']
        self.windowid = json['windowID']
        self.srcid = json['srcID']
        self.url = json['url']
        self.time = json['time']
        self.transition = json['transition']

    def __repr__(self):
        return '<id {}>'.format(self.id)

@app.route('/', methods=['GET'])
def index():
    return app.last

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
