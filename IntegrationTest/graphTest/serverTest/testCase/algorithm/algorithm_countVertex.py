#!/usr/bin/env python 
# -*- coding:utf-8 -*-
"""
hugegraph算法接口count_vertex：统计顶点信息，包括图中顶点数量、各类型的顶点数量
wiki：
Copyright (c) 2018 Baidu.com, Inc. All Rights Reserved
__title__ = ''
__author__ = 'tianxiaoyuan'
__mtime__ = '20/05/13'

"""
import sys
import os
import unittest
import importlib

sys.path.append('%s/..' % os.path.split(os.path.realpath(__file__))[0])
sys.path.append('../../')
importlib.reload(sys)

from IntegrationTest.graphTest.serverTest.common.hugegraph_api.algorithm_api import AlgInterface
from IntegrationTest.graphTest.serverTest.testCase.algorithm.task_status import Task
from IntegrationTest.graphTest.serverTest.common.config.produce_data import ProduceData


TYPE = "basic"


class TestCountVertex(unittest.TestCase):
    """
    接口count_vertex：统计顶点信息，包括图中顶点数量、各类型的顶点数量
    """

    @classmethod
    def setUp(self):
        self.alg = AlgInterface()
        self.task = Task()
        self.p = ProduceData()

        # 初始化图
        self.clear_data = self.p.init_data("clear")
        self.init_data = self.p.init_data(TYPE)

        # 预期结果
        self.expect_result = {"software": 5, "person": 11, "*": 16}

    # @unittest.skip("skip")
    def test_count_vertex_001(self):
        """
        统计顶点信息接口
        :return:
        """
        body = {}
        code, ret = self.alg.post_countertex(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(result["software"], 5, msg="software check not pass")
        self.assertEqual(result["person"], 11, msg="person check not pass")
        self.assertEqual(result["*"], 16, msg="* check not pass")
        self.assertEqual(result["software"] + result["person"], result["*"], msg="*=software+person check not pass")


if __name__ == '__main__':
    # run all cases
    # unittest.main(verbosity=2)

    # run one case
    suite = unittest.TestSuite()
    suite.addTest(TestCountVertex("test_count_vertex_001"))
    runner = unittest.TextTestRunner()
    runner.run(suite)
