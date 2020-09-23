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

from IntegrationTest.graphTest.serverTest.common.hugegraph_api.algorithm_api import AlgInterface
from IntegrationTest.graphTest.serverTest.testCase.algorithm.task_status import Task
from IntegrationTest.graphTest.serverTest.common.config.produce_data import ProduceData

TYPE = "basic"


class TestLouvain(unittest.TestCase):
    """
    接口louvain：louvain社区发现
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
        cls.modularity = 0.5680473372781065
        cls.expect_result_no = {"pass_times": 2, "phase1_times": 3, "last_precision": 0.0, "times": 20,
                                 "communities": 5, "modularity": 0.5680473372781065}
        cls.expect_result_sourcelabel = {"pass_times": 2, "phase1_times": 2, "last_precision": 0.0, "times": 20,
                                          "communities": 4, "modularity": 0.5680473372781065}
        cls.expect_result_degree = {"pass_times": 2, "phase1_times": 2, "last_precision": 0.0, "times": 20,
                                     "communities": 5, "modularity": 0.5680473372781065}
        cls.expect_result_times = {"pass_times": 2, "phase1_times": 2, "last_precision": 0.0, "times": 5,
                                    "communities": 5, "modularity": 0.5680473372781065}
        cls.expect_result_stabletimes = {"pass_times": 2, "phase1_times": 2, "last_precision": 0.0, "times": 20,
                                          "communities": 5, "modularity": 0.5680473372781065}
        cls.expect_result_5 = {"pass_times": 2, "phase1_times": 2, "last_precision": 0.0, "times": 10,
                                "communities": 5, "modularity": 0.5680473372781065}
        cls.expect_result_worker0 = {"pass_times": 2, "phase1_times": 2, "last_precision": 0.0, "times": 20,
                                      "communities": 5, "modularity": 0.5680473372781065}
        cls.expect_result_worker100 = {"pass_times": 2, "phase1_times": 4, "last_precision": 0.0, "times": 20,
                                        "communities": 5, "modularity": 0.5680473372781065}

    @classmethod
    def tearDownClass(cls):
        """
        init graph
        """
        pass

    # @unittest.skip("skip")
    def test_louvain_01(self):
        """
        :return:
        """
        body = {}
        code, ret = self.alg.post_louvain(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(cmp(result["modularity"], self.modularity), 0, "result check not pass")

    def test_louvain_02(self):
        """
        :return:
        """
        body = {"source_label": "person", "workers": 0}
        code, ret = self.alg.post_louvain(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(cmp(result, self.expect_result_sourcelabel), 0, "result check not pass")

    def test_louvain_03(self):
        """
        :return:
        """
        body = {"degree": 5, "workers": 0}
        code, ret = self.alg.post_louvain(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(cmp(result, self.expect_result_degree), 0, "result check not pass")

    def test_louvain_004(self):
        """
        :return:
        """
        body = {"times": 5, "workers": 0}
        code, ret = self.alg.post_louvain(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(cmp(result, self.expect_result_times), 0, "result check not pass")

    def test_louvain_05(self):
        """
        :return:
        """
        body = {"stable_times": 5, "workers": 0}
        code, ret = self.alg.post_louvain(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(cmp(result, self.expect_result_stabletimes), 0, "result check not pass")

    def test_louvain_06(self):
        """
        :return:
        """
        body = {"percision": 0.1, "workers": 0}
        code, ret = self.alg.post_louvain(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(cmp(result, self.expect_result_degree), 0, "result check not pass")

    def test_louvain_07(self):
        """
        :return:
        """
        body = {"show_community": "1:h", "workers": 0}
        code, ret = self.alg.post_louvain(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(cmp(result, []), 0, "result check not pass")

    def test_louvain_08(self):
        """
        :return:
        """
        body = {"clear": -1, "workers": 0}
        code, ret = self.alg.post_louvain(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(result, 0, "result check not pass")

    def test_louvain_09(self):
        """
        :return:
        """
        body = {"clear": 0, "workers": 0}
        code, ret = self.alg.post_louvain(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(result, 0, "result check not pass")

    @unittest.skip("skip")
    def test_louvain_10(self):
        """
        :return:com.baidu.algorithm.HugeException: Failed to execute algorithm: Undefined vertex label: 'c_pass-0'
        """
        body = {"show_modularity": 0, "workers": 0}
        code, ret = self.alg.post_louvain(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(cmp(result, self.expect_result_sourcelabel), 0, "result check not pass")

    def test_louvain_11(self):
        """
        :return:
        """
        body = {"degree": 5,
                "times": 10,
                "stable_times": 5,
                "percision": 0.1,
                "workers": 0}
        code, ret = self.alg.post_louvain(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(cmp(result, self.expect_result_5), 0, "result check not pass")

    def test_louvain_12(self):
        """
        :return:
        """
        body = {"degree": -1,
                "times": 10,
                "stable_times": 5,
                "percision": 0.1,
                "source_label": "person",
                "show_community": "1:h",
                "clear": -1,
                "show_modularity": 0,
                "workers": 0}
        code, ret = self.alg.post_louvain(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(result, 0, "result check not pass")

    def test_louvain_13(self):
        """
        :return:
        """
        body = {"workers": -1}
        code, ret = self.alg.post_louvain(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(cmp(result["modularity"], self.modularity), 0, "result check not pass")

    def test_louvain_14(self):
        """
        :return:
        """
        body = {"workers": 0}
        code, ret = self.alg.post_louvain(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(cmp(result, self.expect_result_worker0), 0, "result check not pass")

    def test_louvain_15(self):
        """
        :return:
        """
        body = {"workers": 100}
        code, ret = self.alg.post_louvain(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(cmp(result["modularity"], self.modularity), 0, "result check not pass")


if __name__ == '__main__':
    # run all cases
    unittest.main(verbosity=2)

    # run one case
    # suite = unittest.TestSuite()
    # suite.addTest(TestLouvain("test_louvain_001"))
    # runner = unittest.TextTestRunner()
    # runner.run(suite)
