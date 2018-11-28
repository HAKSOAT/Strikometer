from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

from app import app, db
from models import News

manager = Manager(app)
migrate = Migrate(app, db)

def make_shell_context():
    return dict(app=app, db=db, News=News)

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command("db", MigrateCommand)


if __name__ == "__main__":
    manager.run()