from flask import make_response
from functools import update_wrapper


def never_cache(f):
    def new_func(*args, **kwargs):
        response = make_response(f(*args, **kwargs))
        response.cache_control.no_cache = True
        response.headers.add('Expires', '01 Jan 2000 12:00:00 GMT')
        response.headers.add('Cache-Control', 'no-cache, no-store, max-age=0, must-revalidate')
        response.headers.add('Pragma', 'no-cache')
        return response
    return update_wrapper(new_func, f)
