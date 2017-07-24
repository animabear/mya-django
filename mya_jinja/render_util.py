# coding=utf-8
import json
import os
import jinja2

import settings
from .resource import MYAResource

class SilentUndefined(jinja2.Undefined):
    '''
    变量不存在时不抛出异常，同 django 默认行为
    '''
    def _fail_with_undefined_error(self, *args, **kwargs):
        return None

# jinja2 extension
from .extension.widget import WidgetExtension
from .extension.script import ScriptExtension
from .extension.style  import StyleExtension
from .extension.html   import HtmlExtension, HtmlClostExtension
from .extension.filter import jsonify

from .i18n import _gettext

j2_env = jinja2.Environment(loader=jinja2.FileSystemLoader(settings.TEMPLATE_DIRS),
                        undefined=SilentUndefined,
                        extensions=['jinja2.ext.with_', WidgetExtension, ScriptExtension, StyleExtension, HtmlExtension, HtmlClostExtension])

jinja2.filters.FILTERS['jsonify'] = jsonify # for comp
j2_env.filters['jsonify'] = jsonify # for global

# i18n
j2_env.globals.update(
    gettext=_gettext
)
# end extension

# 模板目录一定要有
TEMPLATE_DIRS = settings.TEMPLATE_DIRS[0]

try:
    MYA_CONF_DIR = settings.MYA_CONF_DIR
except:
    MYA_CONF_DIR = os.path.join(TEMPLATE_DIRS, 'template', 'mya_conf')

"""
@param string template 模版路径，由模板namespace和模板资源id构成，
                       即 namespace:template_path  eg. 'aweme_web:page/home/index.html'
@param dict   context  模版变量
"""
def view(request, template, context={}):
    template_data = template.split(':')
    if len(template_data) == 1:
        namespace = ''
        template_id   = template_data[0]
    else:
        namespace = template_data[0]
        template_id   = template_data[1]

    mya_debug = _get_mya_debug(request)
    mya_resource = MYAResource(MYA_CONF_DIR, mya_debug)

    ctx = {
        '_mya_resource': mya_resource
    }
    ctx.update(context)

    t = j2_env.get_template(mya_resource.get_template_path(template))
    html = t.render(ctx)
    mya_resource.load_page_deps(template) # 最后load入口页面依赖的资源
    html = mya_resource.render_response(html)

    return html

def _get_mya_debug(request):
    mya_debug = False

    # django
    try:
        return request.GET.get('mya_debug') == '1'
    except:
        pass

    # flask
    try:
        return request.args.get('mya_debug') == '1'
    except:
        pass

    return mya_debug