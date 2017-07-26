# coding=utf-8
from utils.render_util import mya_jinja_render as view

def home(request):
    ctx = {
        'name': '<script>animabear</script>',
        'age': '25',
        'user': {
            'username': u'<script>熊猫大侠</script>',
            'name': '熊猫大侠',
            'age':  25
        },
        'list': [{'name': '1'}, {'name': '2'}]
    }

    return view(request, 'web_i18n:page/home/index.html', ctx)
