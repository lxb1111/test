# # -*- coding:utf-8 -*-
# """
# author     : lxb
# note       : 整体测试
# create_time: 2020/4/21 7:29 下午
# """
# import subprocess
# import sys
# import time
# from utils import setLog
# from utils import getIni
# from utils import loadPath
# from utils import setFile
#
# project_path = loadPath.ProjectPath()
# logger = setLog.basic_log(project_path.log_file())
# con = getIni.config_ini(project_path.test_ini())
#
#
# class TestClass:
#     """
#     不想访问类变量和实例变量，可以用静态方法
#     只想访问类内变量，不想访问实例变量用类方法
#     即想访问类变量，也想访问实例变量用实例方法
#     函数与静态方法相同，只是静态方法的作用域定义在类内
#     """
#     # __slots__ = ["name", "age", "score"]
#
#     # 类的 __slots__ 列表属性
#     # 作用：
#     #   限定一个类创建的实例只能有固定的实例属性
#     #   不允许对象添加列表以外的实例属性(变量)
#     #   防止用户因错写属性的名称而发生程序错误!
#
#     def __init__(self, a, b):
#         self.name = a
#         self.age = b
#
#     def __del__(self):
#         """
#         析构方法在对象被销毁时被自动调用，建议不要在对象销毁时做任何事情，因为销毁的时间难以确定
#         :return:
#         """
#         pass
#
#     @staticmethod
#     def test1(c, d):
#         """
#         静态方法
#         :param c:
#         :param d:
#         :return:
#         """
#         return c + d
#
#     @classmethod
#     def test2(cls, e):
#         """
#         类方法
#         :param d:
#         :return:
#         """
#         cls.name = e
#         print(cls.name, "欢迎到来")
#
#     def test3(self, f, g):
#         """
#         :param f:
#         :param g:
#         :return:
#         """
#         pass
#
#
# def get_founction(a, b, c):
#     """
#     函数
#     :param a:
#     :param b:
#     :param c:
#     :return:
#     """
#
#
# if __name__ == "__main__":
#     config_path = project_path.graph_properties()
#     logger.info(config_path)
#     ### loader、server、tools、hubble
#     param_1 = sys.argv[1]
#     if 'server' == param_1:
#         pass
#     elif 'loader' == param_1:
#         sh_name = con.get('loader', 'loader_sh')
#         loader_config_path = config_path+'loader/'
#         f_lines = setFile.FileClass(loader_config_path + sh_name, 'r').get_readlines()
#         for line in f_lines:
#             if line.startswith('#') or line.startswith('\n'):
#                 ### 执行导入命令
#                 cmd = line % (project_path.deploy_graph()+'graph_server/', loader_config_path, loader_config_path)
#                 subprocess.call(cmd, shell=True)
#                 ### 清除数据库数据
#                 pass
#             else:
#                 pass
#     elif 'tools' == param_1:
#         pass
#     elif 'hubble' == param_1:
#         pass
#     else:
#         logger.error('the  param is error --- [server、loader、tools、hubble]')