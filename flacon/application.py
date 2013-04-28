from flask import Flask, request, jsonify, redirect, url_for, flash, render_template
from flacon.config import DefaultConfig
from werkzeug.utils import import_string, ImportStringError

__all__ = ['create_app']

try:
    from flask.ext.babel import gettext as _
except ImportError:
    _ = lambda x: x


def create_app(app_name, config):
    """
    This Function Create of Configure main application.

    Tabe asli hast ke app ro misaze va configesh mikone.

    Function resive Configuration as config and Appilication Name as app_name then create and return new app.

    :param config: Class or Object of setting's
    :type config: Class or Object
    :param app_name: Appilication Names's
    :type app_name: String

    :returns: Appilication Object
    :rtype: Object
    """

    #TODO: static_folder va template_folder bayad dar method joda set beshe
    app = Flask(app_name, static_folder='media/static', template_folder='media/templates')
    load_configs(app, config)
    return app


def configure_app(app):
    configure_logging(app)
    configure_balot(app)
    configure_errorhandlers(app)
    configure_extensions(app)
    configure_blueprints(app)
    configure_before_first_request_handlers(app)
    configure_before_request_handlers(app)
    configure_after_request_handlers(app)
    configure_i18n(app)
    configure_admin(app)
    configure_jinja_filters(app)
    configure_extra(app)
    configure_mimetypes()
    run_initializers(app)
    return app


def load_configs(app, config):
    """
    All Application Configure load or assigned with this function.

    Configuration usually stored in single file on root of application.

    :param config: Object of setting's
    :type config: Object
    :param app: Appilication Object
    :type app: Object
    """

    if config:
        # agar config degari be create_app ersal shode bashe dar in bakhsh load mishe
        # agar tanzimate in bakhsh gablan va dakhele defalt config tanzim shode bashe dobare nevisi mishe
        app.config.from_object(config)
    else:
        # config default ro dakhele app load mikone
        app.config.from_object(DefaultConfig())

    # dar sorati ke environment variable baraye tanzimat set shode bashe ham load mishe
    app.config.from_envvar('%s_CONFIG' % app.name.upper(), silent=True)

    # TODO: temp template rule for testing
#    from jinja2 import StrictUndefined
#    app.jinja_env.undefined = StrictUndefined


def configure_blueprints(app):
    """
    Flaskext Blueprint functionality (configuration or installing) handling in this function.

    :param app: Application Object
    :type app: Object
    """

    app.config.setdefault('INSTALLED_BLUEPRINTS', [])

    for bp_name in app.config['INSTALLED_BLUEPRINTS']:
        bp_urls = import_string('%s.%s.urls' % (app.name, bp_name))
        app.register_blueprint(bp_urls.blueprint)

        bp_module = import_string('%s.%s' % (app.name, bp_name))
        if hasattr(bp_module, '__initializers__'):
            for func in getattr(bp_module, '__initializers__'):
                func(app, bp_urls.blueprint)


def configure_logging(app):
    """
    This function Configure Logger for given Application.

    :param app: Application Object
    :type app: Object
    """

    from flacon.utils.extended_logging import wrap_app_logger
    wrap_app_logger(app)


def configure_balot(app):
    if not app.config.get('USE_BALOT'):
        return

    from balot import FlaskBalotHandler
    import logging

    app.config.setdefault('BALOT_DB_URI', None)
    app.config.setdefault('BALOT_DB_NAME', None)
    app.config.setdefault('BALOT_LOG_LEVEL', logging.NOTSET)

    balot_handler = FlaskBalotHandler(app.config['BALOT_APP_ID'], app.config['BALOT_DB_URI'], app.config['BALOT_DB_NAME'],
                                      level=app.config['BALOT_LOG_LEVEL'])

    app.logger.addHandler(balot_handler)


def configure_i18n(app):
    """
    This Function Configure I18n Setting for application translate.

    :param app: Application Object
    :type app: Object
    """

    if not app.config.get('USE_I18N'):
        return

    babel = app.extensions['babel']
    from .i18n import detect_user_language
    from flask.ext.babel import get_locale

    @app.context_processor
    def inject_lang():
        l = get_locale()
        if l.language in ("he", "ar", "fa"):
            direction = 'rtl'
        else:
            direction = 'ltr'

        return dict(locale=l, lang=l.language, lang_direction=direction)

    @babel.localeselector
    def get_user_locale():
        return detect_user_language()


def configure_admin(app):
    if not app.config.get('USE_ADMIN'):
        return

    def get_db(app):
        # TODO: Make db connection configurable

        from pymongo import Connection

        host = app.config['MONGODB_HOST']
        port = app.config['MONGODB_PORT']
        database = app.config['MONGODB_DATABASE']

        return Connection(host, port)[database]

    db = get_db(app)

    admin = app.extensions['admin'][0]
    for bp_name in app.config['INSTALLED_BLUEPRINTS']:
        try:
            bp_admin = import_string('%s.%s.admin' % (app.name, bp_name))
        except ImportStringError as e:
            continue

        views = bp_admin.get_views(db)
        for view in views:
            admin.add_view(view)


