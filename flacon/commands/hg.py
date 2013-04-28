#from flask.ext.script import  Manager, Server, Shell, Option
from flask_script import Manager, Server, Shell, Option, Command
import os

DEFAULT_ROOT_PATH = os.path.abspath('.')


class HgRepo(object):
    def __init__(self, name='', local_path_base='../'):
        self.name = name
        self.local_path_base = local_path_base

    def local_path(self):
        return os.path.join(DEFAULT_ROOT_PATH, self.local_path_base, self.name)

repos = {}

class Hg(Command):
    def get_options(self):
        options = []

        options += (Option('-l', '--list',
                           action='store_true',
                           dest='print_list',
                           default=False),)

        return options

    def run(self, print_list):
        if print_list:
            self.run_print_list()

    def run_print_list(self):
        for r in repos.values():
            print r.name


class HgCommand(Command):
    def __init__(self, root_path=DEFAULT_ROOT_PATH):
        self.root_path = root_path


class HgPull(HgCommand):
    description = 'Hg pull command'

    def get_options(self):
        options = []
        return options

    def run(self):
        for repo in repos.values():
            path = repo.local_path()
            print '\t\t\t\033[1;35m[%s]\033[1;m' % repo.name
            print '\t\t\t', '-' * (len(repo.name) + 2)
            print '\n\033[1;33mTrying to change path to "%s"\033[1;m' % path,
            if os.path.isdir(path):
                os.chdir(path)
                print ' \033[1;32m[OK]\033[1;m\n'
                os.system('hg pull')
                os.system('hg update')
                print '\033[1;31m' + '=' * 80 + '\033[1;m'
                print


class HgClone(HgCommand):
    description = 'Hg clone command'

    def get_options(self):
        return Command.get_options(self)

    def run(self):
        print 'Hi from hg clone !'
