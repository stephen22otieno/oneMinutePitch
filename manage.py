from flask_script import Manager,Server
from app import create_app,db
from app.models import User,Category,Peptalk,Comments

from flask_migrate import Migrate, MigrateCommand


app = create_app('development')

manager =Manager(app)
migrate = Migrate(app,db)
manager.add_command('server',Server)
manager.add_command('db', MigrateCommand)
app = create_app('test')

@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('test')
    unittest.TextTestRunner(verbosity=2).run(tests)


@manager.shell
def make_shell_contex():
        return dict(app = app, db = db, Category = Category, User = User, Peptalk = Peptalk, Comments = Comments)

if __name__ == '__main__':
    manager.run()
