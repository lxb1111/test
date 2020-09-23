#!/usr/bin/env python 
# -*- coding:utf-8 -*-
"""
hugegraph算法接口count_edge：统计边信息，包括图中边数量、各类型的边数量
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
    接口count_edge：统计边信息，包括图中边数量、各类型的边数量
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
        self.expect_result = {"created": 8, "knows": 5, "*": 13}

    # @unittest.skip("skip")
    def test_count_edge_001(self):
        """
        统计边信息接口
        :return:
        """
        print ('统计边信息接口')
        body = {}
        code, ret = self.alg.post_countedge(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(result["created"], self.expect_result["created"], msg="created check not pass")
        self.assertEqual(result["knows"], self.expect_result["knows"], msg="knows check not pass")
        self.assertEqual(result["*"], self.expect_result["*"], msg="* check not pass")
        self.assertEqual(result["created"] + result["knows"], result["*"], msg="*=software+person check not pass")


if __name__ == '__main__':
    # run all cases
    # unittest.main(verbosity=2)

    # run one case
    suite = unittest.TestSuite()
    suite.addTest(TestCountVertex("test_count_edge_001"))
    runner = unittest.TextTestRunner()
    runner.run(suite)
