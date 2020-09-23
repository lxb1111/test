#!/usr/bin/env python 
# -*- coding:utf-8 -*-
"""
Copyright (c) 2018 Baidu.com, Inc. All Rights Reserved
__title__ = ''
__author__ = 'tianxiaoyuan'
__mtime__ = '20/6/29'

"""
import sys
import os
import unittest
from filecmp import cmp
import importlib

sys.path.append('%s/..' % os.path.split(os.path.realpath(__file__))[0])
sys.path.append('../../')
importlib.reload(sys)

from IntegrationTest.graphTest.serverTest.common.hugegraph_api.algorithm_api import AlgInterface
from IntegrationTest.graphTest.serverTest.testCase.algorithm.task_status import Task
from IntegrationTest.graphTest.serverTest.common.config.produce_data import ProduceData

TYPE = "kings2"


class TestRingsDetect2(unittest.TestCase):
    """
    接口rings_detect：环路检测2（新的图）
    """
    @classmethod
    def setUpClass(cls):
        cls.alg = AlgInterface()
        cls.task = Task()
        cls.p = ProduceData()

        # 初始化图
        cls.clear_data = cls.p.init_data("clear")
        cls.init_data = cls.p.init_data(TYPE)

        # 预期结果
        cls.expect_result_limit2 = {
            "rings": [["1:josh", "2:lily", "2:ripple", "1:josh"], ["1:josh", "2:lop", "2:ripple", "1:josh"]]}
        cls.expect_result_limit1 = {"rings": [["1:josh", "2:lily", "2:ripple", "1:josh"]]}
        cls.expect_result_limit3 = {
            "rings": [["1:josh", "2:lily", "2:ripple", "1:josh"], ["1:josh", "2:lop", "2:ripple", "1:josh"]]}

    @classmethod
    def tearDownClass(cls):
        """
        init graph
        """
        pass

    def test_rings_detect2_01(self):
        """
        :return:
        """
        body = {"depth": 5, "limit": 2}
        code, ret = self.alg.post_rings_detect(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(cmp(result, self.expect_result_limit2), 0, msg="result check not pass")

    def test_rings_detect2_02(self):
        """
        :return:
        """
        body = {"depth": 5, "limit": 1}
        code, ret = self.alg.post_rings_detect(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(cmp(result, self.expect_result_limit1), 0, msg="result check not pass")

    def test_rings_detect2_03(self):
        """
        :return:
        """
        body = {"depth": 5, "limit": 3}
        code, ret = self.alg.post_rings_detect(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(cmp(result, self.expect_result_limit3), 0, msg="result check not pass")


if __name__ == '__main__':
    # run all cases
    unittest.main(verbosity=2)

    # run one case
    # suite = unittest.TestSuite()
    # suite.addTest(TestRingsDetect("test_rings_detect_001"))
    # runner = unittest.TextTestRunner()
    # runner.run(suite)

