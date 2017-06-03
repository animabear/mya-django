# coding=utf-8
import json

from django.shortcuts import render_to_response
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse

def index(request):
    t = get_template('pages/index.html')
    html = t.render(Context({ 'name': 'animabear', 'age': '25' }))

    # todo 资源依赖插入
    with open('templates/map.json') as map_file:
        map_data = json.load(map_file)

    return HttpResponse(html)

