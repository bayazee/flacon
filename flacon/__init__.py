from flask.ext.script import Manager, Shell

from flacon.application import create_app
from flacon.commands.runserver import SimpleServer
from flacon.commands.babel import Babel


def exec_manager(app_name, config=None):
    app = create_app(app_name, config)
    manager = Manager(app, with_default_commands=False)
    manager.add_command("shell", Shell())
    manager.add_command("runserver", SimpleServer(app))
    manager.add_command("babel", Babel(app))
    manager.run()
