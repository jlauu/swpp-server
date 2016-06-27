from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from scripts.keywordsExtract import main as extract_keywords
from models import *
import os

from app import app, db
app.config.from_object(os.environ['APP_SETTINGS'])

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

@manager.command
def update_keywords():
    """Reads urls in db and outputs their keywords"""
    kws = extract_keywords(*[p.url for p in PageVisit.query.limit(100).all()])
    with open(app.config['DATA_DIR'] + "keywords.json", 'w') as f:
        f.write(kws)

if __name__ == '__main__':
    manager.run()

