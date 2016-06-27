from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from scripts.keywordsExtract import main as extract_keywords
from scripts.generate_graphs import formatJSON
from scripts.Graph import *
import json
from models import *
import os

from app import app, db
app.config.from_object(os.environ['APP_SETTINGS'])

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

@manager.command
def generate_graphs():
    """Outputs graph data for the d3 front-end"""
    edges = [{'uid':e.uid, 'src':e.src, 'dest':e.dest, 'time':e.time}
             for e in db.engine.execute(
               """SELECT sessionid as uid, src, dest, lc.time \
                  FROM pagevisits as pv INNER JOIN linkclicks as lc \
                  ON (lc.userid = pv.sessionid AND (lc.src = pv.url OR \
                  lc.dest = pv.url))""")
            ]
    graphs = {}
    for e in edges:
        if e['uid'] is None or e['src'] is None or e['dest'] is None: continue
        if e['uid'] not in graphs:
            graphs[e['uid']] = Graph()
        graphs[e['uid']].addEdge(e['src'].strip(), e['dest'].strip())
    for gid, g in graphs.items():
        g_json = formatJSON(gid, g)
        with open(app.config['DATA_DIR'] + "%s.json" % gid, 'w') as f:
            f.write(json.dumps(g_json))

@manager.command
def update_keywords():
    """Reads urls in db and outputs their keywords"""
    kws = extract_keywords(*[p.url for p in PageVisit.query.limit(100).all()])
    with open(app.config['DATA_DIR'] + "keywords.json", 'w') as f:
        f.write(kws)

if __name__ == '__main__':
    manager.run()

