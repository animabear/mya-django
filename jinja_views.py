# coding=utf-8
from mya_jinja import view, i18n
from django.http import HttpResponse

# pages

def home(request):
    lang_code = i18n.get_lang_code(request.META.get('HTTP_ACCEPT_LANGUAGE'))
    lang_map  = i18n.get_lang_map(lang_code)

    text = i18n.gettext(lang_code, u'{year}年{month}月', month='07', year="2017")

    print text

    ctx = {
        'name': '<script>animabear</script>',
        'age': '25',
        'user': {
            'username': u'<script>熊猫大侠</script>',
            'age':  25
        },
        'list': [{'name': '1'}, {'name': '2'}],
        '_lang_code': lang_code,
        '_lang_map':  lang_map
    }

    # gettext

    return HttpResponse(view(request, 'web_i18n:page/home/index.html', ctx))
