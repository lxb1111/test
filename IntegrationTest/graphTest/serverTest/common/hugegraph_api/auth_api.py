#!/usr/bin/env python 
# -*- coding:utf-8 -*-
"""
Copyright (c) 2018 Baidu.com, Inc. All Rights Reserved
__title__ = ''
__author__ = 'tianxiaoyuan'
__mtime__ = '20/6/7'

"""
import json
from IntegrationTest.graphTest.serverTest.common.hugegraph_api.basic_cls import BasicClassMethod
import base64


class Auths(BasicClassMethod):
    """
    /graphs/algorithm/...
    """
    def __init__(self):
        self.common_cls = BasicClassMethod()
        self.admin = self.common_cls.admin

    def get_auth(self, auth):
        """获取预期的用户名和密码"""
        auth_base64 = self.admin
        if auth is not None:
            auth_base64 = auth
        return auth_base64

    def get_headers(self, auth):
        """用户名密码base64"""
        user_auth = self.get_auth(auth)
        headers = {}
        for key, value in user_auth.items():
            base64string = base64.encodestring('%s:%s' % (key, value))[:-1]  # 这里最后会自动添加一个\n
            auth_header = "Basic %s" % base64string
            headers["Authorization"] = auth_header
        return headers

    def post_targets(self, body, auth=None):
        """
        创建资源
        :return:
        """
        headers = self.get_headers(auth)
        url = "/graphs/%s/auth/targets" % self.common_cls.graph
        code, ret = self.common_cls.request(method='post', path=url, body=json.dumps(body), headers=headers)
        return code, ret

    def get_targets(self, auth=None):
        """
        查看资源
        :return:
        """
        headers = self.get_headers(auth)
        url = "/graphs/%s/auth/targets" % self.common_cls.graph
        code, ret = self.common_cls.request(method='get', path=url, headers=headers)
        return code, ret

    def delete_targets(self, target_id, auth=None):
        """
        删除资源
        :return:
        """
        headers = self.get_headers(auth)
        url = "/graphs/%s/auth/targets/%s" % (self.common_cls.graph, target_id)
        code, ret = self.common_cls.request(method='delete', path=url, headers=headers)
        return code, ret

    def post_groups(self, body, auth=None):
        """
        创建组
        :return:
        """
        headers = self.get_headers(auth)
        url = "/graphs/%s/auth/groups" % self.common_cls.graph
        code, ret = self.common_cls.request(method='post', path=url, body=json.dumps(body), headers=headers)
        return code, ret

    def get_groups(self, auth=None):
        """
        获取用户组
        :return:
        """
        headers = self.get_headers(auth)
        url = "/graphs/%s/auth/groups" % self.common_cls.graph
        code, ret = self.common_cls.request(method='get', path=url, headers=headers)
        return code, ret

    def delete_groups(self, group_id, auth=None):
        """
        删除用户组
        :return:
        """
        headers = self.get_headers(auth)
        url = "/graphs/%s/auth/groups/%s" % (self.common_cls.graph, group_id)
        code, ret = self.common_cls.request(method='delete', path=url, headers=headers)
        return code, ret

    def post_accesses(self, body, auth=None):
        """
        创建group到target的连接 并给group赋权
        :return:
        """
        headers = self.get_headers(auth)
        url = "/graphs/%s/auth/accesses" % self.common_cls.graph
        code, ret = self.common_cls.request(method='post', path=url, body=json.dumps(body), headers=headers)
        return code, ret

    def get_accesses(self, auth=None):
        """
        创建group到target的连接 并给group赋权
        :return:
        """
        headers = self.get_headers(auth)
        url = "/graphs/%s/auth/accesses" % self.common_cls.graph
        code, ret = self.common_cls.request(method='get', path=url, headers=headers)
        return code, ret

    def delete_accesses(self, access_id, auth=None):
        """
        创建group到target的连接 并给group赋权
        :return:
        """
        headers = self.get_headers(auth)
        url = "/graphs/%s/auth/accesses/%s" % (self.common_cls.graph, access_id)
        code, ret = self.common_cls.request(method='delete', path=url, headers=headers)
        return code, ret

    def post_users(self, body, auth=None):
        """
        创建用户
        :return:
        """
        headers = self.get_headers(auth)
        url = "/graphs/%s/auth/users" % self.common_cls.graph
        code, ret = self.common_cls.request(method='post', path=url, body=json.dumps(body), headers=headers)
        return code, ret

    def post_belongs(self, body, auth=None):
        """
        用户绑定组
        :return:
        """
        headers = self.get_headers(auth)
        url = "/graphs/%s/auth/belongs" % self.common_cls.graph
        code, ret = self.common_cls.request(method='post', path=url, body=json.dumps(body), headers=headers)
        return code, ret

    def get_users_role(self, user_id, auth=None):
        """
        获取用户权限
        :return:
        """
        headers = self.get_headers(auth)
        url = "/graphs/%s/auth/users/%s/role" % (self.common_cls.graph, user_id)
        code, ret = self.common_cls.request(method='get', path=url, headers=headers)
        return code, ret

    def get_graphs(self, auth=None):
        """
        验证:图的读权限
        :return:
        """
        headers = self.get_headers(auth)
        url = "/graphs"
        code, ret = self.common_cls.request(method='get', path=url, headers=headers)
        return code, ret

    def put_graphs_mode(self, body, auth=None):
        """
        验证:图的写权限
        :return:
        """
        headers = self.get_headers(auth)
        url = "/graphs/%s/mode" % self.common_cls.graph
        code, ret = self.common_cls.request(method='put', path=url, body=body, headers=headers)
        return code, ret

    def get_propertykeys(self, auth=None):
        """
        验证:propertykeys读权限
        :return:
        """
        headers = self.get_headers(auth)
        url = "/graphs/%s/schema/propertykeys" % self.common_cls.graph
        code, ret = self.common_cls.request(method='get', path=url, headers=headers)
        return code, ret

    def post_propertykeys(self, body, auth=None):
        """
        验证:propertykeys写权限
        :return:
        """
        headers = self.get_headers(auth)
        url = "/graphs/%s/schema/propertykeys" % self.common_cls.graph
        code, ret = self.common_cls.request(method='post', path=url, body=json.dumps(body), headers=headers)
        return code, ret

    def delete_propertykeys(self, name, auth=None):
        """
        验证:propertykeys删除权限
        :return:
        """
        headers = self.get_headers(auth)
        url = "/graphs/%s/schema/propertykeys/%s" % (self.common_cls.graph, name)
        code, ret = self.common_cls.request(method='delete', path=url, headers=headers)
        return code, ret

    def get_VertexLabel(self, auth=None):
        """
        验证:VertexLabel读权限
        :return:
        """
        headers = self.get_headers(auth)
        url = "/graphs/%s/schema/vertexlabels" % self.common_cls.graph
        code, ret = self.common_cls.request(method='get', path=url, headers=headers)
        return code, ret

    def post_VertexLabel(self, body, auth=None):
        """
        验证:VertexLabel写权限
        :return:
        """
        headers = self.get_headers(auth)
        url = "/graphs/%s/schema/vertexlabels" % self.common_cls.graph
        code, ret = self.common_cls.request(method='post', path=url, body=json.dumps(body), headers=headers)
        return code, ret

    def delete_VertexLabel(self, name, auth=None):
        """
        验证:VertexLabel删除权限
        :return:
        """
        headers = self.get_headers(auth)
        url = "/graphs/%s/schema/vertexlabels/%s" % (self.common_cls.graph, name)
        print ('url === ' + url)
        code, ret = self.common_cls.request(method='delete', path=url, headers=headers)
        return code, ret

    def get_tasks(self, task_id, auth=None):
        """
        通过任务id获取详情
        :return:
        """
        headers = self.get_headers(auth)
        url = "/graphs/%s/tasks/" % self.common_cls.graph + str(task_id)
        code, ret = self.common_cls.request(method='get', path=url, headers=headers)
        return code, ret

    def post_gremlin(self, body, auth=None):
        """
        用户执行gremlin语句
        :return:
        """
        headers = self.get_headers(auth)
        url = "/gremlin"
        code, ret = self.common_cls.request(method='post', path=url, body=json.dumps(body), headers=headers)
        return code, ret

    def get_EdgeLabel(self, auth=None):
        """
        验证:EdgeLabel读权限
        :return:
        """
        headers = self.get_headers(auth)
        url = "/graphs/%s/schema/edgelabels" % self.common_cls.graph
        code, ret = self.common_cls.request(method='get', path=url, headers=headers)
        return code, ret

    def post_EdgeLabel(self, body, auth=None):
        """
        验证:EdgeLabel写权限
        :return:
        """
        headers = self.get_headers(auth)
        url = "/graphs/%s/schema/edgelabels" % self.common_cls.graph
        code, ret = self.common_cls.request(method='post', path=url, body=json.dumps(body), headers=headers)
        return code, ret

    def delete_EdgeLabel(self, name, auth=None):
        """
        验证:edgeLabel删除权限
        :return:
        """
        headers = self.get_headers(auth)
        url = "/graphs/%s/schema/edgelabels/" % self.common_cls.graph + name
        code, ret = self.common_cls.request(method='delete', path=url, headers=headers)
        return code, ret

    def get_IndexLabel(self, auth=None):
        """
        验证:IndexLabel读权限
        :return:
        """
        headers = self.get_headers(auth)
        url = "/graphs/%s/schema/indexlabels" % self.common_cls.graph
        code, ret = self.common_cls.request(method='get', path=url, headers=headers)
        return code, ret

    def post_IndexLabel(self, body, auth=None):
        """
        验证:indexLabel写权限
        :return:
        """
        headers = self.get_headers(auth)
        url = "/graphs/%s/schema/indexlabels" % self.common_cls.graph
        code, ret = self.common_cls.request(method='post', path=url, body=json.dumps(body), headers=headers)
        return code, ret

    def delete_IndexLabel(self, name, auth=None):
        """
        验证:indexLabel删除权限
        :return:
        """
        headers = self.get_headers(auth)
        url = "/graphs/%s/schema/indexlabels/" % self.common_cls.graph + name
        code, ret = self.common_cls.request(method='delete', path=url, headers=headers)
        return code, ret

    def get_vertex(self, v_id, auth=None):
        """
        验证:vertex读权限
        :return:
        """
        headers = self.get_headers(auth)
        url = "/graphs/%s/graph/vertices/%s" % (self.common_cls.graph, v_id)
        print (url)
        code, ret = self.common_cls.request(method='get', path=url, headers=headers)
        return code, ret

    def get_vertex_all(self, vertex_name=None, auth=None):
        """
        验证:点的读取权限
        :return:
        """
        headers = self.get_headers(auth)
        url = "/graphs/%s/graph/vertices" % self.common_cls.graph
        code, ret = self.common_cls.request(method='get', path=url, headers=headers)
        return code, ret

    def post_vertex(self, body, auth=None):
        """
        验证:vertex写权限
        :return:
        """
        headers = self.get_headers(auth)
        url = "/graphs/%s/graph/vertices" % self.common_cls.graph
        print (url)
        code, ret = self.common_cls.request(method='post', path=url, body=json.dumps(body), headers=headers)
        return code, ret

    def delete_vertex(self, vertex_id, auth=None):
        """
        验证:点的删除权限
        :return:
        """
        headers = self.get_headers(auth)
        url = "/graphs/%s/graph/vertices/\"%s\"" % (self.common_cls.graph, vertex_id)
        code, ret = self.common_cls.request(method='delete', path=url, headers=headers)
        return code, ret

    def get_edge(self, e_id, auth=None):
        """
        验证:dege读权限
        :return:
        """
        headers = self.get_headers(auth)
        url = "/graphs/%s/graph/edges/%s" % (self.common_cls.graph, e_id)
        print (url)
        code, ret = self.common_cls.request(method='get', path=url, headers=headers)
        return code, ret

    def get_edge_all(self, vertex_name=None, auth=None):
        """
        验证:所有边的读取权限
        :return:
        """
        headers = self.get_headers(auth)
        url = "/graphs/%s/graph/edges" % self.common_cls.graph
        code, ret = self.common_cls.request(method='get', path=url, headers=headers)
        return code, ret

    def post_edge(self, body, auth=None):
        """
        验证:edge写权限
        :return:
        """
        headers = self.get_headers(auth)
        url = "/graphs/%s/graph/edges" % self.common_cls.graph
        print (url)
        code, ret = self.common_cls.request(method='post', path=url, body=json.dumps(body), headers=headers)
        return code, ret

    def delete_edge(self, v_id, auth=None):
        """
        验证:edge 删除权限
        :return:
        """
        headers = self.get_headers(auth)
        url = "/graphs/%s/graph/edges/%s" % (self.common_cls.graph, v_id)
        print (url)
        code, ret = self.common_cls.request(method='delete', path=url, headers=headers)
        return code, ret

    def get_var(self, auth=None):
        """
        验证:var读权限
        :return:
        """
        headers = self.get_headers(auth)
        url = "/graphs/%s/variables" % self.common_cls.graph
        code, ret = self.common_cls.request(method='get', path=url, headers=headers)
        return code, ret

    def put_var(self, body, name, auth=None):
        """
        验证:var写权限
        :return:
        """
        headers = self.get_headers(auth)
        url = "/graphs/%s/variables/%s" % (self.common_cls.graph, "name")
        code, ret = self.common_cls.request(method='put', path=url, body=json.dumps(body), headers=headers)
        return code, ret

    def delete_var(self, name, auth=None):
        """
        验证:var 删除权限
        :return:
        """
        headers = self.get_headers(auth)
        url = "/graphs/%s/variables/%s" % (self.common_cls.graph, name)
        code, ret = self.common_cls.request(method='delete', path=url, headers=headers)
        return code, ret

    def get_task(self, task_id, auth=None):
        """
        验证:task读权限
        :return:
        """
        headers = self.get_headers(auth)
        url = "/graphs/%s/tasks/%s" % (self.common_cls.graph, task_id)
        code, ret = self.common_cls.request(method='get', path=url, headers=headers)
        return code, ret

    def get_task_all(self, auth=None):
        """
        查询所有任务
        :return:
        """
        headers = self.get_headers(auth)
        url = "/graphs/%s/tasks" % self.common_cls.graph
        code, ret = self.common_cls.request(method='get', path=url, headers=headers)
        return code, ret

    def put_task(self, task_id, auth=None):
        """
        验证:task写权限 (取消task)
        :return:
        """
        headers = self.get_headers(auth)
        url = "/graphs/%s/tasks/%s?action=cancel" % (self.common_cls.graph, task_id)
        code, ret = self.common_cls.request(method='put', path=url, headers=headers)
        return code, ret

    def delete_task(self, task_id, auth=None):
        """
        验证:task 删除权限
        :return:
        """
        headers = self.get_headers(auth)
        url = "/graphs/%s/tasks/%s" % (self.common_cls.graph, task_id)
        code, ret = self.common_cls.request(method='delete', path=url, headers=headers)
        return code, ret

    def post_gremlin_task(self, query, auth=None):
        """
        创建gremlin 查询任务
        :return:
        """
        headers = self.get_headers(auth)
        body_json = {
            "gremlin": query,
            "bindings": {},
            "language": "gremlin-groovy",
            "aliases": {}
        }
        url = "/graphs/%s/jobs/gremlin" % self.common_cls.graph
        code, ret = self.common_cls.request(method='post', path=url, body=json.dumps(body_json), headers=headers)
        return code, ret

    def get_users(self, auth=None):
        """
        验证:查看用户列表
        :return:
        """
        headers = self.get_headers(auth)
        url = "/graphs/%s/auth/users" % self.common_cls.graph
        code, ret = self.common_cls.request(method='get', path=url, headers=headers)
        return code, ret

    def get_edge_all_01(self, auth, id):
        """
        :param auth:
        :param id:
        """
        pass

    def get_edge_allLabel(self, auth=None):
        """
        :param auth:
        :param id:
        """
        pass

    def post_job_gremlin(self, body, auth=None):
        """

        :param body:
        :param auth:
        """
        pass