# coding=utf-8
import json

from django.shortcuts import render_to_response
from django.template.loader import get_template
from django.template import Context, RequestContext
from django.http import HttpResponse
from resource import MYAResource

from jinja2 import Template

def get_html_response(request, template, context={}):
    return render_to_response(template, context, context_instance=RequestContext(request))


# django
def index(request):
    return get_html_response(request, 'pages/index.html', {
        'name': 'animabear',
        'user': {
            'username': 'xjj',
            'age':  25
        }
    })


# jinja
def jinja2(request):
    # 读取静态资源映射表
    with open('templates/map.json') as map_file:
        res_map = json.load(map_file)

    mya_resource = MYAResource(res_map)

    ctx = {
        'name': '<script>animabear</script>',
        'age': '25',
        'user': {
            'username': '<script>xjj</script>',
            'age':  25
        },
        '_mya_resource': mya_resource
    }

    t = get_template('pages/jinja2.html')
    html = t.render(ctx)
    html = mya_resource.render_response(html)

    return HttpResponse(html)
