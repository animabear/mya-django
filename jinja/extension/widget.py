from jinja2 import lexer, nodes, Template
from jinja2.ext import Extension


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

    def parse(self, parser):
        ctx_ref = nodes.ContextReference()
        lineno = parser.stream.expect('name:widget').lineno
        call = self.call_method(
            '_widget',
            [ctx_ref],
            lineno=lineno
        )
        return nodes.Output([call])

    def _widget(self, ctx):
        html = self.environment.get_template('widget/common.html')
        return html.render({'custom_param': ctx.get('name')})
