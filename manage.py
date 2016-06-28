from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from sqlalchemy.sql import text
from scripts.keywordsExtract import keywords as extract_keywords
from scripts.generate_graphs import formatJSON
from scripts.Graph import *
import json, os
from models import *

from app import app, db
app.config.from_object(os.environ['APP_SETTINGS'])

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)
edges_query =  """SELECT sessionid as uid, src, dest, lc.time \
                  FROM pagevisits as pv INNER JOIN linkclicks as lc \
                  ON (lc.userid = pv.sessionid AND (lc.src = pv.url OR \
                  lc.dest = pv.url))"""
def upsert_graphs(userid, data):
    return text("""INSERT INTO graphs (userid, data) VALUES(:userid, :data) \
                ON CONFLICT (userid) DO UPDATE SET data = EXCLUDED.data;""").\
                bindparams(userid=userid,data=data)
def upsert_keywords(url, keywords):
    return text("""INSERT INTO keywords (url, keywords) VALUES(:url,:kws) \
                ON CONFLICT (url) DO UPDATE \
                SET keywords = EXCLUDED.keywords;""").\
                bindparams(url=url,kws=keywords)
@manager.command
def generate_graphs():
    """Outputs graph data for the d3 front-end"""
    edges = [{'uid':e.uid, 'src':e.src, 'dest':e.dest, 'time':e.time}
             for e in db.engine.execute(edges_query)]
    graphs = {}
    for e in edges:
        if e['uid'] is None or e['src'] is None or e['dest'] is None: continue
        if e['uid'] not in graphs:
            graphs[e['uid']] = Graph()
        graphs[e['uid']].addEdge(e['src'].strip(), e['dest'].strip())
    queries = []
    for gid, g in graphs.items():
        json_str = json.dumps(formatJSON(gid, g))
        queries.append(upsert_graphs(gid, json_str))
    for q in queries:
        db.engine.execute(q)

@manager.command
def update_keywords():
    """Reads urls in db and outputs their keywords"""
    urls = []
    queries = []
    attempted = set()
    # find keywords for only urls we display on the graph
    for nodes in [row.data['nodes'] for row in UserGraph.query.all()]:
        urls.extend(n['url'] for n in nodes)
    for i,url in enumerate(urls):
        if url in attempted: continue
        attempted.add(url)
        try:
            kws = extract_keywords(url)
        except:
            continue
        queries.append(upsert_keywords(url, kws))
    for q in queries:
        db.engine.execute(q)

if __name__ == '__main__':
    manager.run()
