import re
import os
import sys
import shutil
from jinja2 import Template
from flask_script import Command, Option


def render_file(path, **kwargs):
    text = file(path, 'r').read()
    template = Template(text)
    file(path, 'w').write(template.render(kwargs))


class CreateProject(Command):
    description = 'Create new flask project'

    def get_options(self):
        options = []

        options += (Option('-n', '--name',
                           dest='name',
                           type=str,
                           default='33'),)
        return options

    def run(self, name):
        if not re.search(r'^[a-zA-Z][a-zA-Z0-9\-_]*$', name):
            print '%r is not a valid project name.' % name
            sys.exit(1)

        if os.path.exists(name):
            print 'Folder with name "%s" already exists.' % name
            sys.exit(1)
        import flacon
        source = os.path.join(flacon.__path__[0], 'project_template')
        shutil.copytree(source, name)
        path_join = lambda path: os.path.join(name, path)

        for fn in os.listdir(name):
            if fn.endswith('.py_tmpl'):
                os.rename(path_join(fn), path_join(fn.replace('_tmpl', '')))

        render_file(path_join('manage.py'), project_name=name)
        render_file(path_join('config.py'), project_name=name, secretkey=os.urandom(24).encode('hex'))
