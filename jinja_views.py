# coding=utf-8
from mya_jinja import view
from django.http import HttpResponse

# pages

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
