# coding=utf-8

class MYAResource(object):
    SCRIPT_PLACEHOLDER = '<!--SCRIPT_PLACEHOLDER-->'
    STYLE_PLACEHOLDER  = '<!--STYLE_PLACEHOLDER-->'

    def __init__(self, res_map):
        self.res_map = res_map
        self.deps = []


    """
    /**
     * 分析组件依赖
     * @param  string name 组件名字
     * @return dict   组件依赖
     */
    """
    def loadDeps(self, name):
        print self.res_map.get('res').get(name)
        self.deps.append(name)


    """
    /**
     * 获取组件模版路径
     * @param  string name 组件名字
     * @return dict   组件依赖
     */
    """
    def get_template_uri(self, name):
        return self.res_map.get('res', {}).get(name, {}).get('uri', name)


    def get_deps(self):
        return self.deps

