# coding=utf-8

from jinja2.utils import contextfunction
import os
import re
import json
import settings


I18N_DIR = settings.MYA_I18N_DIR


try:
    I18N_MAP = settings.MYA_I18N_MAP
except:
    I18N_MAP = {
        'zh':    ['zh', 'zh-cn'],
        'zh-tw': ['zh-tw', 'zh-hk'],
        'ja':    ['ja', 'ja-jp'],
        'ko':    ['ko', 'ko-kr']
    }


try:
    I18N_DEFAULT_CODE = settings.MYA_I18N_DEFAULT_CODE
except:
    I18N_DEFAULT_CODE = 'en'


i18n_lang_map = {} # 缓存语言map
interpn_ptn = re.compile(r'\{\s*(\S+?)\s*\}') # 插值


def get_lang_code(accept_language=I18N_DEFAULT_CODE):
    # 1. 获取 HTTP_ACCEPT_LANGUAGE: ja,zh-CN;q=0.8,zh;q=0.6,en;q=0.4
    # 2. 取第一组值中的第一个（移动端通常只有一个，pc端可能有多个）
    # 3. 匹配到结果字符串，默认英文
    accept_lang = accept_language.lower();
    langs = accept_lang.split(';')[0]
    lang  = langs.split(',')[0]

    for k, v in I18N_MAP.items():
        if lang in v:
            return k

    return I18N_DEFAULT_CODE


def get_lang_map(lang_code=I18N_DEFAULT_CODE):
    if i18n_lang_map.get(lang_code):
        return i18n_lang_map.get(lang_code)

    map_path = os.path.join(I18N_DIR, lang_code + '.json')
    lang_map = {}

    try:
        with open(map_path) as map_file:
            lang_map = json.load(map_file)
            i18n_lang_map.update({ lang_code: lang_map })
    except:
        pass

    return lang_map


def gettext(lang_code=I18N_DEFAULT_CODE, text="", **kwargs):
    """ 翻译函数，供后端调用
    Usage::
        gettext('zh', u'{year}年{month}月', month='07', year="2017")
    """
    lang_map = get_lang_map(lang_code)
    if not lang_map.get(text):
        return _replaceText(text, {})
    return _replaceText(lang_map.get(text), kwargs)


@contextfunction
def _gettexttpl(context, text):
    """ 根据语言环境，获取待翻译字符串对应的模板，用于前端翻译
    """
    lang_code = context.get('_lang_code', I18N_DEFAULT_CODE)
    lang_map  = get_lang_map(lang_code)
    if not lang_map.get(text):
        return text
    return lang_map.get(text)


@contextfunction
def _gettext(context, text, **kwargs):
    """ 翻译函数，供模板调用

    :param context: 请求上下文
    :param text: 待翻译字符串

    Usage::
        {{ gettext('用户协议') }}
        {{ gettext('%(year)年%(month)月', year=2017, month=7) }}
    """

    lang_code = context.get('_lang_code', I18N_DEFAULT_CODE)
    lang_map  = get_lang_map(lang_code)
    if not lang_map.get(text):
        return _replaceText(text, {})
    return _replaceText(lang_map.get(text), kwargs)


def _replaceText(text, data):
    def repl(matchobj):
        key = matchobj.group(1)
        return str(data.get(key, ''))

    return re.sub(interpn_ptn, repl, text)
