# coding=utf-8
import json

from django.shortcuts import render_to_response
from django.template.loader import get_template
from django.template import Context
from django.template import RequestContext
from django.http import HttpResponse


def index(request):
    # 读取静态资源映射表
    with open('templates/map.json') as map_file:
        map_data = json.load(map_file)

    t = get_template('pages/index.html')
    c = Context({ 'name': '<script>animabear</script>', 'age': '25', '_map_data': map_data })
    html = t.render(c)

    return HttpResponse(html)


def test(request):
    # 读取静态资源映射表
    with open('templates/map.json') as map_file:
        map_data = json.load(map_file)

    ctx = {
        'name': '<script>animabear</script>',
        'age': '25',
        '_map_data': {'a': 1},
        '_deps': []
    }

    t = get_template('pages/index.html')
    c = Context(ctx)
    html = t.render(c)

    print ctx.get('_deps')

    return HttpResponse(html)

