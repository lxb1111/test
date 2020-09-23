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


TYPE = "fusiform_similarity"


class TestFusiformSimilarity(unittest.TestCase):
    """
    接口fusiform_similarity：棱型发现
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
        cls.expect_result = {}
        cls.expect_result_4 = {"1:josh": [{"id": "2:ripple", "score": 1.0, "intermediaries": ["1:lily", "1:marko"]},
                                           {"id": "1:vadas", "score": 1.0, "intermediaries": ["1:lily", "1:marko"]},
                                           {"id": "1:peter", "score": 1.0, "intermediaries": ["1:lily", "1:marko"]},
                                           {"id": "2:lop", "score": 1.0, "intermediaries": ["1:lily", "1:marko"]}],
                                "1:peter": [{"id": "2:ripple", "score": 1.0, "intermediaries": ["1:lily", "1:marko"]},
                                            {"id": "1:josh", "score": 1.0, "intermediaries": ["1:lily", "1:marko"]},
                                            {"id": "1:vadas", "score": 1.0, "intermediaries": ["1:lily", "1:marko"]},
                                            {"id": "2:lop", "score": 1.0, "intermediaries": ["1:lily", "1:marko"]}],
                                "2:lop": [{"id": "2:ripple", "score": 1.0, "intermediaries": ["1:lily", "1:marko"]},
                                          {"id": "1:josh", "score": 1.0, "intermediaries": ["1:lily", "1:marko"]},
                                          {"id": "1:vadas", "score": 1.0, "intermediaries": ["1:lily", "1:marko"]},
                                          {"id": "1:peter", "score": 1.0, "intermediaries": ["1:lily", "1:marko"]}],
                                "1:vadas": [{"id": "2:ripple", "score": 1.0, "intermediaries": ["1:lily", "1:marko"]},
                                            {"id": "1:josh", "score": 1.0, "intermediaries": ["1:lily", "1:marko"]},
                                            {"id": "1:peter", "score": 1.0, "intermediaries": ["1:lily", "1:marko"]},
                                            {"id": "2:lop", "score": 1.0, "intermediaries": ["1:lily", "1:marko"]}],
                                "2:ripple": [{"id": "1:josh", "score": 1.0, "intermediaries": ["1:lily", "1:marko"]},
                                             {"id": "1:vadas", "score": 1.0, "intermediaries": ["1:lily", "1:marko"]},
                                             {"id": "1:peter", "score": 1.0, "intermediaries": ["1:lily", "1:marko"]},
                                             {"id": "2:lop", "score": 1.0, "intermediaries": ["1:lily", "1:marko"]}]}
        cls.expect_result_mini = {"2:lop": [{"id": "2:ripple", "score": 1.0, "intermediaries": ["1:lily", "1:marko"]},
                                             {"id": "1:josh", "score": 1.0, "intermediaries": ["1:lily", "1:marko"]},
                                             {"id": "1:vadas", "score": 1.0, "intermediaries": ["1:lily", "1:marko"]},
                                             {"id": "1:peter", "score": 1.0, "intermediaries": ["1:lily", "1:marko"]}],
                                   "2:ripple": [{"id": "1:josh", "score": 1.0, "intermediaries": ["1:lily", "1:marko"]},
                                                {"id": "1:vadas", "score": 1.0,
                                                 "intermediaries": ["1:lily", "1:marko"]},
                                                {"id": "1:peter", "score": 1.0,
                                                 "intermediaries": ["1:lily", "1:marko"]},
                                                {"id": "2:lop", "score": 1.0, "intermediaries": ["1:lily", "1:marko"]}],
                                   "1:vadas": [
                                       {"id": "2:ripple", "score": 1.0, "intermediaries": ["1:lily", "1:marko"]},
                                       {"id": "1:josh", "score": 1.0, "intermediaries": ["1:lily", "1:marko"]},
                                       {"id": "1:peter", "score": 1.0, "intermediaries": ["1:lily", "1:marko"]},
                                       {"id": "2:lop", "score": 1.0, "intermediaries": ["1:lily", "1:marko"]}],
                                   "1:peter": [
                                       {"id": "2:ripple", "score": 1.0, "intermediaries": ["1:lily", "1:marko"]},
                                       {"id": "1:josh", "score": 1.0, "intermediaries": ["1:lily", "1:marko"]},
                                       {"id": "1:vadas", "score": 1.0, "intermediaries": ["1:lily", "1:marko"]},
                                       {"id": "2:lop", "score": 1.0, "intermediaries": ["1:lily", "1:marko"]}],
                                   "1:josh": [{"id": "2:ripple", "score": 1.0, "intermediaries": ["1:lily", "1:marko"]},
                                              {"id": "1:vadas", "score": 1.0, "intermediaries": ["1:lily", "1:marko"]},
                                              {"id": "1:peter", "score": 1.0, "intermediaries": ["1:lily", "1:marko"]},
                                              {"id": "2:lop", "score": 1.0, "intermediaries": ["1:lily", "1:marko"]}]}
        cls.expect_result_alphatop = {
            "2:ripple": [{"id": "1:josh", "score": 1.0, "intermediaries": ["1:lily", "1:marko"]}],
            "2:lop": [{"id": "2:ripple", "score": 1.0, "intermediaries": ["1:lily", "1:marko"]}],
            "1:peter": [{"id": "2:ripple", "score": 1.0, "intermediaries": ["1:lily", "1:marko"]}],
            "1:vadas": [{"id": "2:ripple", "score": 1.0, "intermediaries": ["1:lily", "1:marko"]}],
            "1:josh": [{"id": "2:ripple", "score": 1.0, "intermediaries": ["1:lily", "1:marko"]}]}
        cls.expect_result_alphalimit = {
            "2:lop": [{"id": "2:ripple", "score": 1.0, "intermediaries": ["1:lily", "1:marko"]},
                      {"id": "1:josh", "score": 1.0, "intermediaries": ["1:lily", "1:marko"]},
                      {"id": "1:vadas", "score": 1.0, "intermediaries": ["1:lily", "1:marko"]},
                      {"id": "1:peter", "score": 1.0, "intermediaries": ["1:lily", "1:marko"]}]}
        cls.expect_result_in = {}
        cls.expect_result_out = {"1:josh": [{"id": "2:ripple", "score": 1.0, "intermediaries": ["1:lily", "1:marko"]}],
                                  "1:peter": [
                                      {"id": "2:ripple", "score": 1.0, "intermediaries": ["1:lily", "1:marko"]}],
                                  "1:vadas": [
                                      {"id": "2:ripple", "score": 1.0, "intermediaries": ["1:lily", "1:marko"]}],
                                  "2:lop": [{"id": "2:ripple", "score": 1.0, "intermediaries": ["1:lily", "1:marko"]}],
                                  "2:ripple": [{"id": "1:josh", "score": 1.0, "intermediaries": ["1:lily", "1:marko"]}]}

    @classmethod
    def tearDownClass(cls):
        """
        init graph
        """
        pass

    def test_fusiform_similarity_01(self):
        """
        无参数
        :return:
        """
        body = {}
        code, ret = self.alg.post_fusiform_similarity(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(cmp(result, self.expect_result), 0, "result check not pass")

    def test_fusiform_similarity_02(self):
        """
        :return:
        """
        body = {"source_label": "person"}
        code, ret = self.alg.post_fusiform_similarity(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(cmp(result, self.expect_result), 0, "result check not pass")

    def test_fusiform_similarity_03(self):
        """
        :return:
        """
        body = {"direction": "BOTH"}
        code, ret = self.alg.post_fusiform_similarity(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(cmp(result, self.expect_result), 0, "result check not pass")

    def test_fusiform_similarity_04(self):
        """
        :return:
        """
        body = {"direction": "OUT"}
        code, ret = self.alg.post_fusiform_similarity(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(cmp(result, self.expect_result), 0, "result check not pass")

    def test_fusiform_similarity_05(self):
        """
        :return:
        """
        body = {"direction": "IN"}
        code, ret = self.alg.post_fusiform_similarity(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(cmp(result, self.expect_result), 0, "result check not pass")

    def test_fusiform_similarity_06(self):
        """
        :return:
        """
        body = {"label": "help"}
        code, ret = self.alg.post_fusiform_similarity(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(cmp(result, self.expect_result), 0, "result check not pass")

    def test_fusiform_similarity_07(self):  # 这个是2个参数
        """
        :return:
        """
        body = {"min_neighbors": 2,
                "min_similars": 4}
        code, ret = self.alg.post_fusiform_similarity(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(cmp(result, self.expect_result_mini), 0, "result check not pass")

    def test_fusiform_similarity_08(self):
        """
        :return:
        """
        body = {"alpha": 0.8}
        code, ret = self.alg.post_fusiform_similarity(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(cmp(result, self.expect_result), 0, "result check not pass")

    def test_fusiform_similarity_09(self):
        """
        :return:
        """
        body = {"min_similars": 4}
        code, ret = self.alg.post_fusiform_similarity(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(cmp(result, self.expect_result), 0, "result check not pass")

    def test_fusiform_similarity_10(self):
        """
        :return:
        """
        body = {"top": 0}
        code, ret = self.alg.post_fusiform_similarity(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(cmp(result, self.expect_result), 0, "result check not pass")

    def test_fusiform_similarity_11(self):
        """
        :return:
        """
        body = {"top": 4}
        code, ret = self.alg.post_fusiform_similarity(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(cmp(result, self.expect_result), 0, "result check not pass")

    def test_fusiform_similarity_12(self):
        """
        :return:
        """
        body = {"group_property": ""}
        code, ret = self.alg.post_fusiform_similarity(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(cmp(result, self.expect_result), 0, "result check not pass")

    def test_fusiform_similarity_13(self):
        """
        :return:
        """
        body = {"group_property": "software"}
        code, ret = self.alg.post_fusiform_similarity(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(cmp(result, self.expect_result), 0, "result check not pass")

    def test_fusiform_similarity_14(self):
        """
        :return:
        """
        body = {"min_groups": 2}
        code, ret = self.alg.post_fusiform_similarity(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(cmp(result, self.expect_result), 0, "result check not pass")

    def test_fusiform_similarity_15(self):
        """
        :return:
        """
        body = {"degree": 5}
        code, ret = self.alg.post_fusiform_similarity(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(cmp(result, self.expect_result), 0, "result check not pass")

    def test_fusiform_similarity_16(self):
        """
        :return:
        """
        body = {"capacity": 5}
        code, ret = self.alg.post_fusiform_similarity(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(cmp(result, self.expect_result), 0, "result check not pass")

    def test_fusiform_similarity_17(self):
        """
        :return:
        """
        body = {"limit": -1}
        code, ret = self.alg.post_fusiform_similarity(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(cmp(result, self.expect_result), 0, "result check not pass")

    def test_fusiform_similarity_18(self):
        """
        :return:
        """
        body = {"limit": 2}
        code, ret = self.alg.post_fusiform_similarity(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(cmp(result, self.expect_result), 0, "result check not pass")

    # @unittest.skip("skip")
    def test_fusiform_similarity_19(self):
        """
        基本参数校验组合
        :return:
        """
        body = {"direction": "BOTH", "min_neighbors": 2, "min_similars": 4, "degree": -1}
        code, ret = self.alg.post_fusiform_similarity(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(cmp(result, self.expect_result_4), 0, "result check not pass")

    # @unittest.skip("skip")
    def test_fusiform_similarity_20(self):
        """
        校验基本参数 + alpha=0.4, top=1
        :return:
        """
        body = {"direction": "BOTH", "min_neighbors": 2, "min_similars": 4, "degree": -1, "alpha": 0.4, "top": 1}
        code, ret = self.alg.post_fusiform_similarity(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(cmp(result, self.expect_result_alphatop), 0, "result check not pass")

    # @unittest.skip("skip")
    def test_fusiform_similarity_21(self):
        """
        校验基本参数 + alpha=0.4, limit=1
        :return:
        """
        body = {"direction": "BOTH", "min_neighbors": 2, "min_similars": 4, "degree": -1, "alpha": 0.4, "limit": 1}
        code, ret = self.alg.post_fusiform_similarity(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(cmp(result, self.expect_result_alphalimit), 0, "result check not pass")

    def test_fusiform_similarity_22(self):
        """
        校验基本参数 + + alpha=0.4, top=1,direction=IN
        :return:
        """
        body = {"direction": "IN", "min_neighbors": 2, "min_similars": 4, "degree": -1, "alpha": 0.4, "top": 1}
        code, ret = self.alg.post_fusiform_similarity(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(cmp(result, self.expect_result_in), 0, "result check not pass")

    def test_fusiform_similarity_23(self):
        """
        校验基本参数 + + alpha=0.4, top=1,direction=OUT
        :return:
        """
        body = {"direction": "OUT", "min_neighbors": 2, "min_similars": 4, "degree": -1, "alpha": 0.4, "top": 1}
        code, ret = self.alg.post_fusiform_similarity(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(cmp(result, self.expect_result_out), 0, "result check not pass")

    def test_fusiform_similarity_24(self):
        """
        校验基本参数 + + alpha=0.4, top=1,direction=OUT
        :return:
        """
        body = {
            # "source_label": "person",
            "direction": "BOTH",
            "label": "help",
            "min_neighbors": 5,
            "alpha": 0.9,
            "min_similars": 6,
            "top": 0,
            "group_property": "",
            "min_groups": 2,
            "degree": 5,
            "capacity": 5,
            "limit": -1,
        }
        code, ret = self.alg.post_fusiform_similarity(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(cmp(result, self.expect_result), 0, "result check not pass")

    def test_fusiform_similarity_25(self):
        """
        校验基本参数workers
        :return:
        """
        body = {"workers": -1}
        code, ret = self.alg.post_fusiform_similarity(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        status, result = self.task.get_task_2(id)
        self.assertEqual(status, "success", msg="check status not pass")
        # self.assertEqual(cmp(result, self.expect_result_out), 0, "result check not pass")

    def test_fusiform_similarity_26(self):
        """
        校验基本参数workers
        :return:
        """
        body = {"workers": 0}
        code, ret = self.alg.post_fusiform_similarity(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        status, result = self.task.get_task_2(id)
        self.assertEqual(status, "success", msg="check status not pass")
        # self.assertEqual(cmp(result, self.expect_result_out), 0, "result check not pass")

    def test_fusiform_similarity_27(self):
        """
        校验基本参数workers
        :return:
        """
        body = {"workers": 100}
        code, ret = self.alg.post_fusiform_similarity(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        status, result = self.task.get_task_2(id)
        self.assertEqual(status, "success", msg="check status not pass")
        # self.assertEqual(cmp(result, self.expect_result_out), 0, "result check not pass")

    def test_fusiform_similarity_28(self):
        """
        校验基本参数 + + alpha=0.4, top=1,direction=OUT,workers=0
        :return:
        """
        body = {"direction": "OUT", "min_neighbors": 2, "min_similars": 4, "degree": -1,
                "alpha": 0.4, "top": 1, "workers": 0}
        code, ret = self.alg.post_fusiform_similarity(body)
        self.assertEqual(code, 201)
        id = ret["task_id"]
        result = self.task.get_task(id)
        self.assertEqual(cmp(result, self.expect_result_out), 0, "result check not pass")


if __name__ == '__main__':
    # run all cases
    unittest.main(verbosity=2)

    # run one case
    # suite = unittest.TestSuite()
    # suite.addTest(TestFusiformSimilarity("test_fusiform_similarity_01"))
    # runner = unittest.TextTestRunner()
    # runner.run(suite)
