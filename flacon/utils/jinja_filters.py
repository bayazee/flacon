from flask import request, url_for
from .calverter import Calverter


def jalali(value):
    """
    This function given Gregorian Date and convert to Jalali date with help of Calverter lib.

    :param value: gregorian Date
    :type value: Date or DateTime Object

    :returns: Jalali Date
    :rtype: String
    """
    if not value:
        return ''
    calverter = Calverter()
    jd = calverter.gregorian_to_jd(value.year, value.month, value.day)
    jalali = calverter.jd_to_jalali(jd)
    return "%s/%s/%s" % jalali


def url_for_other_page(page):
    """
    This function create link with same arg and add pagination to it

    :param page: page number for create url
    :type page: String

    :returns: Url with page number added
    :rtype: String
    """
    request_args = request.args.to_dict()
    request_args['page'] = page
    return url_for(request.endpoint, **request_args)


def init_filters(app):
    """
    This Function register all filter for Jinja template manager.
    """
    #@TODO: add local date like ghamari and ...
    app.jinja_env.globals['format_date'] = jalali
    app.jinja_env.globals['url_for_other_page'] = url_for_other_page
