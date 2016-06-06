from app import db
from sqlalchemy.dialects.postgresql import TIMESTAMP

class PageVisit(db.Model):
    __tablename__ = 'pagevisits'
    id = db.Column(db.Integer, primary_key=True)
    sessionid = db.Column(db.Integer)
    tabid = db.Column(db.Integer)
    windowid = db.Column(db.Integer)
    srcid = db.Column(db.Integer)
    url = db.Column(db.String())
    time = db.Column(TIMESTAMP)
    transition = db.Column(db.String())

    def __init__(self):
        pass

    def __repr__(self):
        return '<id {}>'.format(self.id)
