# coding=utf-8
import json

from django.shortcuts import render_to_response
from django.template.loader import get_template
from django.template import Context
from django.template import RequestContext
from django.http import HttpResponse
from .mya_resource import MYAResource

def index(request):
    # 读取静态资源映射表
    with open('templates/map.json') as map_file:
        res_map = json.load(map_file)

    mya_resource = MYAResource(res_map)

    ctx = {
        'name': '<script>animabear</script>',
        'age': '25',
        '_mya_resource': mya_resource
    }

    t = get_template('pages/index.html')
    c = Context(ctx)
    html = t.render(c)

    print mya_resource.get_deps()

    return HttpResponse(html)

