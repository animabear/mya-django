# coding=utf-8

from jinja2 import lexer, nodes, Template
from jinja2.ext import Extension

"""
{% html framework="static/mod.js" %}

自定义html标签，用于加载模块管理框架，并输出 <html>
"""

class HtmlExtension(Extension):
    # a set of names that trigger the extension.
    tags = set(['html'])

    def __init__(self, environment):
        super(HtmlExtension, self).__init__(environment)

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
            '_html',
            [cur_ctx],
            kwargs,
            lineno=lineno
        )

        return nodes.Output([call], lineno=lineno)

    def _html(self, *args, **kwargs):
        cur_ctx = args[0]
        framework = kwargs.get('framework', '')
        mya_resource = cur_ctx.get('_mya_resource')
        # 分析并收集依赖
        if framework:
            mya_resource.load_deps(framework)

        return '<html>'


"""
{% endhtml %}

自定义html标签，用于插入内容到html标签之后，并输出 </html>
"""
class HtmlClostExtension(Extension):
    # a set of names that trigger the extension.
    tags = set(['endhtml'])

    def __init__(self, environment):
        super(HtmlClostExtension, self).__init__(environment)

    def parse(self, parser):
        lineno  = parser.stream.expect('name:endhtml').lineno

        call = self.call_method(
            '_endhtml',
            [],
            lineno=lineno
        )

        return nodes.Output([call], lineno=lineno)

    def _endhtml(self):
        # mya_resource = cur_ctx.get('_mya_resource')
        # tips: 后续可以插入一些内容到 html 之后
        return '</html>'
