import os
from urllib.parse import urlencode
from flask import Flask, request, json, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_ 
from sqlalchemy.sql import text

app = Flask(__name__, static_folder='static', static_url_path='')
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import *

@app.route('/', methods=['GET'])
def index():
  if request.args.get('uid') is not None:
      userid = request.args.get('uid')
      clusters = UserCluster.query.filter_by(userid=userid).all()
      name = request.args.get('name')
      clusters = [{
          'id' : c.id,
          'name': c.name, 
          'keywords': c.keywords, 
          'graph': c.cluster
      } for c in clusters if not name or name == c.name]
      h = ClusterHieararchy.query.filter_by(userid=userid).first()
      return json.dumps({clusters: clusters, hierarchy: h})
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
   if userid and name:
       graph = UserCluster.query.filter(and_(UserCluster.name==name, UserCluster.userid==userid)).first()
       return render_template('graph.html', json=graph.cluster)
   elif userid:
       names = [ c.name for c in UserCluster.query.filter_by(userid=userid).all()]
       url = "https://swpp-server-stage.herokuapp.com/clusters?"
       links = [ '<a href="{0}{1}">{2}</a>'.format(url, urlencode({'uid':userid,'name':n}), n) for n in names ] 
       return "Names for user {0}:<br>{1}".format(userid,'<br>'.join(links))
   else:
       return "Bad query"

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
            [upsertUserCluster(c) for c in map(UserCluster, data)]
        elif ty == 'forest':
            upsertHierarchy(ClusterHierarchy(data))
        else:
            return "Bad request (%s): %s".format(ty, request)
        return "Received: " + ty
    else:
        return "Bad request: " + str(data)

def upsertHierarchy(f):
    query = text("""INSERT INTO cluster_hierarchy as ch (userid, data)\
                 VALUES(:u, :d) ON CONFLICT (userid) DO UPDATE SET \
                 data = EXCLUDED.data;""").\
                 bindparams(u=f.userid, d=f.data)
    db.engine.execute(query)
    

def upsertUserCluster(c):
    print("UPSERTING...")
    [print(type(a), a) for a in [c.userid, c.name, c.keywords, c.cluster]]
    if c.id:
        query = text("""INSERT INTO user_clusters as cs (id, userid, name, keywords, cluster)\
                VALUES(:i, :u, :n, :k, :cls) ON CONFLICT (id) DO UPDATE SET \
                     name = EXCLUDED.name,\
                     keywords = EXCLUDED.keywords,\
                     cluster = EXCLUDED.cluster;""").\
                     bindparams(i=c.id, u=c.userid, n=c.name, k=c.keywords, cls=c.cluster)
    else:
        query = text("""INSERT INTO user_clusters as cs (userid, name, keywords, cluster)\
                     VALUES(:u, :n, :k, :cls) ON CONFLICT (userid, name) DO UPDATE SET \
                     keywords = EXCLUDED.keywords, cluster = EXCLUDED.cluster;""").\
                     bindparams(u=c.userid, n=c.name, k=c.keywords, cls=c.cluster)

    db.engine.execute(query)


if __name__ == '__main__':
    app.run()
