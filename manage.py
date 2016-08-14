
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

from src import app, db
from src.models import GUser


migrate = Migrate(app, db)
manager = Manager(app)

# Migrations
manager.add_command("db", MigrateCommand)

@manager.command
def create_db():
    """
    Creates the db tables.
    """
    db.create_all()


@manager.command
def drop_db():
    """
    Drops the db tables.
    """
    db.drop_all()

@manager.command
def create_admin():
    """
    Creates the admin user.
    """
    db.session.add(GUser(email="ad@min.com", password="admin", admin=True))
    db.session.commit()


@manager.command
def create_data():
    """
    Creates sample data.
    """
    pass

@manager.command
def run():
    socketio.run(app,
        host="127.0.0.1",
        port=5000,
        use_reloader=True
        # use_reloader=False,
    )

if __name__ == "__main__":
    manager.run()
