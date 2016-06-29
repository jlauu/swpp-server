from flask_script import Command
from sqlalchemy.sql import text
from json import dumps
from scripts.GraphUtils import *
from app import db

def upsert_graphs(userid, data):
    return text("""INSERT INTO graphs (userid, data) VALUES(:userid, :data) \
                ON CONFLICT (userid) DO UPDATE SET data = EXCLUDED.data;""").\
                bindparams(userid=userid,data=data)

class GenerateGraphs(Command):
    """Compiles graph data and produces a json for the d3 front-end"""

    def run(self):
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
            json = dumps(formatJSON(gid, g))
            queries.append(upsert_graphs(gid, json))
        for q in queries:
            db.engine.execute(q)
