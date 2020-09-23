#!/usr/bin/env python 
# -*- coding:utf-8 -*-
"""
Copyright (c) 2018 Baidu.com, Inc. All Rights Reserved
__title__ = ''
__author__ = 'tianxiaoyuan'
__mtime__ = '20/5/14'

"""
import sys
import os
import time
import json
import unittest
import importlib

sys.path.append('%s/..' % os.path.split(os.path.realpath(__file__))[0])
sys.path.append('../../')
importlib.reload(sys)

from IntegrationTest.graphTest.serverTest.common.hugegraph_api.algorithm_api import AlgInterface


class Task(object):
    """
    provide the result of the task
    """

    def __init__(self):
        self.alg = AlgInterface()

    def get_task(self, id):
        """
        通过id获取详情，并返回详情数据供下一步做校验
        :param id:
        :return:
        """
        code, ret = self.alg.get_graph_tasks(id)
        for i in range(10):
            if code == 200:
                if ret["task_status"] == "failed":
                    return
                elif ret["task_status"] == "success":
                    result = json.loads(ret["task_result"])
                    return result
                else:
                    time.sleep(10)
                    code, ret = self.alg.get_graph_tasks(id)

    def get_task_2(self, id):
        """
        通过id获取详情，并返回详情数据供下一步做校验
        :param id:
        :return:
        """
        code, ret = self.alg.get_graph_tasks(id)
        for i in range(10):
            if code == 200:
                if ret["task_status"] == "failed":
                    return ret["task_status"], ret
                elif ret["task_status"] == "success":
                    result = json.loads(ret["task_result"])
                    return ret["task_status"], result
                else:
                    time.sleep(10)
                    code, ret = self.alg.get_graph_tasks(id)


if __name__ == '__main__':
    Task().get_task(id=7)
