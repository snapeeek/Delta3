# manage.py

from flask_migrate import MigrateCommand
from flask_script import Manager

from Delta3Mini import create_app, db

manager = Manager(create_app())

manager.add_command('db', MigrateCommand)

if __name__ == "__main__":
    manager.run()
