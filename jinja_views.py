# coding=utf-8
import json

from django.http import HttpResponse
from django.conf import settings
from resource import MYAResource
import jinja2

# extension
from jinja.extension.widget import WidgetExtension
from jinja.extension.script import ScriptExtension
from jinja.extension.style  import StyleExtension

env = jinja2.Environment(loader=jinja2.FileSystemLoader(settings.TEMPLATE_DIRS),
                        extensions=[WidgetExtension, ScriptExtension, StyleExtension])

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
            'username': 'xjj',
            'age':  25
        },
        '_mya_resource': mya_resource
    }

    t = env.get_template('pages/jinja2.html')
    html = t.render(ctx)
    html = mya_resource.render_response(html)

    return HttpResponse(html)
