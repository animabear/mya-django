from jinja2 import nodes
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
        lineno = parser.stream.expect('name:widget').lineno
        call = self.call_method(
            '_widget',
            [nodes.Name('widget', 'load', lineno=lineno)],
            lineno=lineno
        )
        return nodes.Output([nodes.MarkSafe(call)])

    def _widget(self, name):
        return '<div>wdiget</div>'