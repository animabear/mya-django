# coding=utf-8

from jinja2.utils import htmlsafe_json_dumps

def jsonify(value):
    return htmlsafe_json_dumps(value)