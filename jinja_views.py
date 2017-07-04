# coding=utf-8
from mya_jinja.render_util import view
from django.http import HttpResponse

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
    return HttpResponse(view(request, 'pages/jinja2.html', ctx))


def home(request):
    ctx = {
        'name': '<script>animabear</script>',
        'age': '25',
        'user': {
            'username': u'<script>熊猫大侠</script>',
            'age':  25
        },
        'list': [{'name': '1'}, {'name': '2'}]
    }
    return HttpResponse(view(request, 'web_i18n:page/home/index.html', ctx))
