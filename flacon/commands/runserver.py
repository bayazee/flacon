#from flask.ext.script import  Manager, Server, Shell, Option
from flask_script import Server, Option
from flacon.application import configure_app


class SimpleServer(Server):
    def __init__(self, app):

        Server.__init__(self)
        self.app = app

    def get_options(self):
        options = Server.get_options(self)

        options += (Option('-m', '--verbose_mongodb',
                           action='store_true',
                           dest='verbose_mongodb',
                           default=False),)

        options += (Option('--profile',
                           action='store_true',
                           dest='profile',
                           help='Init python profiler',
                           default=False),)

        exp = 'bugman' in self.app.config['INSTALLED_EXTENSIONS']
        if exp:
            options += (Option('-b', '--no-bugman',
                               action='store_false',
                               dest='use_bugman',
                               help='Deactivate Flask-Bugman',
                               default=exp),)

        else:
            options += (Option('-b', '--bugman',
                               action='store_true',
                               dest='use_bugman',
                               help='Activate Flask-Bugman',
                               default=exp),)
        return options

    def handle(self, app, host, port, use_debugger, use_reloader, threaded, processes, **kwargs):
        use_bugman = kwargs.pop('use_bugman')
        if use_bugman and not 'bugman' in self.app.config['INSTALLED_EXTENSIONS']:
            self.app.config['INSTALLED_EXTENSIONS'].append('bugman')
        elif not use_bugman and 'bugman' in self.app.config['INSTALLED_EXTENSIONS']:
            self.app.config['INSTALLED_EXTENSIONS'].remove('bugman')

        self.app.config['VERBOSE_MONGODB'] = kwargs.pop('verbose_mongodb')

        if kwargs.pop('profile'):
            from werkzeug.contrib.profiler import ProfilerMiddleware
            app.wsgi_app = ProfilerMiddleware(app.wsgi_app, file('profile.data', 'w'))

        app = configure_app(app)
        Server.handle(self, app, host, port, use_debugger, use_reloader, threaded, processes, False)
