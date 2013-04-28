#coding:utf8
from flask import current_app, request, after_this_request, g
from flask_auth import current_user
from werkzeug import cached_property


class UserLanguageDetector(object):
    def __init__(self):
        self.accept_languages = current_app.config.get('ACCEPT_LANGUAGES', {'fa': u'فارسی', 'en': 'English'}).keys()

    @cached_property
    def lang_request_arg(self):
        lang = request.args.get('lang')
        if lang not in self.accept_languages:
            lang = None
        return lang

    @cached_property
    def lang_cookie(self):
        lang = request.cookies.get('lang')
        if lang not in self.accept_languages:
            lang = None
        return lang

    def detect_user_language(self):
        try:
            if current_user.is_authenticated():
                if self.lang_request_arg:
                    return self.lang_request_arg
                # TODO; Make an API for getting language from user
                return current_user.language
        except AttributeError:
            pass

        if self.lang_request_arg:

            @after_this_request
            def remember_language(response):
                response.set_cookie('lang', self.lang_request_arg)
                return response

            return self.lang_request_arg
        elif self.lang_cookie:
            return self.lang_cookie


def detect_user_language():
    u = UserLanguageDetector()
    return u.detect_user_language()
