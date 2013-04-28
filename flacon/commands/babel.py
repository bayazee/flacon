from flask_script import Option, Command

import os


class Babel(Command):
    description = 'Babel command'

    def __init__(self, app):
        Command.__init__(self)
        self.app = app
        self.dir_name = os.path.join(app.root_path, 'translations')
        self.messages_file_path = os.path.join(self.dir_name, 'messages.pot')

    def get_options(self):
        options = []

        options += (Option('-m', '--make',
                           dest='lang_make',
                           type=str,
                           default=''),)

        options += (Option('-c', '--compile',
                           dest='lang_compile',
                           type=str,
                           default=''),)

        options += (Option('-u', '--update',
                           dest='lang_update',
                           type=str,
                           default=''),)

        options += (Option('-v', '--verbose',
                           action='store_true',
                           dest='verbose',
                           default=False),)

        return options

    def extract_messages(self, verbose=False):
        print 'Extracting messages from project ...'

        v = 'v' if verbose else 'q'

        cmd = 'pybabel -%s extract -F babel.cfg -k lazy_gettext --no-wrap -o %s --msgid-bugs-address bug@mydomain.com \
                    --copyright-holder Me --project %s --version 0.1 .'

        os.system(cmd % (v, self.messages_file_path, self.app.name))

    def run(self, lang_make, lang_update, lang_compile, verbose):
        if not os.path.exists(self.dir_name):
            os.mkdir(self.dir_name)

        if lang_make:
            self.extract_messages(verbose)
            os.system('pybabel init -i %s -d %s -l %s' % (self.messages_file_path, self.dir_name, lang_make))
        elif lang_update:
            self.extract_messages(verbose)
            os.system('pybabel update -i %s -d %s -l %s' % (self.messages_file_path, self.dir_name, lang_update))
        elif lang_compile:
            os.system('pybabel compile -d %s -l %s' % (self.dir_name, lang_compile))
