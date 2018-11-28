from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

from app import app
import models

manager = Manager(app)
migrate = Migrate(app, models.db)

def make_shell_context():
    return dict(app=app, db=models.db, News=models.News)

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command("db", MigrateCommand)


if __name__ == "__main__":
    manager.run()