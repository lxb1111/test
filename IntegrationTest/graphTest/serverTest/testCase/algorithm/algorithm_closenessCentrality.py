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
from filecmp import cmp
import importlib

sys.path.append('%s/..' % os.path.split(os.path.realpath(__file__))[0])
sys.path.append('../../')
importlib.reload(sys)
sys.setdefaultencoding('utf-8')

from IntegrationTest.graphTest.serverTest.common.hugegraph_api.algorithm_api import AlgInterface
from IntegrationTest.graphTest.serverTest.testCase.algorithm.task_status import Task
from IntegrationTest.graphTest.serverTest.common.config.produce_data import ProduceData

TYPE = "centrality"


class TestClosenessCentrality(unittest.TestCase):
    """
    接口closeness_centrality：紧密中心性
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
        cls.expect_result_01 = {"1:vadas": 1.0833333333333333, "2:lop": 1.0833333333333333,
                                    "1:marko": 0.8333333333333333, "1:josh": 0.8333333333333333, "2:ripple": 0.5,
                                    "1:peter": 0.5}
        cls.expect_result_02 = {"1:vadas": 1.0833333333333333, "2:lop": 1.0833333333333333, "2:ripple": 0.5,
                                           "1:marko": 0.5, "1:josh": 0.5, "1:peter": 0.5}
        cls.expect_result_03 = {"2:lop": 1.0833333333333333, "1:josh": 0.5}
        cls.expect_result_04 = {"2:ripple": 2.1666666666666665, "1:marko": 2.1666666666666665,
                                     "1:peter": 2.1666666666666665, "1:josh": 1.6666666666666665,
                                     "1:vadas": 1.6666666666666665, "2:lop": 1.6666666666666665}
        cls.expect_result_05 = {"2:lop": 2.3666666666666667, "1:marko": 2.333333333333333,
                                      "1:vadas": 1.9166666666666665, "1:josh": 1.6666666666666665,
                                      "2:ripple": 1.5833333333333333, "1:peter": 1.5833333333333333}
        cls.expect_result_06 = {"2:ripple": 1.0, "1:marko": 0.8333333333333333, "1:peter": 0.8333333333333333}
        cls.expect_result_07 = {"1:marko": 1.3333333333333333, "1:peter": 1.3333333333333333,
                                           "1:josh": 1.0833333333333333, "1:vadas": 1.0833333333333333}
        cls.expect_result_08 = {"2:ripple": 2.1666666666666665, "1:marko": 2.1666666666666665,
                                            "1:peter": 2.1666666666666665, "1:josh": 1.6666666666666665,
                                            "1:vadas": 1.6666666666666665, "2:lop": 1.6666666666666665}
        cls.expect_result_09 = {"1:marko": 1.8333333333333333, "1:peter": 1.0, "2:lop": 0.5}
        cls.expect_result_10 = {"2:ripple": 1.5, "1:josh": 0.8333333333333333, "1:vadas": 0.5, "1:peter": 0.5}
        cls.expect_result_11 = {"2:ripple": 2.1666666666666665, "1:marko": 2.1666666666666665,
                                        "1:peter": 2.1666666666666665, "1:josh": 1.6666666666666665,
                                        "1:vadas": 1.6666666666666665, "2:lop": 1.6666666666666665}
        cls.expect_result_12 = {"2:ripple": 2.1666666666666665, "1:marko": 2.1666666666666665,
                                        "1:peter": 2.1666666666666665, "1:josh": 1.6666666666666665,
                                        "1:vadas": 1.6666666666666665}
        cls.expect_result_13 = {"2:ripple": 2.1666666666666665, "1:marko": 2.1666666666666665,
                                "1:peter": 2.1666666666666665, "1:josh": 1.6666666666666665,
                                "1:vadas": 1.6666666666666665, "2:lop": 1.6666666666666665}
        cls.expect_result_14 = {"2:ripple": 1.0, "1:marko": 0.8333333333333333, "1:peter": 0.8333333333333333}
        cls.expect_result_15 = {"2:ripple": 2.1666666666666665, "1:marko": 2.1666666666666665,
                                    "1:peter": 2.1666666666666665, "1:josh": 1.6666666666666665,
                                    "1:vadas": 1.6666666666666665, "2:lop": 1.6666666666666665}
        cls.expect_result_16 = {"2:ripple": 1.5, "1:josh": 0.8333333333333333, "1:vadas": 0.5, "1:peter": 0.5}
        cls.expect_result_17 = {"1:marko": 1.8333333333333333, "1:peter": 1.0, "2:lop": 0.5}
        cls.expect_result_18 = {"2:ripple": 1.0, "1:marko": 0.8333333333333333, "1:peter": 0.8333333333333333}
        cls.expect_result_19 = {"2:ripple": 1.0, "1:marko": 0.8333333333333333, "1:peter": 0.8333333333333333}

    @classmethod
    def tearDownClass(cls):
        """
        init graph
        """
        pass

    def test_closeness_centrality_01(self):  # 结果会变
        """
        param=[depth]
        :return:
        """
        body = {"depth": 5}
        code, ret = self.alg.post_closeness_centrality(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        # self.assertEqual(cmp(result, self.expect_result_01), 0, "result check not pass")

    def test_closeness_centrality_02(self):  # 结果会变
        """
        param=[depth, source_sample]
        :return:
        """
        body = {"depth": 5, "source_sample": -1}
        code, ret = self.alg.post_closeness_centrality(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        # self.assertEqual(cmp(result, self.expect_result_02), 0, "result check not pass")

    def test_closeness_centrality_03(self):  # 结果会变
        """
        param=[depth, source_sample]
        :return:
        """
        body = {"depth": 5, "source_sample": 2}
        code, ret = self.alg.post_closeness_centrality(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        # self.assertEqual(cmp(result, self.expect_result_03), 0, "result check not pass")

    def test_closeness_centrality_04(self):
        """
        param=[depth, sample]
        :return:
        """
        body = {"depth": 5, "sample": -1}
        code, ret = self.alg.post_closeness_centrality(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(cmp(result, self.expect_result_04), 0, "result check not pass")

    def test_closeness_centrality_05(self):  # 结果会变
        """
        param=[depth, sample]
        :return:
        """
        body = {"depth": 5, "sample": 2}
        code, ret = self.alg.post_closeness_centrality(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        # self.assertEqual(cmp(result, self.expect_result_05), 0, "result check not pass")

    def test_closeness_centrality_06(self):
        """
        param=[depth, label, sample]
        :return:
        """
        body = {"depth": 5, "sample": -1, "label": "created"}
        code, ret = self.alg.post_closeness_centrality(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(cmp(result, self.expect_result_06), 0, "result check not pass")

    def test_closeness_centrality_07(self):
        """
        param=[depth, label, sample]
        :return:
        """
        body = {"depth": 5, "sample": -1, "label": "knows"}
        code, ret = self.alg.post_closeness_centrality(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(cmp(result, self.expect_result_07), 0, "result check not pass")

    def test_closeness_centrality_08(self):
        """
        param=[depth, direction, sample]
        :return:
        """
        body = {"depth": 5, "sample": -1, "direction": "BOTH"}
        code, ret = self.alg.post_closeness_centrality(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(cmp(result, self.expect_result_08), 0, "result check not pass")

    def test_closeness_centrality_09(self):
        """
        param=[depth, direction, sample]
        :return:
        """
        body = {"depth": 5, "sample": -1, "direction": "OUT"}
        code, ret = self.alg.post_closeness_centrality(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(cmp(result, self.expect_result_09), 0, "result check not pass")

    def test_closeness_centrality_10(self):
        """
        param=[depth, direction, sample]
        :return:
        """
        body = {"depth": 5, "sample": -1, "direction": "IN"}
        code, ret = self.alg.post_closeness_centrality(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(cmp(result, self.expect_result_10), 0, "result check not pass")

    def test_closeness_centrality_11(self):
        """
        param=[depth, degree, sample]
        :return:
        """
        body = {"depth": 5, "sample": -1, "degree": 5}
        code, ret = self.alg.post_closeness_centrality(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(cmp(result, self.expect_result_11), 0, "result check not pass")

    def test_closeness_centrality_12(self):
        """
        param=[depth, top, sample]
        :return:
        """
        body = {"depth": 5, "sample": -1, "top": 5}
        code, ret = self.alg.post_closeness_centrality(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(cmp(result, self.expect_result_12), 0, "result check not pass")

    # @unittest.skip("skip")
    def test_closeness_centrality_13(self):
        """
        param=[depth, degree, sample, top, source_sample]
        :return:
        """
        body = {"depth": 5, "degree": 50, "sample": -1, "top": 10, "source_sample": -1}
        code, ret = self.alg.post_closeness_centrality(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(cmp(result, self.expect_result_13), 0, "result check not pass")

    # @unittest.skip("skip")
    def test_closeness_centrality_14(self):
        """
        param=[depth, degree, sample, top, source_sample, label]
        :return:
        """
        body = {"depth": 5, "degree": 50, "sample": -1, "top": 10, "source_sample": -1, "label": "created"}
        code, ret = self.alg.post_closeness_centrality(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(cmp(result, self.expect_result_14), 0, "result check not pass")

    # @unittest.skip("skip")
    def test_closeness_centrality_15(self):
        """
        param=[depth, degree, sample, top, source_sample, direction]
        :return:
        """
        body = {"depth": 5, "degree": 50, "sample": -1, "top": 10, "source_sample": -1, "direction": "BOTH"}
        code, ret = self.alg.post_closeness_centrality(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(cmp(result, self.expect_result_15), 0, "result check not pass")

    def test_closeness_centrality_16(self):
        """
        param=[depth, degree, sample, top, source_sample, direction]
        :return:
        """
        body = {"depth": 5, "degree": 50, "sample": -1, "top": 10, "source_sample": -1, "direction": "IN"}
        code, ret = self.alg.post_closeness_centrality(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(cmp(result, self.expect_result_16), 0, "result check not pass")

    def test_closeness_centrality_17(self):
        """
        param=[depth, degree, sample, top, source_sample, direction]
        :return:
        """
        body = {"depth": 5, "degree": 50, "sample": -1, "top": 10, "source_sample": -1, "direction": "OUT"}
        code, ret = self.alg.post_closeness_centrality(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(cmp(result, self.expect_result_17), 0, "result check not pass")

    def test_closeness_centrality_18(self):
        """
        param=[depth, degree, sample, top, source_sample, direction, label]
        :return:
        """
        body = {"depth": 5, "degree": 50, "sample": -1, "top": 10, "source_sample": -1,
                "direction": "BOTH", "label": "created"}
        code, ret = self.alg.post_closeness_centrality(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        print (result)
        self.assertEqual(cmp(result, self.expect_result_18), 0, "result check not pass")

    # @unittest.skip("skip")
    def test_closeness_centrality_19(self):
        """
        param=[depth, degree, sample, top, source_sample, direction, label]
        :return:
        """
        body = {"depth": 5, "degree": 50, "sample": -1, "top": 10, "source_sample": 10,
                "direction": "BOTH", "label": "created"}
        code, ret = self.alg.post_closeness_centrality(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        print (result)
        self.assertEqual(cmp(result, self.expect_result_19), 0, "result check not pass")


if __name__ == '__main__':
    # run all cases
    # unittest.main(verbosity=2)

    # run one case
    suite = unittest.TestSuite()
    suite.addTest(TestClosenessCentrality("test_closeness_centrality_18"))
    suite.addTest(TestClosenessCentrality("test_closeness_centrality_19"))
    runner = unittest.TextTestRunner()
    runner.run(suite)
