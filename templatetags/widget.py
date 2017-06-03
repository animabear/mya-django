# coding=utf-8

from django import template
from django.template.loader import get_template
from django.template import Context

register = template.Library()

# widget标签的默认参数
default_params = ['name', 'mode']

@register.tag(name="widget")
def do_widget(parser, token):
    try:
        contents = token.split_contents()
        tag_name = contents[0]
        params   = contents[1:]

    except ValueError:
        print 'params error'

    return WidgetNode(params)


class WidgetNode(template.Node):
    def __init__(self, params):
        self.params = params

    def render(self, context):
        params = {}
        ctx_params = {}

        for item in self.params:
            key, value = item.split('=')
            real_value = value.replace(r'"', '') # 去除参数中的引号
            if key not in default_params:
                try:
                    ctx_params[key] = template.Variable(real_value).resolve(context)
                except:
                    ctx_params[key] = ''
            else:
                params[key] = real_value

        name = params.get('name', '')
        mode = params.get('mode', '')

        t = get_template(name)
        html = t.render(Context( ctx_params ))
        return html
