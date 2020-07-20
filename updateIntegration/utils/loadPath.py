# -*- coding:utf-8 -*-
"""
author     : lxb
note       : 获取文件的绝对路径
create_time: 2020/4/22 3:14 下午
"""
import inspect
import os
import time


class ProjectPath:
    """
    初始化所用的文件的绝对路径
    """
    def __init__(self):
        # 获取当前文件路径
        current_path = inspect.getfile(inspect.currentframe())
        # 获取当前文件所在目录，相当于当前文件的父目录
        dir_name = os.path.dirname(current_path)
        # 转换为绝对路径
        file_abs_path = os.path.abspath(dir_name)
        # 划分目录，比如a/b/c划分后变为a/b和c
        list_path = os.path.split(file_abs_path)
        # 获取项目根目录
        project_root_path = list_path[0]
        self.root = project_root_path

    def log_file(self):
        """
        获取日志打印目录
        :return:
        """
        time_str = time.strftime("%m%d_%h%m", time.localtime())
        path = self.root + '/log'
        if os.path.exists(path):
            pass
        else:
            os.mkdir(path)
        return path + '/integrationTest_%s.log' % time_str

    def deploy_graph(self):
        """
        获取 server 部署的目录
        :return:
        """
        path = self.root + '/testEnv'
        if os.path.exists(path):
            pass
        else:
            os.mkdir(path)
        return path

    def git_graph(self):
        """
        获取 git clone 的目录
        :return:
        """
        path = self.root + '/testEnv/git'
        if os.path.exists(path):
            pass
        else:
            os.mkdir(path)
        return path

    def graph_properties(self):
        """
        获取 server 配置的路径
        :return:
        """
        path = self.root + '/config'
        if os.path.exists(path):
            pass
        else:
            os.mkdir(path)
        return path


if __name__ == '__main__':
    test = ProjectPath()
    print('项目根目录：' + test.root)
    print('日志打印目录：' + test.log_file())
    for e in ['hugegraph-0.11.0.tar.gz', 'hugegraph-0.11.0', 'hugegraph-hbase']:
        if 'hugegraph-0.' in e and '.tar.gz' not in e:
            print(e)


