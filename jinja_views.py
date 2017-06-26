# coding=utf-8
from jinja.render_util import view

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
    return view(request, 'pages/jinja2.html', ctx)


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
    return view(request, 'template@page/home/index.html', ctx)
