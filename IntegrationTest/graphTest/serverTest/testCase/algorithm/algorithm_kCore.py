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


class TestKCore(unittest.TestCase):
    """
    接口kcore：K-Core社区发现
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
        cls.expect_result_no = {"kcores": []}

    @classmethod
    def tearDownClass(cls):
        """
        init graph
        """
        pass

    def test_kcore_01(self):
        """
        无参数
        :return:
        """
        body = {}
        code, ret = self.alg.post_kcore(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(cmp(result, self.expect_result_no), 0, "result check not pass")

    def test_kcore_02(self):
        """
        :return:
        """
        body = {"source_label": "person"}
        code, ret = self.alg.post_kcore(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(cmp(result, self.expect_result_no), 0, "result check not pass")

    def test_kcore_03(self):
        """
        :return:
        """
        body = {"direction": "BOTH"}
        code, ret = self.alg.post_kcore(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(cmp(result, self.expect_result_no), 0, "result check not pass")

    def test_kcore_04(self):
        """
        :return:
        """
        body = {"direction": "IN"}
        code, ret = self.alg.post_kcore(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(cmp(result, self.expect_result_no), 0, "result check not pass")

    def test_kcore_05(self):
        """
        :return:
        """
        body = {"direction": "OUT"}
        code, ret = self.alg.post_kcore(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(cmp(result, self.expect_result_no), 0, "result check not pass")

    def test_kcore_06(self):
        """
        :return:
        """
        body = {"label": "created"}
        code, ret = self.alg.post_kcore(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(cmp(result, self.expect_result_no), 0, "result check not pass")

    def test_kcore_07(self):
        """
        :return:
        """
        body = {"k": 3}
        code, ret = self.alg.post_kcore(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(cmp(result, self.expect_result_no), 0, "result check not pass")

    def test_kcore_08(self):
        """
        :return:
        """
        body = {"k": 5}
        code, ret = self.alg.post_kcore(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(cmp(result, self.expect_result_no), 0, "result check not pass")

    def test_kcore_09(self):
        """
        :return:
        """
        body = {"alpha": 0.1}
        code, ret = self.alg.post_kcore(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(cmp(result, self.expect_result_no), 0, "result check not pass")

    def test_kcore_10(self):
        """
        :return:
        """
        body = {"alpha": 0.9}
        code, ret = self.alg.post_kcore(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(cmp(result, self.expect_result_no), 0, "result check not pass")

    def test_kcore_11(self):
        """
        :return:
        """
        body = {"degree": 1}
        code, ret = self.alg.post_kcore(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(cmp(result, self.expect_result_no), 0, "result check not pass")

    def test_kcore_12(self):
        """
        :return:
        """
        body = {"degree": 3}
        code, ret = self.alg.post_kcore(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(cmp(result, self.expect_result_no), 0, "result check not pass")

    def test_kcore_13(self):
        """
        :return:
        """
        body = {"merged": True}
        code, ret = self.alg.post_kcore(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(cmp(result, self.expect_result_no), 0, "result check not pass")

    def test_kcore_14(self):
        """
        :return:
        """
        body = {"merged": False}
        code, ret = self.alg.post_kcore(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(cmp(result, self.expect_result_no), 0, "result check not pass")

    # @unittest.skip("skip")
    def test_kcore_15(self):
        """
        :return:
        """
        body = {"direction": "BOTH", "k": 4, "degree": 3}
        code, ret = self.alg.post_kcore(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(cmp(result, self.expect_result_no), 0, "result check not pass")

    def test_kcore_16(self):
        """
        :return:
        """
        body = {"direction": "BOTH", "k": 4, "degree": 3, "alpha": 0.6}
        code, ret = self.alg.post_kcore(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(cmp(result, self.expect_result_no), 0, "result check not pass")

    def test_kcore_17(self):
        """
        校验基本参数 + alpha=0.6, merged=true
        :return:
        """
        body = {"direction": "BOTH", "k": 4, "degree": 3, "alpha": 0.6, "merged": True}
        code, ret = self.alg.post_kcore(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(cmp(result, self.expect_result_no), 0, "result check not pass")

    def test_kcore_18(self):
        """
        校验基本参数 +alpha=0.6, merged=true,direction=IN
        :return:
        """
        body = {"direction": "IN", "k": 4, "degree": 3, "alpha": 0.6, "merged": True}
        code, ret = self.alg.post_kcore(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(cmp(result, self.expect_result_no), 0, "result check not pass")

    def test_kcore_19(self):
        """
        校验基本参数 + alpha=0.6, merged=true,direction=OUT
        :return:
        """
        body = {"direction": "OUT", "k": 4, "degree": 3, "alpha": 0.6, "merged": True}
        code, ret = self.alg.post_kcore(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(cmp(result, self.expect_result_no), 0, "result check not pass")

    def test_kcore_20(self):
        """
        校验基本参数 + alpha=0.6, merged=true,label=knows
        :return:
        """
        body = {"direction": "OUT", "k": 4, "degree": 3, "alpha": 0.6, "merged": True, "label": "knows"}
        code, ret = self.alg.post_kcore(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(cmp(result, self.expect_result_no), 0, "result check not pass")

    def test_kcore_21(self):
        """
        :return:
        """
        body = {"workers": -1}
        code, ret = self.alg.post_kcore(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(cmp(result, self.expect_result_no), 0, "result check not pass")

    def test_kcore_22(self):
        """
        :return:
        """
        body = {"workers": 0}
        code, ret = self.alg.post_kcore(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(cmp(result, self.expect_result_no), 0, "result check not pass")

    def test_kcore_23(self):
        """
        :return:
        """
        body = {"workers": 100}
        code, ret = self.alg.post_kcore(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(cmp(result, self.expect_result_no), 0, "result check not pass")

    def test_kcore_24(self):
        """
        校验基本参数 + alpha=0.6, merged=true,label=knows
        :return:
        """
        body = {"direction": "OUT", "k": 4, "degree": 3, "alpha": 0.6, "merged": True, "label": "knows", "workers": 0}
        code, ret = self.alg.post_kcore(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(cmp(result, self.expect_result_no), 0, "result check not pass")


if __name__ == '__main__':
    # run all cases
    # unittest.main(verbosity=2)

    # run one case
    suite = unittest.TestSuite()
    suite.addTest(TestKCore("test_kcore_01"))
    runner = unittest.TextTestRunner()
    runner.run(suite)
