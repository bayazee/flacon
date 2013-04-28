class DefaultConfig(object):
    # Essentials

    DEBUG = True
    DEPLOYMENT = False

    SECRET_KEY = 'SECRET_KEY'

    MAIN_URL = 'http://127.0.0.1:5000'
    MAIN_STATIC_URL = 'http://static.127.0.0.1:5000'

    INSTALLED_EXTENSIONS = []
    INSTALLED_BLUEPRINTS = []

    if DEBUG:
        LOG_FORMAT = '\033[1;35m[%(asctime)s]\033[1;m [\033[1;31m %(levelname)s \033[1;m] \033[1;32m[%(logger_name)s]\033[1;m: \
        \033[1;33m %(message)s \033[1;m'
    else:
        LOG_FORMAT = '[%(asctime)s] %(levelname)s [%(logger_name)s]: %(message)s'
