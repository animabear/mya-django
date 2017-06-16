# coding=utf-8
import json

from django.http import HttpResponse
from django.conf import settings
from resource import MYAResource

"""
@param string template 模版路径，由模板所在顶层目录(相对于TEMPLATE_DIRS)和模板资源id构成，
                       即 template_base@template_path  eg. 'template/aweme_web@page/home/index.html'
@param dict   context  模版变量
"""
def get_html_response(request, template, context={}, env={}):
    template_data = template.split('@')
    if len(template_data) == 1:
        template_base = ''
        template_id   = template_data[0]
    else:
        template_base = template_data[0]
        template_id   = template_data[1]

    # 读取静态资源映射表
    with open('templates/' + template_base + '/map.json') as map_file:
        res_map = json.load(map_file)

    mya_resource = MYAResource(res_map)

    ctx = {
        '_mya_resource': mya_resource
    }
    ctx.update(context)

    t = env.get_template(template_base + '/' + template_id)
    html = t.render(ctx)
    mya_resource.load_page(template_id)
    html = mya_resource.render_response(html)

    return HttpResponse(html)