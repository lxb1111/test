#!/usr/bin/env python 
# -*- coding:utf-8 -*-
"""
Copyright (c) 2018 Baidu.com, Inc. All Rights Reserved
__title__ = ''
__author__ = 'tianxiaoyuan'
__mtime__ = '20/5/18'

"""

import sys
import os
import unittest
import importlib
from filecmp import cmp

sys.path.append('%s/..' % os.path.split(os.path.realpath(__file__))[0])
sys.path.append('../../')
importlib.reload(sys)
sys.setdefaultencoding('utf-8')

from IntegrationTest.graphTest.serverTest.common.hugegraph_api.algorithm_api import AlgInterface
from IntegrationTest.graphTest.serverTest.testCase.algorithm.task_status import Task
from IntegrationTest.graphTest.serverTest.common.config.produce_data import ProduceData

TYPE = "basic"


class TestTriangleCount(unittest.TestCase):
    """
    接口triangle_count：三角形计数
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
        cls.expect_result_03 = {"edges_in": 13, "vertices_in": 9, "triangles": 2}
        cls.expect_result_04 = {"edges_out": 13, "vertices_out": 7, "triangles": 2}
        cls.expect_result_05 = {"edges_in": 13, "vertices_in": 9, "triangles": 2}
        cls.expect_result_06 = {"edges_out": 13, "vertices_out": 7, "triangles": 2}
        cls.expect_result_07 = {"edges_out": 13, "vertices_out": 7, "triangles": 0}
        cls.expect_result_08 = {"edges_in": 13, "vertices_in": 9, "triangles": 0}

    @classmethod
    def tearDownClass(cls):
        """
        init graph
        """
        pass

    def test_triangle_count_01(self):
        """
        param = []
        :return:
        """
        body = {}
        code, ret = self.alg.post_triangle_count(body)
        self.assertNotEqual(code, 201)

    def test_triangle_count_02(self):
        """
        param = [direction]
        :return:
        """
        body = {"direction": "BOTH"}
        code, ret = self.alg.post_triangle_count(body)
        self.assertNotEqual(code, 201)

    def test_triangle_count_03(self):
        """
        param = [direction]
        :return:
        """
        body = {"direction": "IN"}
        code, ret = self.alg.post_triangle_count(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(cmp(result, self.expect_result_03), 0, "result check not pass")

    def test_triangle_count_04(self):
        """
        param = [direction, degree]
        :return:
        """
        body = {"direction": "OUT"}
        code, ret = self.alg.post_triangle_count(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(cmp(result, self.expect_result_04), 0, "result check not pass")

    # @unittest.skip("skip")
    def test_triangle_count_05(self):
        """
        param = [direction, degree]
        :return:
        """
        body = {"direction": "IN", "degree": -1}
        code, ret = self.alg.post_triangle_count(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(cmp(result, self.expect_result_05), 0, "result check not pass")

    # @unittest.skip("skip")
    def test_triangle_count_06(self):
        """
        param = [direction, degree]
        :return:
        """
        body = {"direction": "OUT", "degree": -1}
        code, ret = self.alg.post_triangle_count(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(cmp(result, self.expect_result_06), 0, "result check not pass")

    # @unittest.skip("skip")
    def test_triangle_count_07(self):
        """
        param = [direction, degree]
        :return:
        """
        body = {"direction": "OUT", "degree": 1}
        code, ret = self.alg.post_triangle_count(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(cmp(result, self.expect_result_07), 0, "result check not pass")

    def test_triangle_count_08(self):
        """
        param = [direction, degree]
        :return:
        """
        body = {"direction": "IN", "degree": 1}
        code, ret = self.alg.post_triangle_count(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(cmp(result, self.expect_result_08), 0, "result check not pass")


if __name__ == '__main__':
    # run all cases
    unittest.main(verbosity=2)

    # run one case
    # suite = unittest.TestSuite()
    # suite.addTest(TestTriangleCount("test_triangle_count_01"))
    # runner = unittest.TextTestRunner()
    # runner.run(suite)
