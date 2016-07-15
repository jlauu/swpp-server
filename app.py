import os
from flask import Flask, request, json, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_ 

app = Flask(__name__, static_folder='static', static_url_path='')
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import *

@app.route('/', methods=['GET'])
def index():
  if request.args.get('uid') is not None:
      userid = request.args.get('uid')
      graphs = UserCluster.query.filter_by(userid=userid)
      return json.dumps(graphs)
  else:
      return ""

@app.route('/graph', methods=['GET'])
def graph():
   graph = UserGraph.query.filter_by(userid=request.args.get('uid')).first()
   return render_template('graph.html', json=graph.data)

@app.route('/clusters', methods=['GET'])
def clusters():
   name = request.args.get('name')
   userid = request.args.get('uid')
   graph = UserCluster.query.filter_by(name=name).filter_by(userid=userid).first()
   return render_template('graph.html', json=graph.cluster)

@app.route('/send', methods=['POST'])
def send():
    if request.headers['Content-type'] == 'application/json':
        msg = request.get_json()
        ty = msg['type']
        data = msg['data']
        if ty == 'pages':
            [db.session.add(pv) for pv in map(PageVisit, data)]
            db.session.commit()
        elif ty == 'links':
            [db.session.add(l) for l in map(LinkClick, data)]
            db.session.commit()
        elif ty == 'interactions':
            [db.session.add(i) for i in map(InteractionEvent, data)]
            db.session.commit()
        elif ty == 'cluster':
            [db.session.add(c) for c in map(UserCluster, data)]
            db.session.commit()
        else:
            return "Bad request (%s): %s".format(ty, request)
        return "Received: " + ty
    else:
        return "Bad request: " + str(data)

if __name__ == '__main__':
    app.run()
