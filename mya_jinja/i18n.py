# coding=utf-8

from jinja2.utils import contextfunction
import os
import re
import json
import settings
from .utils import isNum, dict_merge

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


i18n_lang_map = {}
interpn_ptn = re.compile(r'\{\s*(\S+?)\s*\}') # 插值


def get_lang_code(accept_language=None):
    # 1. 获取 HTTP_ACCEPT_LANGUAGE: ja,zh-CN;q=0.8,zh;q=0.6,en;q=0.4
    # 2. 取第一组值中的第一个（移动端通常只有一个，pc端可能有多个）
    # 3. 匹配到结果字符串，默认英文
    if accept_language is None:
        accept_language = I18N_DEFAULT_CODE

    accept_lang = accept_language.lower();
    langs = accept_lang.split(';')[0]
    lang  = langs.split(',')[0]

    for k, v in I18N_MAP.items():
        if lang in v:
            return k

    return I18N_DEFAULT_CODE


def get_lang_map(lang_code=None):
    if lang_code is None:
        lang_code = I18N_DEFAULT_CODE

    if i18n_lang_map.get(lang_code):
        return i18n_lang_map.get(lang_code)

    # map_path = os.path.join(I18N_DIR, lang_code + '.json')
    # lang_map = {}
    #
    # try:
    #     with open(map_path) as map_file:
    #         lang_map = json.load(map_file)
    #         i18n_lang_map.update({ lang_code: lang_map })
    # except:
    #     pass

    if not i18n_lang_map:
        dict_merge(i18n_lang_map, _load_lang_map())

    return i18n_lang_map.get(lang_code, {})


def gettext(lang_code=None, text="", **kwargs):
    """ 翻译函数，供后端调用
    Usage::
        gettext('zh', u'{year}年{month}月', month='07', year="2017")
    """
    if lang_code is None:
        lang_code = I18N_DEFAULT_CODE

    lang_map = get_lang_map(lang_code)
    if not lang_map.get(text):
        return _replaceText(text, kwargs)
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
        {{ gettext('{year}年{month}月', year=2017, month=7) }}
    """

    lang_code = context.get('_lang_code', I18N_DEFAULT_CODE)
    lang_map  = get_lang_map(lang_code)
    if not lang_map.get(text):
        return _replaceText(text, kwargs)
    return _replaceText(lang_map.get(text), kwargs)


def _replaceText(text, data):
    def repl(matchobj):
        key = matchobj.group(1)
        res = data.get(key, '')
        return str(res) if isNum(res) else res

    return re.sub(interpn_ptn, repl, text)


def _load_lang_map():
    """ 读取指定目录下的翻译文件，一次性载入内存
    读取 lang/${namespace}/*.json，生成 lang_map
    {
        "zh": 合并 lang/*/zh.json
    }
    """
    lang_map_res = {}
    dirs = os.listdir(I18N_DIR) # web web_i18n
    namespaces = [os.path.join(I18N_DIR, ns) for ns in dirs]
    for ns in namespaces:
        langs = os.listdir(ns) # en.json ja.json
        for lang in langs:
            lang_code = lang.replace('.json', '')
            map_path  = os.path.join(ns, lang)
            try:
                with open(map_path) as map_file:
                    lang_map = json.load(map_file)
                    lang_map_res = dict_merge(lang_map_res, { lang_code: lang_map })
            except:
                pass

    return lang_map_res