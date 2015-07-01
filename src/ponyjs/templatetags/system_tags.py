import subprocess

from django import template
from django.conf import settings
from django.utils.six.moves.urllib.parse import urljoin

register = template.Library()

JSPM_EXECUTABLE = './node_modules/.bin/jspm'


class System(object):

    def __init__(self, app, outfile, **opts):
        self.app = app
        self.outfile = outfile
        self.opts = opts
        self.stdout = self.stdin = self.stderr = subprocess.PIPE

    def command(self, command):
        proc = subprocess.Popen(
            command, shell=True, cwd=self.cwd, stdout=self.stdout,
            stdin=self.stdin, stderr=self.stderr)
        result, err = proc.communicate()
        return result

    @classmethod
    def bundle(cls, app, outfile, **opts):
        system = cls(app, outfile, **opts)
        cmd = u'{jspm} bundle-sfx {app} {outfile}'
        system.command(cmd)


class SystemImportNode(template.Node):

    def __init__(self, path):
        self.path = path

    def render(self, context):
        """
        Build the filepath by appending the extension.
        """
        module_path = self.path.resolve(context)
        path = u'{path}.{ext}'.format(path=module_path, ext='js')
        if settings.DEBUG:
            tpl = """<script type="text/javascript">System.import('{app}');</script>"""
            return tpl.format(app=module_path)

        # else: create a bundle
        import bpdb; bpdb.set_trace()

    @classmethod
    def handle_token(cls, parser, token):
        bits = token.split_contents()

        if len(bits) < 2:
            raise template.TemplateSyntaxError(
                "'%s' takes at least one argument (js module, without extension)" % bits[0])

        # for 'as varname' support, check django.templatetags.static
        path = parser.compile_filter(bits[1])
        return cls(path)


@register.tag
def system_import(parser, token):
    """
    Import a Javascript module via SystemJS, bundling the app.

    Syntax::

        {% system_import 'path/to/file' %}

    Example::

        {% system_import 'mydjangoapp/js/myapp' %}

    Which would be rendered like::

        <script type="text/javascript" src="/static/CACHE/mydjangoapp.js.min.myapp.js"></script>

    where /static/CACHE can be configured through settings.

    In DEBUG mode, the result would be

        <script type="text/javascript">System.import('mydjangoapp/js/myapp');</script>
    """

    return SystemImportNode.handle_token(parser, token)
