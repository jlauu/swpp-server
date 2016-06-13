import os
from flask import Flask, request, json, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.last = ""

class InteractionEvent(db.Model):
    __tablename__ = 'interactions'
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.String());
    event = db.Column(db.String());
    url = db.Column(db.String());
    time = db.Column(db.BigInteger());
    
    def __init__(self, json):
        self.userid = json['userID']
        self.url = json['url']
        self.event = json['event']
        self.time = json['time']

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

@app.route('/send', methods=['POST'])
def send():
    if request.headers['Content-type'] == 'application/json':
        json = request.get_json()
        ty = json['type']
        data = json['data']
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
