# coding=utf-8
from django.http import HttpResponse
from mya_jinja import view, i18n


def mya_jinja_render(request, template, context=None, a=None, b=None):
    locale = i18n.get_locale(request.META.get('HTTP_ACCEPT_LANGUAGE')) # get _locale
    context = context or {}

    context['GA_ID'] = 'UA-75850242-4'
    context['_mya_locale'] = locale # inject _locale
    context['_lang_map']  = i18n.get_lang_map(locale)

    return HttpResponse( view(request, template, context) )