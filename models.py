from sqlalchemy.dialects.postgresql import JSON, ARRAY

from app import db

class UserClusters(db.Model):
    """User-made or accepted clusterings"""
    __tablename__ = "user_clusters"
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.String(),nullable=False)
    name = db.Column(db.String(),nullable=False)
    keywords = db.Column(ARRAY(db.String()))
    cluster = db.Column(JSON,nullable=False)

    def __init__(self, json):
        self.userid = json['userID']
        self.name = json['name']
        self.keywords = json['keywords']
        self.cluster = json['cluster']

class UrlKeywords(db.Model):
    """Keywords metadata for a url, and clustering id based on them"""
    __tablename__ = "keywords"
    url = db.Column(db.String(), unique=True, primary_key=True)
    keywords = db.Column(ARRAY(db.String()))
    cluster = db.Column(db.Integer(), nullable=True)

    def __init__(self, url, *kws, group=None):
        self.url = url
        self.keywords = kws
        self.group = group

class UserGraph(db.Model):
    __tablename__ = "graphs"
    userid = db.Column(db.String(), unique=True, primary_key=True)
    data = db.Column(JSON,nullable=False)

    def __init__(self, userid, json):
        self.userid = userid
        self.json = json

class InteractionEvent(db.Model):
    __tablename__ = 'interactions'
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.String());
    event = db.Column(db.String());
    url = db.Column(db.String());
    time = db.Column(db.BigInteger());
    target = db.Column(db.String());
    
    def __init__(self, json):
        self.userid = json['userid']
        self.url = json['url']
        self.event = json['event']
        self.time = json['time']
        self.target = json['target']

class LinkClick(db.Model):
    __tablename__ = 'linkclicks'
    id = db.Column(db.Integer, primary_key=True)
    src = db.Column(db.String())
    dest = db.Column(db.String())
    time = db.Column(db.BigInteger());
    userid = db.Column(db.String());

    def __init__(self, json):
        self.src = json['from']
        self.dest = json['to']
        self.time = json['time']
        self.userid = json['userID']

class PageVisit(db.Model):
    __tablename__ = 'pagevisits'
    id = db.Column(db.Integer, primary_key=True)
    sessionid = db.Column(db.String())
    tabid = db.Column(db.Integer)
    windowid = db.Column(db.Integer)
    srcid = db.Column(db.Integer)
    url = db.Column(db.String())
    time = db.Column(db.Float())
    transition = db.Column(db.String())

    def __init__(self, json):
        self.sessionid = json['sessionID']
        self.tabid = json['tabID']
        self.windowid = json['windowID']
        self.srcid = json['srcID']
        self.url = json['url']
        self.time = json['time']
        self.transition = json['transition']

    def __repr__(self):
        return '<id {}>'.format(self.id)
