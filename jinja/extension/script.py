# coding=utf-8

from jinja2 import lexer, nodes, Template
from jinja2.ext import Extension

"""
{% script %}
<script>
    require('widget/xxx').init({{ data }})
</script>
{% endscript %}

自定义script标签，收集script，用于最后插入
"""

class ScriptExtension(Extension):
    # a set of names that trigger the extension.
    tags = set(['script'])

    def __init__(self, environment):
        super(ScriptExtension, self).__init__(environment)

    def parse(self, parser):
        lineno  = parser.stream.expect('name:script').lineno # {% script
        cur_ctx = nodes.ContextReference() # 当前上下文
        body    = []
        script  = ''
        end     = False # flag 标记是否即将结束渲染
        args    = []

        next(parser.stream) # %}

        while parser.stream:
            token = parser.stream.current
            if end:
                parser.stream.expect('name:endscript')
                break
            if parser.stream.look().value == 'endscript':
                end = True
                next(parser.stream)
                continue
            body.append(token.value)
            next(parser.stream)

        script = ' '.join(body)

        args.append(cur_ctx)
        args.append(nodes.Const(script)) # 要用 nodes.Const 处理，否则会报错

        call = self.call_method(
            '_script',
            args,
            lineno=lineno
        )

        return nodes.Output([call], lineno=lineno)

    def _script(self, cur_ctx, script):
        mya_resource = cur_ctx.get('_mya_resource')
        t = Template(script)
        mya_resource.add_script_pool(t.render(cur_ctx)) # 收集script
        return Template('').render()
