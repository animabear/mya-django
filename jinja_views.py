# coding=utf-8
from django.conf import settings
from jinja.render_util import get_html_response

# jinja2 extension
import jinja2
from jinja.extension.widget import WidgetExtension
from jinja.extension.script import ScriptExtension
from jinja.extension.style  import StyleExtension
from jinja.extension.filter import jsonify

env = jinja2.Environment(loader=jinja2.FileSystemLoader(settings.TEMPLATE_DIRS),
                        extensions=[WidgetExtension, ScriptExtension, StyleExtension])

jinja2.filters.FILTERS['jsonify'] = jsonify
# end

# pages
def jinja2(request):
    ctx = {
        'name': '<script>animabear</script>',
        'age': '25',
        'user': {
            'username': u'<script>熊猫大侠</script>',
            'age':  25
        }
    }
    return get_html_response(request, 'pages/jinja2.html', ctx, env)


def home(request):
    ctx = {
        'name': '<script>animabear</script>',
        'age': '25',
        'user': {
            'username': u'<script>熊猫大侠</script>',
            'age':  25
        }
    }
    return get_html_response(request, 'template@page/home/index.html', ctx, env)
