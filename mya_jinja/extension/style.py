# coding=utf-8

from jinja2 import lexer, nodes, Template
from jinja2.ext import Extension

"""
{% style %}
    .widget { color: red }
{% endstyle %}

自定义style标签，收集style，用于最后插入
"""

class StyleExtension(Extension):
    # a set of names that trigger the extension.
    tags = set(['style'])

    def __init__(self, environment):
        super(StyleExtension, self).__init__(environment)

    def parse(self, parser):
        lineno  = parser.stream.expect('name:style').lineno # {% style
        cur_ctx = nodes.ContextReference() # 当前上下文
        body    = []
        style   = ''
        end     = False # flag 标记是否即将结束渲染
        args    = []

        next(parser.stream) # %}

        while parser.stream:
            token = parser.stream.current
            if end:
                parser.stream.expect('name:endstyle')
                break
            if parser.stream.look().value == 'endstyle':
                end = True
                next(parser.stream)
                continue
            body.append(str(token.value))
            next(parser.stream)

        style = ' '.join(body)

        args.append(cur_ctx)
        args.append(nodes.Const(style)) # 要用 nodes.Const 处理，否则会报错

        call = self.call_method(
            '_style',
            args,
            lineno=lineno
        )

        return nodes.Output([call], lineno=lineno)

    def _style(self, cur_ctx, style):
        mya_resource = cur_ctx.get('_mya_resource')
        t = Template(style)
        mya_resource.add_style_pool(t.render(cur_ctx)) # 收集style
        return Template('').render()
