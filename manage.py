import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from sqlalchemy.sql import text
from scripts.keywordsExtract import keywords as extract_keywords
from models import *
from tasks.generate_graphs import GenerateGraphs

from app import app, db
app.config.from_object(os.environ['APP_SETTINGS'])

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)
manager.add_command('generate_graphs', GenerateGraphs())

edges_query =  """SELECT sessionid as uid, src, dest, lc.time \
                  FROM pagevisits as pv INNER JOIN linkclicks as lc \
                  ON (lc.userid = pv.sessionid AND (lc.src = pv.url OR \
                  lc.dest = pv.url))"""
def upsert_keywords(url, keywords):
    return text("""INSERT INTO keywords (url, keywords) VALUES(:url,:kws) \
                ON CONFLICT (url) DO UPDATE \
                SET keywords = EXCLUDED.keywords;""").\
                bindparams(url=url,kws=keywords)

@manager.command
def generate_graphs():
    """Outputs graph data for the d3 front-end"""

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
