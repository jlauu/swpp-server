import os
from flask import Flask, render_template, json, request
from flask_sqlalchemy import SQLAlchemy

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
        app.pv = data
        return "Recieved: " + data
    else:
        return "Bad request"

if __name__ == '__main__':
    app.run()
