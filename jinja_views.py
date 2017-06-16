# coding=utf-8
from jinja.render_util import get_html_response

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
    return get_html_response(request, 'pages/jinja2.html', ctx)


def home(request):
    ctx = {
        'name': '<script>animabear</script>',
        'age': '25',
        'user': {
            'username': u'<script>熊猫大侠</script>',
            'age':  25
        }
    }
    return get_html_response(request, 'template@page/home/index.html', ctx)
