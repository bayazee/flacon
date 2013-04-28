from flask import Flask
from flask_script import Manager

from flacon.commands.createproject import CreateProject


def exec_manager():
    flacon = Flask(__name__)
    manager = Manager(flacon, with_default_commands=False)
    manager.add_command("createproject", CreateProject())
    manager.run()

exec_manager()
