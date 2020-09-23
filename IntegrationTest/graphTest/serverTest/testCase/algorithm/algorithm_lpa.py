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
from filecmp import cmp
import importlib

sys.path.append('%s/..' % os.path.split(os.path.realpath(__file__))[0])
sys.path.append('../../')
importlib.reload(sys)

from IntegrationTest.graphTest.serverTest.common.hugegraph_api.algorithm_api import AlgInterface
from IntegrationTest.graphTest.serverTest.testCase.algorithm.task_status import Task
from IntegrationTest.graphTest.serverTest.common.config.produce_data import ProduceData

TYPE = "basic"


class TestLpa(unittest.TestCase):
    """
    接口lpa：lpa社区发现
    """

    @classmethod
    def setUpClass(cls):
        cls.alg = AlgInterface()
        cls.task = Task()
        cls.p = ProduceData()

        # 初始化数据
        cls.cleardata = cls.p.init_data("clear")
        cls.initdata = cls.p.init_data(TYPE)

        # 预期结果
        cls.expect_result = {"iteration_times": 20, "last_precision": 0.6875, "times": 20, "communities": 9}
        cls.expect_result_label = {"iteration_times": 2, "last_precision": 0.0, "times": 20, "communities": 9}
        cls.expect_result_direction = {"iteration_times": 3, "last_precision": 0.0, "times": 20, "communities": 5}
        cls.expect_result_directionOUT = {"iteration_times": 10, "last_precision": 0.0, "times": 20, "communities": 9}
        cls.expect_result_directionIN = {"iteration_times": 3, "last_precision": 0.0, "times": 20, "communities": 7}
        cls.expect_result_degree = {"iteration_times": 3, "last_precision": 0.0, "times": 20, "communities": 5}
        cls.expect_result_degree1 = {"iteration_times": 2, "last_precision": 0.0, "times": 20, "communities": 5}
        cls.expect_result_times = {"iteration_times": 3, "last_precision": 0.0, "times": 10, "communities": 5}
        cls.expect_result_4 = {"iteration_times": 2, "last_precision": 0.0, "times": 20, "communities": 10}
        cls.expect_result_workers = {"iteration_times": 20, "last_precision": 0.375, "times": 20, "communities": 7}
        cls.expect_result_workers0 = {"iteration_times": 3, "last_precision": 0.0, "times": 20, "communities": 5}
        cls.expect_result_workers100 = {"iteration_times": 20, "last_precision": 0.125, "times": 20, "communities": 6}

    @classmethod
    def tearDownClass(cls):
        """
        init graph
        """
        pass

    def test_lpa_01(self):
        """
        :return:
        """
        body = {}
        code, ret = self.alg.post_lpa(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        status, result = self.task.get_task_2(id)
        self.assertEqual(status, "success", msg="check status not pass")
        # self.assertEqual(cmp(result, self.expect_result), 0, "result check not pass")

    def test_lpa_02(self):
        """
        :return:
        """
        body = {"label": "created", "workers": 0}
        code, ret = self.alg.post_lpa(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        status, result = self.task.get_task_2(id)
        self.assertEqual(status, "success", msg="check status not pass")

    def test_lpa_03(self):
        """
        :return:
        """
        body = {"direction": "BOTH", "workers": 0}
        code, ret = self.alg.post_lpa(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(cmp(result, self.expect_result_direction), 0, "result check not pass")

    def test_lpa_04(self):
        """
        :return:
        """
        body = {"direction": "OUT", "workers": 0}
        code, ret = self.alg.post_lpa(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        status, result = self.task.get_task_2(id)
        self.assertEqual(status, "success", msg="check status not pass")

    def test_lpa_05(self):
        """
        :return:
        """
        body = {"direction": "IN", "workers": 0}
        code, ret = self.alg.post_lpa(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        status, result = self.task.get_task_2(id)
        self.assertEqual(status, "success", msg="check status not pass")
        # self.assertEqual(cmp(result, self.expect_result_directionIN), 0, "result check not pass")

    def test_lpa_06(self):
        """
        :return:
        """
        body = {"degree": 2, "workers": 0}
        code, ret = self.alg.post_lpa(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        status, result = self.task.get_task_2(id)
        self.assertEqual(status, "success", msg="check status not pass")
        # self.assertEqual(cmp(result, self.expect_result_degree), 0, "result check not pass")

    def test_lpa_07(self):
        """
        :return:
        """
        body = {"degree": -1, "workers": 0}
        code, ret = self.alg.post_lpa(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        status, result = self.task.get_task_2(id)
        self.assertEqual(status, "success", msg="check status not pass")
        # self.assertEqual(cmp(result, self.expect_result_degree1), 0, "result check not pass")

    def test_lpa_08(self):
        """
        :return:
        """
        body = {"times": 10, "workers": 0}
        code, ret = self.alg.post_lpa(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        status, result = self.task.get_task_2(id)
        self.assertEqual(status, "success", msg="check status not pass")
        # self.assertEqual(cmp(result, self.expect_result_times), 0, "result check not pass")

    def test_lpa_09(self):
        """
        :return:
        """
        body = {"percision": 0.5, "workers": 0}
        code, ret = self.alg.post_lpa(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(cmp(result, self.expect_result_degree), 0, "result check not pass")

    def test_lpa_10(self):
        """
        :return:
        """
        body_lpa = {"direction": "BOTH"}
        code, ret = self.alg.post_lpa(body_lpa)
        id = ret["task_id"]
        result = self.task.get_task(id)
        body = {"show_community": "1:qian",
                "workers": 0}
        code, ret = self.alg.post_lpa(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(cmp(result, ["1:qian"]), 0, "result check not pass")

    def test_lpa_11(self):
        """
        :return:
        """
        body = {"source_label": "person", "workers": 0}
        code, ret = self.alg.post_lpa(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        status, result = self.task.get_task_2(id)
        self.assertEqual(status, "success", msg="check status not pass")
        # self.assertEqual(cmp(result, self.expect_result_label), 0, "result check not pass")

    def test_lpa_12(self):
        """
        :return:
        """
        body = {
            # "source_label": "person",
            "label": "created",
            "direction": "OUT",
            "percision": 0.5,
            "workers": 0}
        code, ret = self.alg.post_lpa(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        status, result = self.task.get_task_2(id)
        self.assertEqual(status, "success", msg="check status not pass")
        # self.assertEqual(cmp(result, self.expect_result_4), 0, "result check not pass")

    def test_lpa_13(self):
        """
        :return:
        """
        body = {
            # "source_label": "person",
            "label": "created",
            "direction": "OUT",
            "percision": 0.5,
            "degree": 5,
            "times": 10,
            # "show_community": "1:r",
            "workers": 0}
        code, ret = self.alg.post_lpa(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        status, result = self.task.get_task_2(id)
        self.assertEqual(status, "success", msg="check status not pass")
        # self.assertEqual(cmp(result, self.expect_result_label), 0, "result check not pass")

    def test_lpa_14(self):
        """
        :return:
        """
        body = {"workers": -1}
        code, ret = self.alg.post_lpa(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        status, result = self.task.get_task_2(id)
        self.assertEqual(status, "success", msg="check status not pass")
        # self.assertEqual(cmp(result, self.expect_result_workers), 0, "result check not pass")

    def test_lpa_15(self):
        """
        :return:
        """
        body = {"workers": 0}
        code, ret = self.alg.post_lpa(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(cmp(result, self.expect_result_workers0), 0, "result check not pass")

    def test_lpa_16(self):
        """
        :return:
        """
        body = {"workers": 100}
        code, ret = self.alg.post_lpa(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        status, result = self.task.get_task_2(id)
        self.assertEqual(status, "success", msg="check status not pass")
        # self.assertEqual(cmp(result, self.expect_result_workers100), 0, "result check not pass")


if __name__ == '__main__':
    # run all cases
    unittest.main(verbosity=2)

    # run one case
    # suite = unittest.TestSuite()
    # suite.addTest(TestLpa("test_lpa_001"))
    # runner = unittest.TextTestRunner()
    # runner.run(suite)
