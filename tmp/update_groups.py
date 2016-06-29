from app import db
from sqlalchemy.sql import text

with open('tmp/url-cluster-em-100words.csv') as f:
    skip = True
    urls = []
    for line in f:
        if skip:
            skip = False
            continue
        parts = line.rpartition(',')
        group = parts[-1].strip()
        url = parts[0].partition(',')[-1].strip()
        urls.append((url,int(group)))
    
def mkq(u,g):
    return text("INSERT INTO keywords (url, keywords, cluster) VALUES (:u, '{}', :g) ON CONFLICT (url) DO UPDATE SET cluster = EXCLUDED.cluster;").bindparams(u=u,g=g)

for u, g in urls:
    db.engine.execute(mkq(u,g))
