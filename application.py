import os
import unittest

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask import json

from app import blueprint
from app.main import create_app, db

from app.main.model import user
from app.main.model import blacklist
from app.main.model import recipe
from app.main.model import tag
from app.main.model import challenge
from app.main.model import image

application = app = create_app('prod')
app.register_blueprint(blueprint)

app.app_context().push()

manager = Manager(app)

migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)

@manager.command
def run():
   app.run()

@manager.command 
def spec():
   print(json.dumps(app.__schema__))

@manager.command
def test():
   """Runs the unit tests."""
   tests = unittest.TestLoader().discover('app/test', pattern='test*.py')
   result = unittest.TextTestRunner(verbosity=2).run(tests)
   if result.wasSuccessful():
      return 0
   return 1

@app.teardown_request
def teardown_request(exception):
    if exception:
        db.session.rollback()
    db.session.remove()

if __name__ == '__main__':
   manager.run()