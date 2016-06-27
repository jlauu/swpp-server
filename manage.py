from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from scripts.keywordsExtract import main as extract_keywords
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
upsert_query = """INSERT INTO graphs (userid, data) VALUES({0},'{1}') \
                  ON CONFLICT (userid) DO UPDATE SET data = EXCLUDED.data;"""
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
        queries.append(upsert_query.format(gid, json_str))
    db.engine.execute("".join(queries).replace("%","%%"))

@manager.command
def update_keywords():
    """Reads urls in db and outputs their keywords"""
    kws = extract_keywords(*[p.url for p in PageVisit.query.limit(100).all()])
    with open(app.config['DATA_DIR'] + "keywords.json", 'w') as f:
        f.write(kws)

if __name__ == '__main__':
    manager.run()
