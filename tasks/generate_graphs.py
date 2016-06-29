from flask_script import Command
from sqlalchemy.sql import text
from json import dumps
from scripts.GraphUtils import *
from app import db
from models import UrlKeywords

edges_query =  """SELECT sessionid as uid, src, dest, lc.time \
                  FROM pagevisits as pv INNER JOIN linkclicks as lc \
                  ON (lc.userid = pv.sessionid AND (lc.src = pv.url OR \
                  lc.dest = pv.url))"""

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
        for uid, g in graphs.items():
            clusters = self.getClusters(g)
            json = formatJSON(uid, g, clusters)
            query = upsert_graphs(uid, json)
            db.engine.execute(upsert_graphs(uid, dumps(json)))

    def getClusters(self, graph):
        """Creates a map from node ids to their cluster"""
        nodes = graph.ids
        clusters = {}
        rows = UrlKeywords.query.filter(UrlKeywords.url.in_(nodes.keys()))
        for url, cluster in [ (row.url, row.cluster) for row in rows]:
            if cluster is not None:
                clusters[nodes[url]] = cluster
        return clusters
