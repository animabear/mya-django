# coding=utf-8
import os
from django import template
from django.template.loader import get_template
from django.template import Context

register = template.Library()

class RequireNode(template.Node):
    def __init__(self, params):
        self.params = params

    def render(self, context):
        params = {}

        for item in self.params:
            key, value = item.split('=')
            params[key] = value.replace(r'"', '') # 去除参数中的引号

        name = params.get('name', '')
        # todo: 支持 defer async
        # 解析参数
        filename, extname = os.path.splitext(name)
        # todo: 支持多种文件格式
        # todo: 从map中读取
        if extname == '.js':
            return '<script src="%s"></script>' % (name)
        else:
            return '<link rel="stylesheet" href="%s" />' % (name)


def do_require(parser, token):
    try:
        contents = token.split_contents()
        tag_name = contents[0]
        params   = contents[1:]

    except ValueError:
        print 'params error'

    return RequireNode(params)


register.tag('require', do_require)