def configure_errorhandlers(app):
    """
    This Function register regular error in error handler for raise intelligible Error.

    :param app: Appilication Object
    :type app: Object
    """

    if app.testing:
        return

    @app.errorhandler(404)
    def page_not_found(error):
        """
        Standard Page Not Found Error(404).

        Function check request is_xhr flag, if request is a xmlHttpRequest (Ajax) then return jsonify 404 Error else return plane html 404 Error.

        :param error: Error message
        :type error: String

        :returns: Standard 404 Page Not Found Error (Plane HTML or Jsonify)
        :rtype: Plane HTML of Json
        """
        if request.is_xhr:
            return jsonify(error=_('Sorry, page not found'))
        return render_template("errors/404.html", error=error), 404

    @app.errorhandler(403)
    def forbidden(error):
        """
        Standard Not Allowed Error(403).

        Function check request is_xhr flag, if request is a xmlHttpRequest (Ajax) then return jsonify 403 Error elsev return plane html 403 Error.

        :param error: Error message
        :type error: String

        :returns: Standard 403 Not Allowed Error (Plane HTML or Jsonify)
        :rtype: Plane HTML of Json
        """
        if request.is_xhr:
            return jsonify(error=_('Sorry, not allowed'))
        return render_template("errors/403.html", error=error), 403

    @app.errorhandler(500)
    def server_error(error):
        """
        Standard Internal Server Error(500).

        Function check request is_xhr flag, if request is a xmlHttpRequest (Ajax) then return jsonify 500 Error else return plane html 500 Error.

        :param error: Error message
        :type error: String

        :returns: Standard 500 Internal Server Error (Plane HTML or Jsonify)
        :rtype: Plane HTML of Json
        """
        if request.is_xhr:
            return jsonify(error=_('Sorry, an error has occurred')), 500
        return render_template("errors/500.html", error=error)

    @app.errorhandler(401)
    def unauthorized(error):
        """
        Standard Login required Error(401).

        Function check request is_xhr flag, if request is a xmlHttpRequest (Ajax) then return jsonify 401 Error else return plane html 401 Error.

        :param error: Error message
        :type error: String

        :returns: Standard 401 Login required Error (Plane HTML or Jsonify)
        :rtype: Plane HTML of Json
        """
        if request.is_xhr:
            return jsonify(error=_("Login required"))
        flash(_("Please login to see this page"), "error")
        return redirect(url_for("%s.login" % app.name, next=request.path))


def configure_extensions(app):
    """
    This function Configure all Extention's for Appilication.

    This function for each name in INSTALLED_EXTENSIONS key of app.config dict import extention's and initial it whit init_app method.

    :param app: Application Object
    :type app: Object
    """
    for ext_name in app.config['INSTALLED_EXTENSIONS']:
        ext = import_string('%s.extensions.%s' % (app.name, ext_name))
        ext.init_app(app)


def configure_jinja_filters(app):
    """
    This function configure Jinja Template engine Filters.

    :param app: Application Object
    :type app: Object
    """
    from flacon.utils.jinja_filters import init_filters
    init_filters(app)


def configure_before_first_request_handlers(app):
    """
    This function configure befor first request handlers

    :param app: Application Object
    :type app: Object
    """

    handlers = app.config.get('BEFORE_FIRST_REQUEST')
    if handlers:
        for handler_path in handlers:
            func = import_string(handler_path)
            app.before_first_request(func)


def configure_before_request_handlers(app):
    """
    This function configure befor request handlers

    :param app: Application Object
    :type app: Object
    """

    handlers = app.config.get('BEFORE_REQUEST_HANDLERS')
    if handlers:
        for handler_path in handlers:
            func = import_string(handler_path)
            app.before_request(func)


def configure_after_request_handlers(app):
    """
    This function configure after request handlers

    :param app: Application Object
    :type app: Object
    """

    handlers = app.config.get('AFTER_REQUEST_HANDLERS')
    if handlers:
        for handler_path in handlers:
            func = import_string(handler_path)
            app.after_request(func)


def configure_extra(app):
    """
    This function Configure main Application

    :param app: Application Object
    :type app: Object
    """

#    def handle_unregistered_user():
#        pass
#    app.before_request(handle_unregistered_user)

    @app.after_request
    def no_cache_headers(response):
        # add no-cache headers if not cache-headers added
        if 'Cache-Control' not in response.headers:
            response.headers.add('Expires', '01 Jan 2000 12:00:00 GMT')
            response.headers.add('Cache-Control', 'no-cache, no-store, max-age=0, must-revalidate')
            response.headers.add('Pragma', 'no-cache')
        return response

    if app.config['DEBUG']:
        @app.after_request
        def after_request(response):
            # allow all cross domain requests in debug mode
            if request.headers.get('Origin'):
                response.headers.add('Access-Control-Allow-Origin', request.headers.get('Origin'))
                response.headers.add('Access-Control-Allow-Credentials', 'true')
            return response


def configure_mimetypes():
    import os
    import mimetypes

    our_mime_types = os.path.abspath(
                        os.path.normpath(
                            os.path.join(os.path.dirname(__file__),
                                         './mime.types')))
    if our_mime_types not in mimetypes.knownfiles:
        mimetypes.knownfiles.append(our_mime_types)
        mimetypes.init()


def run_initializers(app):
    initializers = app.config.get('INITIALIZERS')
    if initializers:
        for init_path in initializers:
            func = import_string(init_path)
            func(app)
