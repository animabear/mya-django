# coding=utf-8

from jinja2 import lexer, nodes, Template
from jinja2.ext import Extension

"""
{% widget name="widget/header.html" mode="bigrender" kwarg1=arg1 kwarg2="string arg2" %}

自定义组件标签，渲染组件模版，收集依赖；支持嵌套，对于嵌套情况，解析顺序自顶向下
"""

# widget标签的默认参数
default_kwargs = ['name', 'mode']

class WidgetExtension(Extension):
    # a set of names that trigger the extension.
    tags = set(['widget'])

    def __init__(self, environment):
        super(WidgetExtension, self).__init__(environment)

        # add the defaults to the environment
        # environment.extend(
        #     fragment_cache_prefix='',
        #     fragment_cache=None
        # )

    @staticmethod
    def parse_expression(parser):
        token = parser.stream.current
        if token.test(lexer.TOKEN_STRING):
            expr = nodes.Const(token.value, lineno=token.lineno)
            next(parser.stream)
        else:
            expr = parser.parse_expression(False)

        return expr

    def parse(self, parser):
        lineno  = next(parser.stream).lineno # parser.stream 是一个迭代器对象
        kwargs = None
        cur_ctx = nodes.ContextReference() # 当前上下文

        while parser.stream.current.type != lexer.TOKEN_BLOCK_END:
            token = parser.stream.current
            if kwargs is not None:
                if token.type != lexer.TOKEN_NAME:
                    parser.fail(
                        "got '{}', expected name for keyword argument"
                        "".format(lexer.describe_token(token)),
                        lineno=token.lineno
                    )
                arg = token.value
                next(parser.stream)
                parser.stream.expect(lexer.TOKEN_ASSIGN) # 匹配到 '='，同时执行 next()
                kwargs[arg] = self.parse_expression(parser)
            else:
                if parser.stream.look().type == lexer.TOKEN_ASSIGN:
                    kwargs = {}
                continue

        if kwargs is not None:
            kwargs = [nodes.Keyword(key, val) for key, val in kwargs.items()]

        call = self.call_method(
            '_widget',
            [cur_ctx],
            kwargs,
            lineno=lineno
        )

        return nodes.Output([call], lineno=lineno)

    def _widget(self, *args, **kwargs):
        cur_ctx = args[0]
        params = {}
        ctx_params = {}

        for key, val in kwargs.items():
            if key in default_kwargs:
                params[key] = val
            else:
                ctx_params[key] = val

        name = params.get('name') # template name
        mode = params.get('mode') # render mode

        # 向下层 widget 传递 mya_resource
        ctx_params['_mya_resource'] = mya_resource = cur_ctx.get('_mya_resource')
        # 分析并收集依赖
        mya_resource.load_deps(name)
        # 渲染模版
        t = self.environment.get_template(mya_resource.get_template_path(name))
        html = t.render(ctx_params)

        return html
