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


TYPE = "centrality"


class TestDegreeCentrality(unittest.TestCase):
    """
    接口degree_centrality：度中心性
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
        cls.expect_result_01 = {"2:lop": 1, "1:josh": 1, "1:marko": 3, "1:peter": 3, "1:vadas": 1, "2:ripple": 3}
        cls.expect_result_02 = {"1:marko": 1, "1:peter": 1, "2:ripple": 2}
        cls.expect_result_03 = {"1:josh": 1, "1:marko": 2, "1:peter": 2, "1:vadas": 1}
        cls.expect_result_04 = {"2:lop": 1, "1:josh": 1, "1:marko": 3, "1:peter": 3, "1:vadas": 1,
                                            "2:ripple": 3}
        cls.expect_result_05 = {"2:lop": 1, "1:marko": 3, "1:peter": 2}
        cls.expect_result_06 = {"1:josh": 1, "1:peter": 1, "1:vadas": 1, "2:ripple": 3}
        cls.expect_result_07 = {"2:lop": 1, "1:josh": 1, "1:marko": 3, "1:peter": 3, "1:vadas": 1, "2:ripple": 3}
        cls.expect_result_08 = {"2:ripple": 3, "1:marko": 3, "1:peter": 3, "1:josh": 1, "1:vadas": 1}

        cls.expect_result_09 = {"1:marko": 3, "1:peter": 2, "2:lop": 1}
        cls.expect_result_10 = {"1:marko": 1, "1:peter": 1}
        cls.expect_result_11 = {"2:ripple": 2}
        cls.expect_result_12 = {"1:marko": 1, "1:peter": 1}

    @classmethod
    def tearDownClass(cls):
        """
        init graph
        """
        pass

    # @unittest.skip("skip")
    def test_degree_centrality_01(self):
        """
        no param
        :return:
        """
        body = {}
        code, ret = self.alg.post_degree_centrality(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(cmp(result, self.expect_result_01), 0, "result check not pass")

    # @unittest.skip("skip")
    def test_degree_centrality_02(self):
        """
        param = [label]
        :return:
        """
        body = {"label": "created"}
        code, ret = self.alg.post_degree_centrality(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(cmp(result, self.expect_result_02), 0, "result check not pass")

    # @unittest.skip("skip")
    def test_degree_centrality_03(self):
        """
        param = [label]
        :return:
        """
        body = {"label": "knows"}
        code, ret = self.alg.post_degree_centrality(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(cmp(result, self.expect_result_03), 0, "result check not pass")

    # @unittest.skip("skip")
    def test_degree_centrality_04(self):
        """
        param = [direction]
        :return:
        """
        body = {"direction": "BOTH"}
        code, ret = self.alg.post_degree_centrality(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(cmp(result, self.expect_result_04), 0, "result check not pass")

    def test_degree_centrality_05(self):
        """
        param = [direction]
        :return:
        """
        body = {"direction": "OUT"}
        code, ret = self.alg.post_degree_centrality(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(cmp(result, self.expect_result_05), 0, "result check not pass")

    def test_degree_centrality_06(self):
        """
        param = [direction]
        :return:
        """
        body = {"direction": "IN"}
        code, ret = self.alg.post_degree_centrality(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(cmp(result, self.expect_result_06), 0, "result check not pass")

    def test_degree_centrality_07(self):
        """
        param = [top]
        :return:
        """
        body = {"top": 0}
        code, ret = self.alg.post_degree_centrality(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(cmp(result, self.expect_result_07), 0, "result check not pass")

    def test_degree_centrality_08(self):
        """
        param = [top]
        :return:
        """
        body = {"top": 5}
        code, ret = self.alg.post_degree_centrality(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(cmp(result, self.expect_result_08), 0, "result check not pass")

    # @unittest.skip("skip")
    def test_degree_centrality_09(self):
        """
        param = [top、direction]
        :return:
        """
        body = {"direction": "OUT", "top": 5}
        code, ret = self.alg.post_degree_centrality(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(cmp(result, self.expect_result_09), 0, "result check not pass")

    # @unittest.skip("skip")
    def test_degree_centrality_10(self):
        """
        param = [top、direction、label]
        :return:
        """
        body = {"direction": "OUT", "top": 5, "label": "created"}
        code, ret = self.alg.post_degree_centrality(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(cmp(result, self.expect_result_10), 0, msg="result check not pass")

    # @unittest.skip("skip")
    def test_degree_centrality_11(self):
        """
        param = [top、direction、label]
        :return:
        """
        body = {"direction": "IN", "top": 5, "label": "created"}
        code, ret = self.alg.post_degree_centrality(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(cmp(result, self.expect_result_11), 0, msg="result check not pass")

    # @unittest.skip("skip")
    def test_degree_centrality_12(self):
        """
        param = [top、direction、label]
        :return:
        """
        body = {"direction": "OUT", "top": 5, "label": "created"}
        code, ret = self.alg.post_degree_centrality(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(cmp(result, self.expect_result_12), 0, msg="result check not pass")


if __name__ == '__main__':
    # run all cases
    unittest.main(verbosity=2)

    # run one case
    # suite = unittest.TestSuite()
    # suite.addTest(TestDegreeCentrality("test_degree_centrality_002"))
    # runner = unittest.TextTestRunner()
    # runner.run(suite)
