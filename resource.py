# coding=utf-8

class MYAResource(object):
    SCRIPT_PLACEHOLDER = '<!--SCRIPT_PLACEHOLDER-->'
    STYLE_PLACEHOLDER  = '<!--STYLE_PLACEHOLDER-->'

    """
    /**
     * @param res_map 静态资源映射表
     */
    """
    def __init__(self, res_map):
        self.res_map = res_map
        self.style_deps = []  # 样式依赖
        self.script_deps = [] # 脚本依赖


    """
    /**
     * 分析组件依赖 (深度优先后序遍历)
     * @param string name 文件名字
     */
    """
    def load_deps(self, name):
        res = self.res_map.get('res', {})
        file_data = res.get(name, {})
        file_type = file_data.get('type')
        uri       = file_data.get('uri')
        deps      = file_data.get('deps', [])

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
     * @param  string name 组件名字
     */
    """
    def get_template_path(self, name):
        return self.res_map.get('res', {}).get(name, {}).get('uri', name)


    """
    /**
     * 获取依赖
     * todo: del
     */
    """
    def get_deps(self):
        deps = {
            'css': self.style_deps,
            'js':  self.script_deps
        }
        return deps


    """
    /**
     * 输出最终模版，插入css和js
     */
    """
    def render_response(self, html):
        return html
