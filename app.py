import os
from flask import Flask, request, json, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.last = ""

class PageVisit(db.Model):
    __tablename__ = 'pagevisits'
    id = db.Column(db.Integer, primary_key=True)
    sessionid = db.Column(db.Integer)
    tabid = db.Column(db.Integer)
    windowid = db.Column(db.Integer)
    srcid = db.Column(db.Integer)
    url = db.Column(db.String())
    time = db.Column(db.Float())
    transition = db.Column(db.String())

    def __init__(json):
        self.sessionid = json['sessionID']
        self.tabid = json['tabid']
        self.windowid = json['windowid']
        self.srcid = json['srcid']
        self.url = json['url']
        self.time = json['time']
        self.transition = json['transition']

    def __repr__(self):
        return '<id {}>'.format(self.id)
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
