#!/usr/bin/env python 
# -*- coding:utf-8 -*-
"""
Copyright (c) 2018 Baidu.com, Inc. All Rights Reserved
__title__ = ''
__author__ = 'tianxiaoyuan'
__mtime__ = '19/10/09'
"""
import json
from IntegrationTest.graphTest.serverTest.common.hugegraph_api.basic_cls import BasicClassMethod


class AlgInterface(BasicClassMethod):
    """
    set algorithm
    """

    def __init__(self):
        self.common_cls = BasicClassMethod()

    def post_countertex(self, body):
        """
        统计顶点信息
        :param data:
        :return:
        """
        url = "/graphs/%s/jobs/algorithm/count_vertex" % self.common_cls.graph
        code, ret = self.common_cls.request(method='post', path=url, body=body)
        return code, ret

    def get_graph_tasks(self, task_id):
        """
        通过任务id获取详情
        :param task_id:
        :return:
        """
        url = "/graphs/%s/tasks/" % self.common_cls.graph + str(task_id)
        code, ret = self.common_cls.request(method='get', path=url)
        return code, ret

    def post_countedge(self, body):
        """
        统计边信息
        :param body:
        :return:
        """
        url = "/graphs/%s/jobs/algorithm/count_edge" % self.common_cls.graph
        code, ret = self.common_cls.request(method='post', path=url, body=body)
        return code, ret

    def post_degree_centrality(self, body):
        """
        度中心性
        :param body:
        :return:
        """
        url = "/graphs/%s/jobs/algorithm/degree_centrality" % self.common_cls.graph
        code, ret = self.common_cls.request(method='post', path=url, body=json.dumps(body))
        return code, ret

    def post_eigenvector_centrality(self, body):
        """
        特征中心性
        :param body:
        :return:
        """
        url = "/graphs/%s/jobs/algorithm/eigenvector_centrality" % self.common_cls.graph
        code, ret = self.common_cls.request(method='post', path=url, body=json.dumps(body))
        return code, ret

    def post_betweeness_centrality(self, body):
        """
        中介中心性
        :param body:
        :return:
        """
        url = "/graphs/%s/jobs/algorithm/betweeness_centrality" % self.common_cls.graph
        code, ret = self.common_cls.request(method='post', path=url, body=json.dumps(body))
        return code, ret

    def post_closeness_centrality(self, body):
        """
        紧密中心性
        :param body:
        :return:
        """
        url = "/graphs/%s/jobs/algorithm/closeness_centrality" % self.common_cls.graph
        code, ret = self.common_cls.request(method='post', path=url, body=json.dumps(body))
        return code, ret

    def post_triangle_count(self, body):
        """
        三角形计数
        :param body:
        :return:
        """
        url = "/graphs/%s/jobs/algorithm/triangle_count" % self.common_cls.graph
        code, ret = self.common_cls.request(method='post', path=url, body=json.dumps(body))
        return code, ret

    def post_cluster_coeffcient(self, body):
        """
        聚类系数
        :param body:
        :return:
        """
        url = "/graphs/%s/jobs/algorithm/cluster_coeffcient" % self.common_cls.graph
        code, ret = self.common_cls.request(method='post', path=url, body=json.dumps(body))
        return code, ret

    def post_lpa(self, body):
        """
        lpa社区发现
        :param body:
        :return:
        """
        url = "/graphs/%s/jobs/algorithm/lpa" % self.common_cls.graph
        code, ret = self.common_cls.request(method='post', path=url, body=json.dumps(body))
        return code, ret

    def post_louvain(self, body):
        """
        louvain社区发现
        :param body:
        :return:
        """
        url = "/graphs/%s/jobs/algorithm/louvain" % self.common_cls.graph
        code, ret = self.common_cls.request(method='post', path=url, body=json.dumps(body))
        return code, ret

    def post_kcore(self, body):
        """
        kcore社区发现
        :param body:
        :return:
        """
        url = "/graphs/%s/jobs/algorithm/k_core" % self.common_cls.graph
        code, ret = self.common_cls.request(method='post', path=url, body=json.dumps(body))
        return code, ret

    def post_fusiform_similarity(self, body):
        """
        模型发现
        :param body:
        :return:
        """
        url = "/graphs/%s/jobs/algorithm/fusiform_similarity" % self.common_cls
        code, ret = self.common_cls.request(method='post', path=url, body=json.dumps(body))
        return code, ret

    def post_rings_detect(self, body):
        """
        环路检测
        :param data:
        :return:
        """
        url = "/graphs/%s/jobs/algorithm/rings_detect" % self.common_cls.graph
        code, ret = self.common_cls.request(method='post', path=url, body=json.dumps(body))
        return code, ret

    def post_gremlin(self, body):
        """
        插入数据
        :param body:
        :return:
        """
        url = "/gremlin"
        code, ret = self.common_cls.request(method='post', path=url, body=json.dumps(body))
        return code, ret

    def post_page_rank(self, body):
        """
        顶点权重rank值
        :param body:
        :return:
        """
        url = "/graphs/%s/jobs/algorithm/page_rank" % self.common_cls.graph
        code, ret = self.common_cls.request(method='post', path=url, body=json.dumps(body))
        return code, ret

    def post_weak_connected_component(self, body):
        """
        顶点进行分类
        :param body:
        :return:
        """
        url = "/graphs/%s/jobs/algorithm/weak_connected_component" % self.common_cls.graph
        code, ret = self.common_cls.request(method='post', path=url, body=json.dumps(body))
        return code, ret
