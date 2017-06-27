# coding=utf-8
import json
import os
import jinja2

from django.http import HttpResponse
from django.conf import settings
from .resource import MYAResource

# jinja2 extension
from jinja.extension.widget import WidgetExtension
from jinja.extension.script import ScriptExtension
from jinja.extension.style  import StyleExtension
from jinja.extension.html   import HtmlExtension, HtmlClostExtension
from jinja.extension.filter import jsonify

j2_env = jinja2.Environment(loader=jinja2.FileSystemLoader(settings.TEMPLATE_DIRS),
                        extensions=[WidgetExtension, ScriptExtension, StyleExtension, HtmlExtension, HtmlClostExtension])

jinja2.filters.FILTERS['jsonify'] = jsonify # for comp
j2_env.filters['jsonify'] = jsonify # for global
# end extension

try:
    TEMPLATE_DIRS = settings.TEMPLATE_DIRS[0]
except:
    TEMPLATE_DIRS = 'templates'


"""
@param string template 模版路径，由模板所在顶层目录(相对于TEMPLATE_DIRS)和模板资源id构成，
                       即 template_base@template_path  eg. 'template/aweme_web@page/home/index.html'
@param dict   context  模版变量
"""
def view(request, template, context={}):
    template_data = template.split('@')
    if len(template_data) == 1:
        template_base = ''
        template_id   = template_data[0]
    else:
        template_base = template_data[0]
        template_id   = template_data[1]

    # 读取静态资源映射表
    map_path = os.path.join(TEMPLATE_DIRS, template_base, 'map.json')

    try:
        with open(map_path) as map_file:
            res_map = json.load(map_file)
    except:
        res_map = {'res': {}, 'pkg': {}}

    mya_debug = request.GET.get('mya_debug') == '1'
    mya_resource = MYAResource(res_map, mya_debug)

    ctx = {
        '_mya_resource': mya_resource
    }
    ctx.update(context)

    t = j2_env.get_template(template_base + '/' + template_id)
    html = t.render(ctx)
    mya_resource.load_page(template_id) # 最后load入口页面依赖的资源
    html = mya_resource.render_response(html)

    return HttpResponse(html)