from flask import Blueprint
from werkzeug.utils import import_string, cached_property


class LazyView(object):
    """
    Creates Lazy View to use in BluePrint function.
    """

    def __init__(self, view_func_path, import_prefix=None):
        self.view_func_path = view_func_path
        self.__name__ = view_func_path.rsplit('.', 1)[-1] if '.' in view_func_path else view_func_path
        self.view_name = self.__name__
        self.import_prefix = import_prefix

    @property
    def abs_view_func_path(self):
        if self.import_prefix:
            return self.import_prefix + '.' + self.view_func_path
        else:
            return self.view_func_path

    @cached_property
    def view(self):
        return import_string(self.abs_view_func_path)

    def __call__(self, *args, **kwargs):
        if hasattr(self.view, 'as_view'):
            # class based view
            return self.view.as_view(self.view_name)(*args, **kwargs)
        return self.view(*args, **kwargs)


def create_blueprint(name, import_name, url_prefix, import_prefix, rules):
    """
    This function Create BluePrint and return it.
    """
    bp = Blueprint(name, import_name, url_prefix=url_prefix)
    for rule in rules:
        options = rule[2] if len(rule) > 2 else {}

        view = LazyView(rule[1], import_prefix) if isinstance(rule[1], str) else rule[1]

        bp.add_url_rule(rule[0], view_func=view, methods=options.get('methods'))
    return bp
