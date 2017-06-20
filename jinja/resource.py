# coding=utf-8
import re

class MYAResource(object):
    SCRIPT_PLACEHOLDER_PTN = re.compile(r'<!--\s*SCRIPT_PLACEHOLDER\s*-->')
    STYLE_PLACEHOLDER_PTN  = re.compile(r'<!--\s*STYLE_PLACEHOLDER\s*-->')

    """
    /**
     * @param res_map 静态资源映射表
     */
    """
    def __init__(self, res_map):
        self.res_map = res_map
        self.loaded_deps = [] # 已添加的依赖
        self.style_deps  = [] # 样式依赖
        self.script_deps = [] # 脚本依赖
        self.style_pool  = [] # 收集 {% style %}{% endstyle %} 标签包裹的css
        self.script_pool = [] # 收集 {% script %}{% endscript %} 标签包裹的js

    """
    /**
     * 加载页面，获得入口页面依赖的资源文件
     * @param string res_id 页面资源id
     */
    """
    def load_page(self, res_id):
        res = self.res_map.get('res', {})
        res_data = res.get(res_id, {})
        deps     = res_data.get('deps', [])

        for dep in deps:
            self.load_deps(dep)

    """
    /**
     * 分析组件依赖 (深度优先后序遍历)
     * @param string res_id 资源id
     */
    """
    def load_deps(self, res_id):
        res = self.res_map.get('res', {})
        pkg = self.res_map.get('pkg', {})
        res_data  = res.get(res_id, {})
        file_type = res_data.get('type')
        uri       = res_data.get('uri')
        deps      = res_data.get('deps', [])

        if res_id in self.loaded_deps: # 已经加载过的资源直接跳过
            return

        if res_data.get('pkg'):
            pkg_data = pkg.get(res_data.get('pkg'))
            pkg_deps = pkg_data.get('deps', [])
            pkg_has  = pkg_data.get('has', [])
            pkg_uri  = pkg_data.get('uri')
            pkg_type = pkg_data.get('type')

            for item in pkg_has: # 将 pkg 拥有的模块加入到 loaded_deps 中
                if item not in self.loaded_deps:
                    self.loaded_deps.append(item)

            if not len(pkg_deps):
                self.add_deps(pkg_uri, pkg_type)
                return

            for dep in pkg_deps:
                self.load_deps(dep)

            self.add_deps(pkg_uri, pkg_type)

        else:

            if not len(deps):
                self.add_deps(uri, file_type)
                return

            for dep in deps:
                self.load_deps(dep)

            self.add_deps(uri, file_type)

    def add_deps(self, uri, file_type):
        if self.is_script_can_add(uri, file_type):
            self.script_deps.append(uri)
        if self.is_style_can_add(uri, file_type):
            self.style_deps.append(uri)

    def is_script_can_add(self, uri, file_type):
        return uri and self.is_script(file_type) and uri not in self.script_deps

    def is_style_can_add(self, uri, file_type):
        return uri and self.is_style(file_type) and uri not in self.style_deps

    def is_script(self, file_type):
        return file_type == 'js'

    def is_style(self, file_type):
        return file_type == 'css'

    """
    /**
     * 获取组件模版路径
     * @param string name 组件名字
     */
    """
    def get_template_path(self, name):
        return self.res_map.get('res', {}).get(name, {}).get('uri', name)

    """
    /**
     * 输出最终模版，插入css和js
     * 插入规则：默认插入页面中的对应占位符，如果没有占位符，则css插入 </head> 之前，js插入 </body> 之前
     * @param string html 初步render后的html
     */
    """
    def render_response(self, html):
        css_html = '\n'.join([ self.get_style_tag(uri) for uri in self.style_deps ])
        js_html  = '\n'.join([ self.get_script_tag(uri) for uri in self.script_deps ])

        if self.style_pool:
            css_html += self.render_style_pool()

        if self.script_pool:
            js_html += self.render_script_pool()

        # 插入css
        if MYAResource.STYLE_PLACEHOLDER_PTN.search(html):
            html = re.sub(MYAResource.STYLE_PLACEHOLDER_PTN, css_html, html)
        else:
            html = html.replace('</head>', css_html + '</head>')

        # 插入js
        if MYAResource.SCRIPT_PLACEHOLDER_PTN.search(html):
            html = re.sub(MYAResource.SCRIPT_PLACEHOLDER_PTN, js_html, html)
        else:
            html = html.replace('</body>', js_html + '</body>')

        return html

    def get_style_tag(self, uri):
        return '<link rel="stylesheet" href="%s" />' % (uri)

    def get_script_tag(self, uri, crossorigin=False):
        return '<script src="%s"></script>' % (uri)

    def render_style_pool(self):
        return '\n<style>' + '\n'.join(self.style_pool) + '\n</style>\n'

    def render_script_pool(self):
        script = '';
        for item in self.script_pool:
            script += '(function() {' + item + '\n})();\n'
        script = '\n<script type="text/javascript">\n' + script + '</script>\n'
        return script

    def add_style_pool(self, style):
        self.style_pool.append(style)

    def add_script_pool(self, script):
        self.script_pool.append(script)
