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
import unittest
import importlib
from filecmp import cmp

sys.path.append('%s/..' % os.path.split(os.path.realpath(__file__))[0])
sys.path.append('../../')
importlib.reload(sys)

from IntegrationTest.graphTest.serverTest.common.hugegraph_api.algorithm_api import AlgInterface
from IntegrationTest.graphTest.serverTest.testCase.algorithm.task_status import Task
from IntegrationTest.graphTest.serverTest.common.config.produce_data import ProduceData

TYPE = "betweeness"


class TestBetweenessCentrality(unittest.TestCase):
    """
    betweeness_centrality：中介中心性
    case1\2\3 结果会变需要调试
    """

    @classmethod
    def setUpClass(cls):
        cls.alg = AlgInterface()
        cls.task = Task()
        cls.p = ProduceData()

        # 初始化数据
        cls.clear_data = cls.p.init_data("clear")
        cls.init_data = cls.p.init_data(TYPE)

        # 预期结果
        cls.expect_result_01 = {"2:ripple": 4, "1:vadas": 4, "1:peter": 4, "1:marko": 2, "1:josh": 2, "2:lop": 2}
        cls.expect_result_02 = {"1:vadas": 9, "1:peter": 9, "2:lop": 8, "2:ripple": 7, "1:josh": 6,
                                          "1:marko": 3}
        cls.expect_result_022 = {"1:marko": 4, "1:vadas": 4, "2:ripple": 3, "1:peter": 3, "1:josh": 1,
                                           "2:lop": 1}
        cls.expect_result_04 = {"1:vadas": 28, "1:peter": 28, "2:ripple": 20, "2:lop": 20, "1:marko": 14,
                                    "1:josh": 14}
        cls.expect_result_042 = {"1:vadas": 21, "1:peter": 21, "2:lop": 20, "2:ripple": 14, "1:marko": 9,
                                     "1:josh": 8}
        cls.expect_result_06 = {"1:vadas": 6, "2:ripple": 4, "2:lop": 4}
        cls.expect_result_07 = {"1:marko": 2, "1:josh": 2, "1:vadas": 2, "1:peter": 2}
        cls.expect_result_08 = {"1:vadas": 28, "1:peter": 28, "2:ripple": 20, "2:lop": 20, "1:marko": 14,
                                           "1:josh": 14}
        cls.expect_result_09 = {"1:vadas": 13, "1:peter": 13, "2:ripple": 8, "2:lop": 8, "1:marko": 7,
                                          "1:josh": 7}
        cls.expect_result_10 = {"1:vadas": 13, "1:peter": 13, "2:ripple": 8, "2:lop": 8, "1:marko": 7,
                                         "1:josh": 7}
        cls.expect_result_11 = {"1:vadas": 28, "1:peter": 28, "2:ripple": 20, "2:lop": 20, "1:marko": 14,
                                       "1:josh": 14}
        cls.expect_result_12 = {"1:vadas": 28, "1:peter": 28, "2:ripple": 20, "2:lop": 20, "1:marko": 14}
        cls.expect_result_13 = {"1:vadas": 28, "1:peter": 28, "2:ripple": 20, "2:lop": 20, "1:marko": 14, "1:josh": 14}
        cls.expect_result_14 = {"1:vadas": 6, "2:ripple": 4, "2:lop": 4}
        cls.expect_result_15 = {"1:vadas": 28, "1:peter": 28, "2:ripple": 20, "2:lop": 20, "1:marko": 14,
                                   "1:josh": 14}
        cls.expect_result_16 = {"1:vadas": 13, "1:peter": 13, "2:ripple": 8, "2:lop": 8, "1:marko": 7, "1:josh": 7}
        cls.expect_result_17 = {"1:vadas": 13, "1:peter": 13, "2:ripple": 8, "2:lop": 8, "1:marko": 7, "1:josh": 7}
        cls.expect_result_18 = {"1:vadas": 6, "2:ripple": 4, "2:lop": 4}
        cls.expect_result_19 = {"1:vadas": 6, "2:ripple": 4, "2:lop": 4}

    @classmethod
    def tearDownClass(cls):
        """
        init graph
        """
        pass

    def test_betweeness_centrality_01(self):  # 结果会变
        """
        params = [depth]
        :return:
        """
        body = {"depth": 5}
        code, ret = self.alg.post_betweeness_centrality(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        # self.assertEqual(cmp(result, self.expect_result_01), 0, "result check not pass")

    def test_betweeness_centrality_02(self):  # 结果会变
        """
        params = [depth、source_sample]
        :return:
        """
        body = {"depth": 5, "source_sample": -1}
        code, ret = self.alg.post_betweeness_centrality(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        # self.assertEqual(cmp(result, self.expect_result_02), 0, "result check not pass")

    def test_betweeness_centrality_03(self):  # 结果会变
        """
        params = [depth、source_sample]
        :return:
        """
        body = {"depth": 5, "source_sample": 2}
        code, ret = self.alg.post_betweeness_centrality(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        # self.assertEqual(cmp(result, self.expect_result_022), 0, "result check not pass")

    def test_betweeness_centrality_04(self):
        """
        params = [depth、sample]
        :return:
        """
        body = {"depth": 5, "sample": -1}
        code, ret = self.alg.post_betweeness_centrality(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(cmp(result, self.expect_result_04), 0, "result check not pass")

    def test_betweeness_centrality_05(self):  # 结果会变
        """
        params = [depth、sample]
        :return:
        """
        body = {"depth": 5, "sample": 2}
        code, ret = self.alg.post_betweeness_centrality(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        # self.assertEqual(cmp(result, self.expect_result_042), 0, "result check not pass")

    def test_betweeness_centrality_06(self):
        """
        params = [depth、sample、label]
        :return:
        """
        body = {"depth": 5, "sample": -1, "label": "created"}
        code, ret = self.alg.post_betweeness_centrality(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(cmp(result, self.expect_result_06), 0, "result check not pass")

    def test_betweeness_centrality_07(self):
        """
        params = [depth、sample、label]
        :return:
        """
        body = {"depth": 5, "sample": -1, "label": "knows"}
        code, ret = self.alg.post_betweeness_centrality(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(cmp(result, self.expect_result_07), 0, "result check not pass")

    def test_betweeness_centrality_08(self):
        """
        params = [depth、sample、direction]
        :return:
        """
        body = {"depth": 5, "sample":-1, "direction": "BOTH"}
        code, ret = self.alg.post_betweeness_centrality(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(cmp(result, self.expect_result_08), 0, "result check not pass")

    def test_betweeness_centrality_09(self):
        """
        params = [depth、sample、direction]
        :return:
        """
        body = {"depth": 5, "sample":-1, "direction": "OUT"}
        code, ret = self.alg.post_betweeness_centrality(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(cmp(result, self.expect_result_09), 0, "result check not pass")

    def test_betweeness_centrality_10(self):
        """
        params = [depth、sample、direction]
        :return:
        """
        body = {"depth": 5, "sample":-1, "direction": "IN"}
        code, ret = self.alg.post_betweeness_centrality(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(cmp(result, self.expect_result_10), 0, "result check not pass")

    def test_betweeness_centrality_11(self):
        """
        params = [depth、sample、degree]
        :return:
        """
        body = {"depth": 5, "sample": -1, "degree": 5}
        code, ret = self.alg.post_betweeness_centrality(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(cmp(result, self.expect_result_11), 0, "result check not pass")

    def test_betweeness_centrality_12(self):
        """
        params = [depth、sample、top]
        :return:
        """
        body = {"depth": 5, "sample": -1, "top": 5}
        code, ret = self.alg.post_betweeness_centrality(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(cmp(result, self.expect_result_12), 0, "result check not pass")

    def test_betweeness_centrality_13(self):
        """
        params = [depth、sample、top、source_sample、degree]
        :return:
        """
        body = {"depth": 5, "degree": 50, "sample": -1, "top": 10, "source_sample": -1}
        code, ret = self.alg.post_betweeness_centrality(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(cmp(result, self.expect_result_13), 0, "result check not pass")

    # @unittest.skip("skip")
    def test_betweeness_centrality_14(self):
        """
        params = [depth、sample、top、source_sample、degree、label]
        :return:
        """
        body = {"depth": 5, "degree": 50, "sample": -1, "top": 10, "source_sample": -1, "label": "created"}
        code, ret = self.alg.post_betweeness_centrality(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(cmp(result, self.expect_result_14), 0, "result check not pass")

    # @unittest.skip("skip")
    def test_betweeness_centrality_15(self):
        """
        params = [depth、sample、top、source_sample、degree、direction]
        :return:
        """
        body = {"depth": 5, "degree": 50, "sample": -1, "top": 10, "source_sample": -1, "direction": "BOTH"}
        code, ret = self.alg.post_betweeness_centrality(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(cmp(result, self.expect_result_15), 0, "result check not pass")

    def test_betweeness_centrality_16(self):
        """
        params = [depth、sample、top、source_sample、degree、direction]
        :return:
        """
        body = {"depth": 5, "degree": 50, "sample": -1, "top": 10, "source_sample": -1, "direction": "IN"}
        code, ret = self.alg.post_betweeness_centrality(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(cmp(result, self.expect_result_16), 0, "result check not pass")

    def test_betweeness_centrality_17(self):
        """
        params = [depth、sample、top、source_sample、degree、direction]
        :return:
        """
        body = {"depth": 5, "degree": 50, "sample": -1, "top": 10, "source_sample": -1, "direction": "OUT"}
        code, ret = self.alg.post_betweeness_centrality(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(cmp(result, self.expect_result_17), 0, "result check not pass")

    def test_betweeness_centrality_18(self):
        """
        params = [depth、sample、top、source_sample、degree、direction、label]
        :return:
        """
        body = {"depth": 5, "degree": 50, "sample": -1, "top": 10, "source_sample": -1,
                "direction": "BOTH", "label": "created"}
        code, ret = self.alg.post_betweeness_centrality(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(cmp(result, self.expect_result_18), 0, "result check not pass")

    # @unittest.skip("skip")
    def test_betweeness_centrality_19(self):
        """
        params = [depth、sample、top、source_sample、degree、direction、label]
        :return:
        """
        body = {"depth": 5, "degree": 50, "sample": -1, "top": 10, "source_sample": 10,
                "direction": "BOTH", "label": "created"}
        code, ret = self.alg.post_betweeness_centrality(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(cmp(result, self.expect_result_19), 0, "result check not pass")


if __name__ == '__main__':
    # run all cases
    # unittest.main(verbosity=2)

    # run one case
    suite = unittest.TestSuite()
    suite.addTest(TestBetweenessCentrality("test_betweeness_centrality_11"))
    suite.addTest(TestBetweenessCentrality("test_betweeness_centrality_12"))
    suite.addTest(TestBetweenessCentrality("test_betweeness_centrality_13"))
    runner = unittest.TextTestRunner()
    runner.run(suite)
