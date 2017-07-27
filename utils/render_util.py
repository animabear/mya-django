# coding=utf-8
from django.http import HttpResponse
from mya_jinja import view, i18n


def mya_jinja_render(request, template, context=None, a=None, b=None):
    lang_code = i18n.get_lang_code(request.META.get('HTTP_ACCEPT_LANGUAGE')) # get _lang_code
    context = context or {}

    context['GA_ID'] = 'UA-75850242-4'
    context['_lang_code'] = lang_code # inject _lang_code
    context['_lang_map']  = i18n.get_lang_map(lang_code)

    return HttpResponse( view(request, template, context) )