# -*- coding:utf-8 -*-
"""
author     : lxb
note       : 粗粒度权限的鉴权和越权
create_time: 2020/4/22 5:17 下午
"""
import sys
import os
import unittest
import time
import importlib

sys.path.append('%s/..' % os.path.split(os.path.realpath(__file__))[0])
sys.path.append('../../')
importlib.reload(sys)

from IntegrationTest.graphTest.serverTest.common.hugegraph_api.auth_api import Auths
from IntegrationTest.graphTest.serverTest.testCase.auth import set_auth
from IntegrationTest.graphTest.serverTest.common.config.produce_data import ProduceData
from IntegrationTest.graphTest.serverTest.common.hugegraph_api.basic_cls import BasicClassMethod

TYPE = "basic"


class TestCommonAuth(unittest.TestCase):
    """
    粗粒度权限验证：创建用户并对用户进行鉴权和越权验证
    """

    def setUp(self):
        """
        每条case的前提条件
        :return:
        """
        self.auth = Auths()
        self.p = ProduceData()
        self.graph = BasicClassMethod().graph
        self.host = BasicClassMethod().host
        self.port = BasicClassMethod().port
        self.user = {"graphTest": "123456"}
        # 清空图数据，只保留超管权限
        self.p.init_data("clear")

    def test_status_read_01(self):
        """
        资源读权限
        :return:
        """
        permission_list = [
            {"target_list": [{"type": "STATUS"}], "permission": "READ", "name": "status_read"}
        ]
        user_id = set_auth.post_auth(permission_list)

        # check auth
        code, ret = self.auth.get_users_role(user_id)
        for key, value in ret["roles"][self.graph].items():
            self.assertEqual(key, "READ", msg="role permission check fail")
            self.assertEqual(value[0]["type"], "STATUS", msg="role type check fail")

        # check Authorize
        code, ret = self.auth.get_graphs(auth=self.user)
        self.assertEqual(code, 200, msg="Authorize code check fail")
        self.assertEqual(ret["graphs"][0], self.graph, msg="Authorize result check fail")

        # check Unauthorized"
        body = "RESTORING"
        code, ret = self.auth.put_graphs_mode(body, auth=self.user)
        self.assertNotEqual(code, 200, msg="Unauthorized code check fail")

    def test_status_write_02(self):
        """
        资源写权限 === 越权验证失败，此处有bug-常帅跟踪
        :return:
        """
        permission_list = [
            {"target_list": [{"type": "STATUS"}], "permission": "WRITE", "name": "status_write"}
        ]
        user_id = set_auth.post_auth(permission_list)

        # check role
        code, ret = self.auth.get_users_role(user_id)
        for key, value in ret["roles"][self.graph].items():
            self.assertEqual(key, "WRITE", msg="role permission check fail")
            self.assertEqual(value[0]["type"], "STATUS", msg="role type check fail")

        # check Authorize - 该接口只有管理员有权限，普通用户即使赋予了status资源写权限也返回403，符合预期

        body = "RESTORING"
        code, ret = self.auth.put_graphs_mode(body, auth=self.user)
        self.assertNotEqual(code, 200, msg="Unauthorized code check fail")

        # check Unauthorized
        code, ret = self.auth.get_graphs(auth=self.user)
        self.assertNotEqual(code, 200, msg="Authorize code check fail")  # 越权验证失败，此处有bug-常帅跟踪

    def test_propertyKey_read_03(self):
        """
        property_key读权限 === 越权验证失败有 bug
        :return:
        """
        # add graph
        self.p.init_data("basic")
        # check role
        permission_list = [
            {"target_list": [{"type": "PROPERTY_KEY"}], "permission": "READ", "name": "propertyKey_read"}
        ]
        user_id = set_auth.post_auth(permission_list)

        code, ret = self.auth.get_users_role(user_id)
        for key, value in ret["roles"][self.graph].items():
            self.assertEqual(key, "READ", msg="role permission check fail")
            self.assertEqual(value[0]["type"], "PROPERTY_KEY", msg="role type check fail")

        # check Authorize
        code, ret = self.auth.get_propertykeys(auth=self.user)
        self.assertEqual(code, 200, msg="Authorize code check fail")

        # check Unauthorized--write
        body = {
            "name": "test_name",
            "data_type": "INT",
            "cardinality": "SINGLE"
        }
        code, ret = self.auth.post_propertykeys(body, auth=self.user)
        self.assertNotEqual(code, 200, msg="Unauthorized code check fail")
        self.assertEqual(ret["message"], "User not authorized.", msg="Unauthorized result check fail")

        # check Unauthorized--delete
        name = "test_name"
        code, ret = self.auth.delete_propertykeys(name, auth=self.user)
        self.assertNotEqual(code, 200, msg="Unauthorized code check fail")
        self.assertEqual(ret["message"], "User not authorized.", msg="Unauthorized result check fail")

    def test_propertyKey_write_04(self):
        """
        property_key写权限
        :return:
        """
        permission_list = [
            {"target_list": [{"type": "PROPERTY_KEY"}], "permission": "WRITE", "name": "propertyKey_write"}
        ]
        user_id = set_auth.post_auth(permission_list)

        # check role
        code, ret = self.auth.get_users_role(user_id)
        for key, value in ret["roles"][self.graph].items():
            self.assertEqual(key, "WRITE", msg="role permission check fail")
            self.assertEqual(value[0]["type"], "PROPERTY_KEY", msg="role type check fail")

        # check Authorize
        body = {
            "name": "test_name",
            "data_type": "INT",
            "cardinality": "SINGLE"
        }
        code, ret = self.auth.post_propertykeys(body, auth=self.user)
        self.assertEqual(code, 201, msg="Unauthorized code check fail")
        self.assertEqual(ret["name"], body["name"], msg="Unauthorized result check fail")

        # check Unauthorized--read
        code, ret = self.auth.get_propertykeys(auth=self.user)
        self.assertNotEqual(code, 200, msg="Authorize code check fail")
        self.assertEqual(ret["message"], "User not authorized.", msg="Unauthorized result check fail")

        # check Unauthorized--delete
        name = "age"
        code, ret = self.auth.delete_propertykeys(name, auth=self.user)
        self.assertNotEqual(code, 200, msg="Unauthorized code check fail")
        self.assertEqual(ret["message"], "User not authorized.", msg="Unauthorized result check fail")

    def test_propertyKey_delete_05(self):
        """
        property_key删权限
        :return:
        """
        # add graph_propertyKey
        body = {
            "name": "test_name",
            "data_type": "INT",
            "cardinality": "SINGLE"
        }
        code, ret = self.auth.post_propertykeys(body, auth={"admin": "123456"})

        # check role
        permission_list = [
            {"target_list": [{"type": "PROPERTY_KEY"}], "permission": "DELETE", "name": "propertyKey_delete"}
        ]
        user_id = set_auth.post_auth(permission_list)
        code, ret = self.auth.get_users_role(user_id)
        for key, value in ret["roles"][self.graph].items():
            self.assertEqual(key, "DELETE", msg="role permission check fail")
            self.assertEqual(value[0]["type"], "PROPERTY_KEY", msg="role type check fail")

        # check Authorize--delete
        name = "test_name"
        code, ret = self.auth.delete_propertykeys(name, auth=self.user)
        self.assertEqual(code, 204, msg="Unauthorized code check fail")

        # check Unauthorized--read
        code, ret = self.auth.get_propertykeys(auth=self.user)
        self.assertNotEqual(code, 200, msg="Authorize code check fail")
        self.assertEqual(ret["message"], "User not authorized.", msg="Unauthorized result check fail")

        # check Unauthorized--write
        body = {
            "name": "test_name",
            "data_type": "INT",
            "cardinality": "SINGLE"
        }
        code, ret = self.auth.post_propertykeys(body, auth=self.user)
        self.assertNotEqual(code, 201, msg="Unauthorized code check fail")
        self.assertEqual(ret["message"], "User not authorized.", msg="Unauthorized result check fail")

    # @unittest.skip("skip")
    def test_vertexLabel_read_06(self):
        """
        vertex_label读权限
        :return:
        """
        # add graph
        self.p.init_data("basic")

        # check role
        permission_list = [
            {"target_list": [{"type": "PROPERTY_KEY"}, {"type": "VERTEX_LABEL"}],
             "permission": "READ",
             "name": "vertex_label_read"}
        ]
        user_id = set_auth.post_auth(permission_list)
        code, ret = self.auth.get_users_role(user_id)
        print (ret)
        for key, value in ret["roles"][self.graph].items():
            self.assertEqual(key, "READ", msg="role permission check fail")
            self.assertEqual(value[1]["type"], "VERTEX_LABEL", msg="role type check fail")

        # check Authorize--read
        code, ret = self.auth.get_VertexLabel(auth=self.user)
        self.assertEqual(code, 200, msg="Authorize code check fail")

        # check Unauthorized--write
        body = {
            "name": "test_name",
            "id_strategy": "DEFAULT",
            "properties": ["name", "age"],
            "primary_keys": ["name"],
            "nullable_keys": [],
            "enable_label_index": True
        }
        code, ret = self.auth.post_VertexLabel(body, auth=self.user)
        self.assertNotEqual(code, 201, msg="Unauthorized code check fail")
        self.assertEqual(ret["message"], "User not authorized.", msg="Unauthorized result check fail")

        # check Unauthorized--delete
        name = "person2"
        code, ret = self.auth.delete_VertexLabel(name, auth=self.user)
        self.assertNotEqual(code, 201, msg="Unauthorized code check fail")
        self.assertEqual(ret["message"], "User not authorized.", msg="Unauthorized result check fail")

    def test_vertexLabel_write_07(self):
        """
        vertex_label写权限
        :return:
        """
        # add graph
        self.p.init_data("basic")

        # check role
        permission_list = [
            {"target_list": [{"type": "PROPERTY_KEY"}], "permission": "READ", "name": "propertyKey_read"},
            {"target_list": [{"type": "VERTEX_LABEL"}], "permission": "WRITE", "name": "vertexLabel_write"}
        ]
        user_id = set_auth.post_auth(permission_list)
        code1, ret1 = self.auth.get_users_role(user_id)

        for key, value in ret1["roles"][self.graph].items():
            if key == "WRITE":
                self.assertIn(value[0]["type"], "VERTEX_LABEL", msg="role type check fail")
            elif key == "READ":
                self.assertIn(value[0]["type"], "PROPERTY_KEY", msg="role type check fail")

        # check Authorize
        body = {
            "name": "test_name",
            "id_strategy": "DEFAULT",
            "properties": ["name", "age"],
            "primary_keys": ["name"],
            "nullable_keys": [],
            "enable_label_index": True
        }
        code2, ret2 = self.auth.post_VertexLabel(body, auth=self.user)
        self.assertEqual(code2, 201, msg="Unauthorized code check fail")

        # check Unauthorized--READ
        code3, ret3 = self.auth.get_VertexLabel(auth=self.user)
        self.assertEqual(code3, 200, msg="UnAuthorized code check fail")
        self.assertEqual(ret3["vertexlabels"], [], msg="UnAuthorized result check fail")

        # check Unauthorized--DELETE
        name = "person2"
        code4, ret4 = self.auth.delete_VertexLabel(name, auth=self.user)
        self.assertNotEqual(code4, 201, msg="Unauthorized code check fail")
        self.assertEqual(ret4["message"], "User not authorized.", msg="Unauthorized result check fail")

    def test_vertexLabel_delete_08(self):
        """
        vertex_label删权限
        :return:
        """
        # add graph
        self.p.init_data("basic")
        # add vertexlabel
        body = {
            "name": "graphTest",
            "properties": ["name", "age"],
            "primary_keys": ["name"],
            "enable_label_index": False
        }
        self.auth.post_VertexLabel(body, auth={"admin": "123456"})

        # check role
        permission_list = [
            {"target_list": [{"type": "VERTEX_LABEL"}], "permission": "DELETE", "name": "vertexLabel_delete"},
            {"target_list": [{"type": "TASK"}], "permission": "WRITE", "name": "task_write"},
            {"target_list": [{"type": "TASK"}], "permission": "READ", "name": "task_read"},
            {"target_list": [{"type": "TASK"}], "permission": "EXECUTE", "name": "task_execute"}
        ]
        user_id = set_auth.post_auth(permission_list)
        code, ret = self.auth.get_users_role(user_id)
        for key, value in ret["roles"][self.graph].items():
            if key == "DELETE":
                self.assertIn(value[0]["type"], "VERTEX_LABEL", msg="role type check fail")
            elif key == "WRITE":
                self.assertIn(value[0]["type"], "TASK", msg="role type check fail")
            else:
                pass

        # check Authorize
        name = "graphTest"
        code, ret = self.auth.delete_VertexLabel(name, auth=self.user)
        print (ret)
        self.assertEqual(code, 202, msg="Unauthorized code check fail")
        id = ret["task_id"]
        time.sleep(10)  # 延迟10s
        code, ret = self.auth.get_tasks(id, {"admin": "123456"})
        print (code)
        print (ret)
        self.assertEqual(ret["task_status"], "success",
                         msg="Authorize result check fail")  # 通过接口访问返回fail，但是在界面操作是没问题的，需要追下原因--具体情况常帅知道

        # check Unauthorized--READ
        code, ret = self.auth.get_VertexLabel(auth=self.user)
        self.assertEqual(code, 200, msg="UnAuthorized code check fail")
        self.assertEqual(ret["vertexlabels"], [], msg="UnAuthorized result check fail")

        # check Unauthorized--WRITE
        code, ret = self.auth.post_VertexLabel(body, auth=self.user)
        self.assertEqual(code, 403, msg="Unauthorized code check fail")

    def test_edgeLabel_read_09(self):
        """
        edge_label读权限
        :return:
        """
        # add graph
        self.p.init_data("basic")

        # check role
        permission_list = [
            {
                "target_list": [{"type": "PROPERTY_KEY"}, {"type": "VERTEX_LABEL"}, {"type": "EDGE_LABEL"}],
                "permission": "READ",
                "name": "propertyKey_read"
            }
        ]
        user_id = set_auth.post_auth(permission_list)
        code, ret = self.auth.get_users_role(user_id)
        for key, value in ret["roles"][self.graph].items():
            self.assertEqual(key, "READ", msg="role permission check fail")
            self.assertEqual(value[2]["type"], "EDGE_LABEL", msg="role type check fail")

        # check Authorize--read
        code, ret = self.auth.get_EdgeLabel(auth=self.user)
        self.assertEqual(code, 200, msg="Authorize code check fail")

        # check Unauthorized--write
        body = {
            "name": "test_name",
            "source_label": "person",
            "target_label": "software",
            "frequency": "SINGLE",
            "properties": []
        }
        code, ret = self.auth.post_EdgeLabel(body, auth=self.user)
        self.assertNotEqual(code, 201, msg="Unauthorized code check fail")
        self.assertEqual(ret["message"], "User not authorized.", msg="Unauthorized result check fail")

        # check Unauthorized--delete
        name = "person2"
        code, ret = self.auth.delete_EdgeLabel(name, auth=self.user)
        self.assertNotEqual(code, 201, msg="Unauthorized code check fail")
        self.assertEqual(ret["message"], "User not authorized.", msg="Unauthorized result check fail")

    def test_edgeLabel_write_10(self):
        """
        edge_label写权限
        :return:
        """
        # add graph
        self.p.init_data("basic")

        # check role
        permission_list = [
            {"target_list": [{"type": "PROPERTY_KEY"}, {"type": "VERTEX_LABEL"}],
             "permission": "READ", "name": "propertyKey_read"},
            {"target_list": [{"type": "EDGE_LABEL"}], "permission": "WRITE", "name": "edgeLabel_write"}
        ]
        user_id = set_auth.post_auth(permission_list)
        code, ret = self.auth.get_users_role(user_id)

        for key, value in ret["roles"][self.graph].items():
            if key == "WRITE":
                self.assertIn(value[0]["type"], "EDGE_LABEL", msg="role type check fail")
            elif key == "READ":
                self.assertIn(value[0]["type"], "PROPERTY_KEY", msg="role type check fail")

        # check Authorize
        body = {
            "name": "test_name",
            "source_label": "person",
            "target_label": "software",
            "frequency": "SINGLE",
            "properties": []
        }
        code, ret = self.auth.post_EdgeLabel(body, auth=self.user)
        self.assertEqual(code, 201, msg="Unauthorized code check fail")

        # check Unauthorized--READ
        code, ret = self.auth.get_EdgeLabel(auth=self.user)
        print (code)
        print (ret)
        self.assertEqual(code, 200, msg="UnAuthorized code check fail")
        self.assertEqual(ret["edgelabels"], [], msg="UnAuthorized result check fail")

        # check Unauthorized--DELETE
        name = "person2"
        code, ret = self.auth.delete_EdgeLabel(name, auth=self.user)
        self.assertNotEqual(code, 201, msg="Unauthorized code check fail")
        self.assertEqual(ret["message"], "User not authorized.", msg="Unauthorized result check fail")

    def test_edgeLabel_delete_11(self):
        """
        vertex_label删权限
        :return:
        """
        # add graph
        self.p.init_data("basic")
        # add edgelabel
        body = {
            "name": "test_name",
            "source_label": "person",
            "target_label": "software",
            "frequency": "SINGLE",
            "properties": [],
            "enable_label_index": False
        }
        self.auth.post_EdgeLabel(body, auth={"admin": "123456"})

        # check role
        permission_list = [
            {"target_list": [{"type": "EDGE_LABEL"}], "permission": "DELETE", "name": "edgeLabel_delete"},
            {"target_list": [{"type": "TASK"}], "permission": "WRITE", "name": "task_write"},
            {"target_list": [{"type": "TASK"}], "permission": "READ", "name": "task_read"},
            {"target_list": [{"type": "TASK"}], "permission": "EXECUTE", "name": "task_execute"}
        ]
        user_id = set_auth.post_auth(permission_list)
        code, ret = self.auth.get_users_role(user_id)
        for key, value in ret["roles"][self.graph].items():
            if key == "DELETE":
                self.assertIn(value[0]["type"], "EDGE_LABEL", msg="role type check fail")
            elif key == "WRITE":
                self.assertIn(value[0]["type"], "TASK", msg="role type check fail")
            else:
                pass

        # check Authorize
        name = "test_name"
        code, ret = self.auth.delete_EdgeLabel(name, auth=self.user)
        print (ret)
        self.assertEqual(code, 202, msg="Unauthorized code check fail")
        id = ret["task_id"]
        time.sleep(10)  # 延迟10s
        code, ret = self.auth.get_tasks(id, {"admin": "123456"})
        print (code)
        print (ret)
        self.assertEqual(ret["task_status"], "success",
                         msg="Authorize result check fail")  # 通过接口访问返回fail，但是在界面操作是没问题的，需要追下原因--具体情况常帅知道

        # check Unauthorized--READ
        code, ret = self.auth.get_EdgeLabel(auth=self.user)
        self.assertEqual(code, 200, msg="UnAuthorized code check fail")
        self.assertEqual(ret["edgelabels"], [], msg="UnAuthorized result check fail")

        # check Unauthorized--WRITE
        code, ret = self.auth.post_EdgeLabel(body, auth=self.user)
        self.assertEqual(code, 403, msg="Unauthorized code check fail")

    def test_indexLabel_vertex_read_12(self):
        """
        index_label 读权限
        :return:
        """
        # add schema_indexLabel
        self.p.init_data("schema_indexLabel")

        # check role
        permission_list = [
            {
                "target_list": [{"type": "PROPERTY_KEY"}, {"type": "VERTEX_LABEL"}, {"type": "INDEX_LABEL"}],
                "permission": "READ",
                "name": "indexLabel_read"
            }
        ]
        user_id = set_auth.post_auth(permission_list)
        code, ret = self.auth.get_users_role(user_id)
        for key, value in ret["roles"][self.graph].items():
            if key == "READ":
                self.assertIn(value[2]["type"], "INDEX_LABEL", msg="role type check fail")
            else:
                pass

        # check Authorize--read
        code, ret = self.auth.get_IndexLabel(auth=self.user)
        self.assertEqual(code, 200, msg="Authorize code check fail")

        # check Unauthorized--write
        body = {
            "name": "personByCity",
            "base_type": "VERTEX_LABEL",
            "base_value": "person",
            "index_type": "SECONDARY",
            "fields": [
                "city"
            ]
        }
        code, ret = self.auth.post_IndexLabel(body, auth=self.user)
        self.assertNotEqual(code, 201, msg="Unauthorized code check fail")
        self.assertEqual(ret["message"], "User not authorized.", msg="Unauthorized result check fail")

        # check Unauthorized--delete
        name = "personByCity"
        code, ret = self.auth.delete_IndexLabel(name, auth=self.user)
        self.assertNotEqual(code, 201, msg="Unauthorized code check fail")
        self.assertEqual(ret["message"], "User not authorized.", msg="Unauthorized result check fail")

    def test_indexLabel_vertex_write_13(self):
        """
        index_label写权限
        :return:
        """
        # add graph
        self.p.init_data("schema_indexLabel")

        # check role
        permission_list = [
            {"target_list": [{"type": "PROPERTY_KEY"}, {"type": "VERTEX_LABEL"}, {"type": "INDEX_LABEL"}],
             "permission": "READ", "name": "propertyKey_read"},
            {"target_list": [{"type": "INDEX_LABEL"}, {"type": "TASK"}],
             "permission": "WRITE", "name": "indexLabel_write"},
            {"target_list": [{"type": "TASK"}], "permission": "EXECUTE", "name": "task_execute"}
        ]
        user_id = set_auth.post_auth(permission_list)
        code, ret = self.auth.get_users_role(user_id)

        for key, value in ret["roles"][self.graph].items():
            if key == "WRITE":
                self.assertIn(value[0]["type"], "INDEX_LABEL", msg="role type check fail")
            elif key == "READ":
                self.assertIn(value[0]["type"], "PROPERTY_KEY", msg="role type check fail")

        # check Authorize
        body = {
            "name": "personByCity",
            "base_type": "VERTEX_LABEL",
            "base_value": "person",
            "index_type": "SECONDARY",
            "fields": [
                "city"
            ]
        }
        code, ret = self.auth.post_IndexLabel(body, auth=self.user)
        print (code)
        print (ret)
        self.assertEqual(code, 202, msg="Unauthorized code check fail")

        # check Unauthorized--READ
        code, ret = self.auth.get_IndexLabel(auth=self.user)
        print (code)
        print (ret)
        self.assertEqual(code, 200, msg="UnAuthorized code check fail")
        # index_label是写有问题的，具有读的权限
        # self.assertEqual(ret["indexlabels"], [], msg="UnAuthorized result check fail")

        # check Unauthorized--DELETE
        name = "personByAge"
        code, ret = self.auth.delete_IndexLabel(name, auth=self.user)
        self.assertNotEqual(code, 202, msg="Unauthorized code check fail")
        self.assertEqual(ret["message"], "User not authorized.", msg="Unauthorized result check fail")

    def test_indexLabel_vertex_delete_14(self):
        """
        index_label删权限
        :return:
        """
        # add graph_indexLabel
        self.p.init_data("schema_indexLabel")

        # check role
        permission_list = [
            {"target_list": [{"type": "INDEX_LABEL"}], "permission": "DELETE", "name": "indexLabel_delete"},
            {"target_list": [{"type": "TASK"}], "permission": "WRITE", "name": "task_write"},
            {"target_list": [{"type": "TASK"}], "permission": "READ", "name": "task_read"},
            {"target_list": [{"type": "TASK"}], "permission": "EXECUTE", "name": "task_execute"}
        ]
        user_id = set_auth.post_auth(permission_list)
        code, ret = self.auth.get_users_role(user_id)
        for key, value in ret["roles"][self.graph].items():
            if key == "DELETE":
                self.assertIn(value[0]["type"], "INDEX_LABEL", msg="role type check fail")
            elif key == "WRITE":
                self.assertIn(value[0]["type"], "TASK", msg="role type check fail")
            else:
                pass

        # check Authorize
        name = "personByAge"
        code, ret = self.auth.delete_IndexLabel(name, auth=self.user)
        print (ret)
        self.assertEqual(code, 202, msg="Unauthorized code check fail")
        id = ret["task_id"]
        time.sleep(10)  # 延迟10s
        code, ret = self.auth.get_tasks(id, {"admin": "123456"})
        print (code)
        print (ret)
        self.assertEqual(ret["task_status"], "success",
                         msg="Authorize result check fail")  # 通过接口访问返回fail，但是在界面操作是没问题的，需要追下原因--具体情况常帅知道

        # check Unauthorized--READ
        code, ret = self.auth.get_IndexLabel(auth=self.user)
        self.assertEqual(code, 200, msg="UnAuthorized code check fail")
        self.assertEqual(ret["indexlabels"], [], msg="UnAuthorized result check fail")

        # check Unauthorized--WRITE
        body = {
            "name": "personByCity",
            "base_type": "VERTEX_LABEL",
            "base_value": "person",
            "index_type": "SECONDARY",
            "fields": [
                "city"
            ]
        }
        code, ret = self.auth.post_IndexLabel(body, auth=self.user)
        self.assertEqual(code, 403, msg="Unauthorized code check fail")

    def test_indexLabel_edge_read_15(self):
        """
        edge_index_label 读权限
        :return:
        """
        # add schema_indexLabel
        self.p.init_data("schema_indexLabel")

        # check role
        permission_list = [
            {
                "target_list": [
                    {"type": "PROPERTY_KEY"},
                    {"type": "EDGE_LABEL"},
                    {"type": "INDEX_LABEL"},
                    {"type": "VERTEX_LABEL"}
                ],
                "permission": "READ",
                "name": "indexLabel_read"
            }
        ]
        user_id = set_auth.post_auth(permission_list)
        code, ret = self.auth.get_users_role(user_id)
        for key, value in ret["roles"][self.graph].items():
            if key == "READ":
                self.assertIn(value[2]["type"], "INDEX_LABEL", msg="role type check fail")
            else:
                pass

        # check Authorize--read
        code, ret = self.auth.get_IndexLabel(auth=self.user)
        print (code)
        print (ret)
        self.assertEqual(code, 200, msg="Authorize code check fail")

        # check Unauthorized--write
        body = {
            "name": "createdByCity",
            "base_type": "EDGE_LABEL",
            "base_value": "created",
            "index_type": "SECONDARY",
            "fields": [
                "city"
            ]
        }
        code, ret = self.auth.post_IndexLabel(body, auth=self.user)
        self.assertNotEqual(code, 201, msg="Unauthorized code check fail")
        self.assertEqual(ret["message"], "User not authorized.", msg="Unauthorized result check fail")

        # check Unauthorized--delete
        name = "createdByCity"
        code, ret = self.auth.delete_IndexLabel(name, auth=self.user)
        self.assertNotEqual(code, 202, msg="Unauthorized code check fail")
        self.assertEqual(ret["message"], "User not authorized.", msg="Unauthorized result check fail")

    def test_indexLabel_edge_write_16(self):
        """
        index_label写权限
        :return:
        """
        # add graph
        self.p.init_data("schema_indexLabel")

        # check role
        permission_list = [
            {"target_list": [{"type": "PROPERTY_KEY"}, {"type": "VERTEX_LABEL"}, {"type": "EDGE_LABEL"}],
             "permission": "READ", "name": "propertyKey_read"},
            {"target_list": [{"type": "INDEX_LABEL"}, {"type": "TASK"}],
             "permission": "WRITE", "name": "indexLabel_write"},
            {"target_list": [{"type": "TASK"}], "permission": "EXECUTE", "name": "task_execute"}
        ]
        user_id = set_auth.post_auth(permission_list)
        code, ret = self.auth.get_users_role(user_id)

        for key, value in ret["roles"][self.graph].items():
            if key == "WRITE":
                self.assertIn(value[0]["type"], "INDEX_LABEL", msg="role type check fail")
            elif key == "EXECUTE":
                self.assertIn(value[0]["type"], "TASK", msg="role type check fail")

        # check Authorize
        body = {
            "name": "createdByCity",
            "base_type": "EDGE_LABEL",
            "base_value": "created",
            "index_type": "SECONDARY",
            "fields": [
                "city"
            ]
        }
        code, ret = self.auth.post_IndexLabel(body, auth=self.user)
        print(code)
        print(ret)
        self.assertEqual(code, 202, msg="Unauthorized code check fail")

        # check Unauthorized--READ
        code, ret = self.auth.get_IndexLabel(auth=self.user)
        print(code)
        print(ret)
        self.assertEqual(code, 200, msg="UnAuthorized code check fail")
        # index_label是写有问题的，具有读的权限
        # self.assertEqual(ret["indexlabels"], [], msg="UnAuthorized result check fail")

        # check Unauthorized--DELETE
        name = "createdByCity"
        code, ret = self.auth.delete_IndexLabel(name, auth=self.user)
        print(code)
        print(ret)
        self.assertNotEqual(code, 202, msg="Unauthorized code check fail")
        self.assertEqual(ret["message"], "User not authorized.", msg="Unauthorized result check fail")

    def test_indexLabel_edge_delete_17(self):
        """
        index_label删权限
        :return:
        """
        # add graph_indexLabel
        self.p.init_data("schema_indexLabel")

        # check role
        permission_list = [
            {"target_list": [{"type": "INDEX_LABEL"}], "permission": "DELETE", "name": "indexLabel_delete"},
            {"target_list": [{"type": "TASK"}], "permission": "WRITE", "name": "task_write"},
            {"target_list": [{"type": "TASK"}], "permission": "READ", "name": "task_read"},
            {"target_list": [{"type": "TASK"}], "permission": "EXECUTE", "name": "task_execute"}
        ]
        user_id = set_auth.post_auth(permission_list)
        code, ret = self.auth.get_users_role(user_id)
        for key, value in ret["roles"][self.graph].items():
            if key == "DELETE":
                self.assertIn(value[0]["type"], "INDEX_LABEL", msg="role type check fail")
            elif key == "WRITE":
                self.assertIn(value[0]["type"], "TASK", msg="role type check fail")
            else:
                pass

        # check Authorize
        name = "knowsByDate"
        code, ret = self.auth.delete_IndexLabel(name, auth=self.user)
        print(ret)
        self.assertEqual(code, 202, msg="Unauthorized code check fail")
        id = ret["task_id"]
        time.sleep(10)  # 延迟10s
        code, ret = self.auth.get_tasks(id, {"admin": "123456"})
        print(code)
        print(ret)
        self.assertEqual(ret["task_status"], "success",
                         msg="Authorize result check fail")  # 通过接口访问返回fail，但是在界面操作是没问题的，需要追下原因--具体情况常帅知道

        # check Unauthorized--READ
        code, ret = self.auth.get_IndexLabel(auth=self.user)
        self.assertEqual(code, 200, msg="UnAuthorized code check fail")
        self.assertEqual(ret["indexlabels"], [], msg="UnAuthorized result check fail")

        # check Unauthorized--WRITE
        body = {
            "name": "createdByCity",
            "base_type": "EDGE_LABEL",
            "base_value": "created",
            "index_type": "SECONDARY",
            "fields": [
                "city"
            ]
        }
        code, ret = self.auth.post_IndexLabel(body, auth=self.user)
        self.assertEqual(code, 403, msg="Unauthorized code check fail")

    def test_vertex_aggr_read_18(self):
        """
        vertex_arrg 读权限
        :return:
        """
        # add schema_indexLabel
        self.p.init_data("basic")

        # check role
        permission_list = [
            {
                "target_list": [
                    {"type": "VERTEX_AGGR"}
                ],
                "permission": "READ",
                "name": "vertexAggr_read"
            },
            {
                "target_list": [
                    {"type": "GREMLIN"}
                ],
                "permission": "EXECUTE",
                "name": "gremlin_execute"
            }
        ]
        user_id = set_auth.post_auth(permission_list)
        code, ret = self.auth.get_users_role(user_id)
        print(code)
        print(ret)
        for key, value in ret["roles"][self.graph].items():
            if key == "READ":
                self.assertIn(value[0]["type"], "VERTEX_AGGR", msg="role type check fail")
            else:
                pass

        # check Authorize--read
        body = {
            "gremlin": "g.V().count()",
            "bindings": {},
            "language": "gremlin-groovy",
            "aliases": {"graph": "%s" % self.graph, "g": "__g_%s" % self.graph}
        }
        code, ret = self.auth.post_gremlin(body, auth=self.user)
        print (code)
        print (ret)
        self.assertEqual(code, 200, msg="Authorize code check fail")

        # check UNAuthorize--read
        body = {
            "gremlin": "g.V().count()",
            "bindings": {},
            "language": "gremlin-groovy",
            "aliases": {"graph": "%s" % self.graph, "g": "__g_%s" % self.graph}
        }
        code, ret = self.auth.post_gremlin(body, auth=self.user)
        print(code)
        print(ret)
        self.assertNotEqual(code, 200, msg="Unauthorize code check fail")

    def test_edge_aggr_read_19(self):
        """
        edge_aggr 读权限
        :return:
        """
        # add schema_indexLabel
        self.p.init_data("basic")

        # check role
        permission_list = [
            {
                "target_list": [
                    {"type": "EDGE_AGGR"}
                ],
                "permission": "READ",
                "name": "edgeAggr_read"
            },
            {
                "target_list": [
                    {"type": "GREMLIN"}
                ],
                "permission": "EXECUTE",
                "name": "gremlin_execute"
            }
        ]
        user_id = set_auth.post_auth(permission_list)
        code, ret = self.auth.get_users_role(user_id)
        print(code)
        print(ret)
        for key, value in ret["roles"][self.graph].items():
            if key == "READ":
                self.assertIn(value[0]["type"], "EDGE_AGGR", msg="role type check fail")
            else:
                pass

        # check Authorize--read
        body = {
            "gremlin": "g.E().count()",
            "bindings": {},
            "language": "gremlin-groovy",
            "aliases": {"graph": "%s" % self.graph, "g": "__g_%s" % self.graph}
        }
        code, ret = self.auth.post_gremlin(body, auth=self.user)
        print(code)
        print(ret)
        self.assertEqual(code, 200, msg="Authorize code check fail")

        # check unAuthorize--read
        body = {
            "gremlin": "g.V().count()",
            "bindings": {},
            "language": "gremlin-groovy",
            "aliases": {"graph": "%s" % self.graph, "g": "__g_%s" % self.graph}
        }
        code, ret = self.auth.post_gremlin(body, auth=self.user)
        print(code)
        print(ret)
        self.assertNotEqual(code, 200, msg="unAuthorize code check fail")

    def test_vertex_read_20(self):
        """
        vertex 读权限
        :return:
        """
        # add schema_indexLabel
        self.p.init_data("basic")

        # check role
        permission_list = [
            {
                "target_list": [
                    {"type": "VERTEX"},
                    {"type": "VERTEX_LABEL"},
                    {"type": "PROPERTY_KEY"}
                ],
                "permission": "READ",
                "name": "vertex_read"
            }
        ]
        user_id = set_auth.post_auth(permission_list)
        code, ret = self.auth.get_users_role(user_id)
        print(code)
        print(ret)
        for key, value in ret["roles"][self.graph].items():
            if key == "READ":
                self.assertIn(value[0]["type"], "VERTEX", msg="role type check fail")
            else:
                pass
        # check Authorize--vertex read
        v_id = '1:marko'
        code, ret = self.auth.get_vertex(v_id, auth=self.user)
        print(code)
        print(ret)
        self.assertEqual(code, 200, msg="Authorize code check fail")
        self.assertEqual(ret['id'], '1:marko', msg="Authorize code check fail")

        # check unAuthorize--edge read
        e_id = 'S1:marko>1>>S1:josh'
        code, ret = self.auth.get_edge(e_id, auth=self.user)
        print(code)
        print(ret)
        self.assertNotEqual(code, 200, msg="unAuthorize code check fail")

        # check unAuthorize--vertex write
        body = {
            "label": "person",
            "properties": {
                "name": "graphTest",
                "age": 29
            }
        }
        code, ret = self.auth.post_vertex(body, auth=self.user)
        print(code)
        print(ret)
        self.assertNotEqual(code, 200, msg="unAuthorize code check fail")

        # check unAuthorize--vertex delete
        code, ret = self.auth.delete_vertex(v_id, auth=self.user)
        print(code)
        print(ret)
        self.assertNotEqual(code, 200, msg="unAuthorize code check fail")

    def test_vertex_write_21(self):
        """
        vertex 写权限
        :return:
        """
        # add schema_indexLabel
        self.p.init_data("basic")

        # check role
        permission_list = [
            {
                "target_list": [
                    {"type": "VERTEX"},
                ],
                "permission": "WRITE",
                "name": "vertex_write"
            },
            {
                "target_list": [
                    {"type": "VERTEX_LABEL"},
                    {"type": "PROPERTY_KEY"}
                ],
                "permission": "READ",
                "name": "vertexLabel_read"
            }
        ]
        user_id = set_auth.post_auth(permission_list)
        code, ret = self.auth.get_users_role(user_id)
        print(code)
        print(ret)
        for key, value in ret["roles"][self.graph].items():
            if key == "WRITE":
                self.assertIn(value[0]["type"], "VERTEX", msg="role type check fail")
            else:
                pass

        # check Authorize--write
        body = {
            "label": "person",
            "properties": {
                "name": "graphTest",
                "age": 29,
                "city": "baoDing"
            }
        }
        code, ret = self.auth.post_vertex(body, auth=self.user)
        print(code)
        print(ret)
        self.assertEqual(code, 201, msg="Authorize code check fail")
        self.assertEqual(ret['id'], '1:graphTest', msg="Authorize code check fail")

        # check unAuthorize--read
        code, ret = self.auth.get_vertex('1:marko', auth=self.user)
        print(code)
        print(ret)
        self.assertNotEqual(code, 200, msg="unAuthorize code check fail")

        # check unAuthorize--delete
        code, ret = self.auth.delete_vertex('1:marko', auth=self.user)
        print(code)
        print(ret)
        self.assertNotEqual(code, 200, msg="unAuthorize code check fail")

    def test_vertex_delete_22(self):
        """
        vertex 删除权限
        :return:
        """
        # add schema_indexLabel
        self.p.init_data("basic")

        # check role
        permission_list = [
            {
                "target_list": [
                    {"type": "VERTEX"}
                ],
                "permission": "DELETE",
                "name": "vertex_delete"
            },
            {
                "target_list": [
                    {"type": "VERTEX"},
                    {"type": "VERTEX_LABEL"},
                    {"type": "PROPERTY_KEY"}
                ],
                "permission": "READ",
                "name": "vertex_read"  ###  删除顶点不应该有读点的权限 有bug
            }
        ]
        user_id = set_auth.post_auth(permission_list)
        code, ret = self.auth.get_users_role(user_id)
        print(code)
        print(ret)
        for key, value in ret["roles"][self.graph].items():
            if key == "DELETE":
                self.assertIn(value[0]["type"], "VERTEX", msg="role type check fail")
            else:
                pass

        # check Authorize-- vertex delete
        code, ret = self.auth.delete_vertex('1:marko', auth=self.user)
        print(code)
        print(ret)
        self.assertEqual(code, 204, msg="Authorize code check fail")

        # check unAuthorize--vertex read
        code, ret = self.auth.get_vertex('2:e', auth=self.user)
        print(code)
        print(ret)
        self.assertNotEqual(code, 200, msg="unAuthorize code check fail")

        # check unAuthorize--vertex write
        body = {
            "label": "person",
            "properties": {
                "name": "graphTest",
                "age": 29,
                "city": "baoDing"
            }
        }
        code, ret = self.auth.post_vertex(body, auth=self.user)
        print ("点delete权限 - 需要用到点的 read 权限 - 越权")
        # self.assertNotEqual(code, 200, msg="unAuthorize code check fail")

    def test_edge_read_23(self):
        """
        edge 读权限
        :return:
        """
        # add schema_indexLabel
        self.p.init_data("basic")

        # check role
        permission_list = [
            {
                "target_list": [
                    {"type": "PROPERTY_KEY"},
                    {"type": "EDGE_LABEL"},
                    {"type": "EDGE"},
                    {"type": "VERTEX_LABEL"},
                    {"type": "VERTEX"}
                ],
                "permission": "READ",
                "name": "edge_read"
            }
        ]
        user_id = set_auth.post_auth(permission_list)
        code, ret = self.auth.get_users_role(user_id)
        print(code)
        print(ret)
        for key, value in ret["roles"][self.graph].items():
            if key == "READ":
                self.assertIn(value[2]["type"], "EDGE", msg="role type check fail")
            else:
                pass

        # check Authorize--read
        code, ret = self.auth.get_edge('S1:o>2>>S2:p', auth=self.user)
        print(code)
        print(ret)
        self.assertEqual(code, 200, msg="Authorize code check fail")

        # check unAuthorize-- edge write
        body = {
            "label": "created",
            "outV": "1:peter",
            "inV": "2:lop",
            "outVLabel": "person",
            "inVLabel": "software",
            "properties": {
                "date": "2017-5-18",
                "weight": 0.2
            }
        }
        code, ret = self.auth.post_edge(body, auth=self.user)
        print(code)
        print(ret)
        self.assertNotEqual(code, 200, msg="unAuthorize code check fail")

        # check unAuthorize-- edge delete
        code, ret = self.auth.delete_edge('S1:o>2>>S2:p', auth=self.user)
        print(code)
        print(ret)
        self.assertNotEqual(code, 200, msg="unAuthorize code check fail")

    def test_edge_write_24(self):
        """
        edge 写权限
        :return:
        """
        # add schema_indexLabel
        self.p.init_data("basic")

        # check role
        permission_list = [
            {
                "target_list": [
                    {"type": "EDGE"}
                ],
                "permission": "WRITE",
                "name": "edge_write"
            },
            {
                "target_list": [
                    {"type": "VERTEX"},
                    {"type": "EDGE_LABEL"},
                    {"type": "VERTEX_LABEL"},
                    {"type": "PROPERTY_KEY"}
                ],
                "permission": "READ",
                "name": "property_read"
            }
        ]
        user_id = set_auth.post_auth(permission_list)
        code, ret = self.auth.get_users_role(user_id)
        print(code)
        print(ret)
        for key, value in ret["roles"][self.graph].items():
            if key == "WRITE":
                self.assertIn(value[0]["type"], "EDGE", msg="role type check fail")
            else:
                pass

        # check Authorize--write
        body = {
            "label": "created",
            "outV": "1:h",
            "inV": "2:zhao",
            "outVLabel": "person",
            "inVLabel": "software",
            "properties": {
                "city": "Mancheng",
                "date": "20200810"
            }
        }
        code, ret = self.auth.post_edge(body, auth=self.user)
        print(code)
        print(ret)
        self.assertEqual(code, 201, msg="Authorize code check fail")

        # check unAuthorize--read
        code, ret = self.auth.get_edge('S1:o>2>>S2:p', auth=self.user)
        print(code)
        print(ret)
        self.assertNotEqual(code, 200, msg="unAuthorize code check fail")

        # check unAuthorize--delete
        code, ret = self.auth.delete_edge('S1:o>2>>S2:p', auth=self.user)
        print(code)
        print(ret)
        self.assertNotEqual(code, 200, msg="unAuthorize code check fail")

    def test_edge_delete_25(self):
        """
        edge 删除权限
        :return:
        """
        # add schema_indexLabel
        self.p.init_data("basic")

        # check role
        permission_list = [
            {
                "target_list": [
                    {"type": "EDGE"}
                ],
                "permission": "DELETE",
                "name": "edge_delete"
            },
            {
                "target_list": [
                    {"type": "EDGE"},
                    {"type": "VERTEX"},
                    {"type": "EDGE_LABEL"},
                    {"type": "VERTEX_LABEL"},
                    {"type": "PROPERTY_KEY"}
                ],
                "permission": "READ",
                "name": "property_read"
            }
        ]
        user_id = set_auth.post_auth(permission_list)
        code, ret = self.auth.get_users_role(user_id)
        print(code)
        print(ret)
        for key, value in ret["roles"][self.graph].items():
            if key == "DELETE":
                self.assertIn(value[0]["type"], "EDGE", msg="role type check fail")
            else:
                pass

        # check Authorize--delete
        code, ret = self.auth.delete_edge('S1:o>2>>S2:p', auth=self.user)
        print(code)
        print(ret)
        self.assertEqual(code, 204, msg="Authorize code check fail")

        # check unAuthorize--write
        body = {
            "label": "created",
            "outV": "1:h",
            "inV": "2:zhao",
            "outVLabel": "person",
            "inVLabel": "software",
            "properties": {
                "city": "Mancheng",
                "date": "20200810"
            }
        }
        code, ret = self.auth.post_edge(body, auth=self.user)
        print(code)
        print(ret)
        self.assertNotEqual(code, 201, msg="unAuthorize code check fail")

        # check unAuthorize--read
        code, ret = self.auth.get_edge('S1:r>2>>S2:p', auth=self.user)
        print ("边delete权限 - 需要用到边 和 点 的 read 权限 - 越权")
        # self.assertNotEqual(code, 200, msg="unAuthorize code check fail")

    def test_gremlin_execute_26(self):
        """
        vertex 读权限
        :return:
        """
        # add schema_indexLabel
        self.p.init_data("basic")

        # check role
        permission_list = [
            {
                "target_list": [
                    {"type": "VERTEX"},
                    {"type": "VERTEX_LABEL"},
                    {"type": "PROPERTY_KEY"}
                ],
                "permission": "READ",
                "name": "vertex_read"
            },
            {
                "target_list": [
                    {"type": "GREMLIN"}
                ],
                "permission": "EXECUTE",
                "name": "gremlin_execute"
            }
        ]
        user_id = set_auth.post_auth(permission_list)
        code, ret = self.auth.get_users_role(user_id)
        print(code)
        print(ret)
        for key, value in ret["roles"][self.graph].items():
            if key == "READ":
                self.assertIn(value[0]["type"], "VERTEX", msg="role type check fail")
            elif key == "GREMLIN":
                self.assertIn(value[0]["type"], "EXECUTE", msg="role type check fail")
            else:
                pass

        # check Authorize--vertex read
        body = {
            "gremlin": "g.V().limit(2)",
            "bindings": {},
            "language": "gremlin-groovy",
            "aliases": {"graph": "%s" % self.graph, "g": "__g_%s" % self.graph}
        }
        code, ret = self.auth.post_gremlin(body, auth=self.user)
        print(code)
        print(ret)
        self.assertEqual(code, 200, msg="Authorize code check fail")
        self.assertEqual(len(ret['result']['data']), 2, msg="Authorize code check fail")

        # check unAuthorize--edge read
        body = {
            "gremlin": "g.E().limit(2)",
            "bindings": {},
            "language": "gremlin-groovy",
            "aliases": {"graph": "%s" % self.graph, "g": "__g_%s" % self.graph}
        }
        code, ret = self.auth.post_gremlin(body, auth=self.user)
        print(code)
        print(ret)
        self.assertEqual(code, 200, msg="unAuthorize code check fail")
        self.assertEqual(len(ret['result']['data']), 0, msg="unAuthorize code check fail")

    def test_gremlin_execute_27(self):
        """
        edge 读权限
        :return:
        """
        # add graph
        self.p.init_data("basic")

        # check role
        permission_list = [
            {
                "target_list": [
                    {"type": "VERTEX"},
                    {"type": "EDGE"},
                    {"type": "VERTEX_LABEL"},
                    {"type": "EDGE_LABEL"},
                    {"type": "PROPERTY_KEY"}
                ],
                "permission": "READ",
                "name": "edge_read"
            },
            {
                "target_list": [
                    {"type": "GREMLIN"}
                ],
                "permission": "EXECUTE",
                "name": "gremlin_execute"
            }
        ]
        user_id = set_auth.post_auth(permission_list)
        code, ret = self.auth.get_users_role(user_id)
        print(code)
        print(ret)
        for key, value in ret["roles"][self.graph].items():
            if key == "READ":
                self.assertIn(value[1]["type"], "EDGE", msg="role type check fail")
            else:
                pass

        # check Authorize--read
        body = {
            "gremlin": "g.E().limit(2)",
            "bindings": {},
            "language": "gremlin-groovy",
            "aliases": {"graph": "%s" % self.graph, "g": "__g_%s" % self.graph}
        }
        code, ret = self.auth.post_gremlin(body, auth=self.user)
        print(code)
        print(ret)
        self.assertEqual(code, 200, msg="Authorize code check fail")

        # check unAuthorize--read
        body = {
            "gremlin": "g.V().limit(2)",
            "bindings": {},
            "language": "gremlin-groovy",
            "aliases": {"graph": "%s" % self.graph, "g": "__g_%s" % self.graph}
        }
        code, ret = self.auth.post_gremlin(body, auth=self.user)
        print ("gremlin执行权限中查询边的权限 - 依赖查询点的权限")
        # self.assertNotEqual(code, 200, msg="unAuthorize code check fail")

    def test_var_read_28(self):
        """
        var 读权限
        :return:
        """
        # check role
        permission_list = [
            {
                "target_list": [
                    {"type": "VAR"}
                ],
                "permission": "READ",
                "name": "var_read"
            }
        ]
        user_id = set_auth.post_auth(permission_list)
        code, ret = self.auth.get_users_role(user_id)
        print(code)
        print(ret)
        for key, value in ret["roles"][self.graph].items():
            if key == "READ":
                self.assertIn(value[0]["type"], "VAR", msg="role type check fail")
            else:
                pass

        # check Authorize--read
        code, ret = self.auth.get_var(auth=self.user)
        self.assertEqual(code, 200, msg="unAuthorize code check fail")

        # check unAuthorize--write
        body = {
            "data": "tom"
        }
        code, ret = self.auth.put_var(body, "name", auth=self.user)
        print(code)
        print(ret)
        self.assertNotEqual(code, 200, msg="unAuthorize code check fail")

        # check unAuthorize--delete
        code, ret = self.auth.delete_var("name", auth=self.user)
        print(code)
        print(ret)
        self.assertNotEqual(code, 200, msg="unAuthorize code check fail")

    def test_var_write_29(self):
        """
        var 写权限
        :return:
        """
        # check role
        permission_list = [
            {
                "target_list": [
                    {"type": "VAR"}
                ],
                "permission": "WRITE",
                "name": "var_write"
            }
        ]
        user_id = set_auth.post_auth(permission_list)
        code, ret = self.auth.get_users_role(user_id)
        print(code)
        print(ret)
        for key, value in ret["roles"][self.graph].items():
            if key == "WRITE":
                self.assertIn(value[0]["type"], "VAR", msg="role type check fail")
            else:
                pass

        # check Authorize--write
        body = {
            "data": "tom"
        }
        code, ret = self.auth.put_var(body, "name", auth=self.user)
        print(code)
        print(ret)
        self.assertEqual(code, 200, msg="unAuthorize code check fail")

        # check unAuthorize--read
        code, ret = self.auth.get_var(auth=self.user)
        print(code)
        print(ret)
        self.assertNotEqual(code, 200, msg="unAuthorize code check fail")

        # check unAuthorize--delete
        code, ret = self.auth.delete_var("name", auth=self.user)
        print(code)
        print(ret)
        self.assertNotEqual(code, 200, msg="unAuthorize code check fail")

    def test_var_delete_30(self):
        """
        var 删除权限
        :return:
        """
        # check role
        permission_list = [
            {
                "target_list": [
                    {"type": "VAR"}
                ],
                "permission": "DELETE",
                "name": "var_delete"
            }
        ]
        user_id = set_auth.post_auth(permission_list)
        code, ret = self.auth.get_users_role(user_id)
        print(code)
        print(ret)
        for key, value in ret["roles"][self.graph].items():
            if key == "DELETE":
                self.assertIn(value[0]["type"], "VAR", msg="role type check fail")
            else:
                pass

        # check Authorize--delete
        code, ret = self.auth.delete_var("name", auth=self.user)
        print(code)
        print(ret)
        self.assertEqual(code, 204, msg="Authorize code check fail")

        # check unAuthorize--write
        body = {
            "data": "tom"
        }
        code, ret = self.auth.put_var(body, "name", auth=self.user)
        print(code)
        print(ret)
        self.assertNotEqual(code, 200, msg="unAuthorize code check fail")

        # check unAuthorize--read
        code, ret = self.auth.get_var(auth=self.user)
        print(code)
        print(ret)
        self.assertNotEqual(code, 200, msg="unAuthorize code check fail")

    def test_task_execute_write_read_31(self):
        """
        task 写、执行、读权限  用户只能读取自己写的task
        :return:
        """
        # check role
        permission_list = [
            {
                "target_list": [
                    {"type": "TASK"}
                ],
                "permission": "WRITE",
                "name": "task_write"
            },
            {
                "target_list": [
                    {"type": "TASK"}
                ],
                "permission": "EXECUTE",
                "name": "task_execute"
            },
            {
                "target_list": [
                    {"type": "TASK"}
                ],
                "permission": "READ",
                "name": "task_read"
            },
        ]
        user_id = set_auth.post_auth(permission_list)
        code, ret = self.auth.get_users_role(user_id)
        print(code)
        print(ret)
        for key, value in ret["roles"][self.graph].items():
            if key == "WRITE":
                self.assertIn(value[0]["type"], "TASK", msg="role type check fail")
            elif key == "READ":
                self.assertIn(value[0]["type"], "TASK", msg="role type check fail")
            else:
                pass

        # check Authorize--write
        gremlin = "for (int i = 0; i < 10; i++) { " \
                  "g.V().limit(5); " \
                  "try { sleep(1000);} " \
                  "catch (InterruptedException e) { break; }" \
                  "}"
        code, ret = self.auth.post_gremlin_task(gremlin, auth=self.user)
        print(code)
        print(ret)
        self.assertEqual(code, 201, msg="unAuthorize code check fail")
        self.assertEqual(ret['task_id'], 1, msg="unAuthorize code check fail")

        # check Authorize-- read
        code, ret = self.auth.get_task("1", auth=self.user)
        print(code)
        print(ret)
        self.assertEqual(code, 200, msg="Authorize code check fail")

    def test_task_execute_write_delete_33(self):
        """
        task 删除、执行权限
        :return:
        """
        # check role
        permission_list = [
            {
                "target_list": [
                    {"type": "TASK"}
                ],
                "permission": "DELETE",
                "name": "task_delete"
            },
            {
                "target_list": [
                    {"type": "TASK"}
                ],
                "permission": "WRITE",
                "name": "task_write"
            },
            {
                "target_list": [
                    {"type": "TASK"}
                ],
                "permission": "EXECUTE",
                "name": "task_execute"
            }
        ]
        user_id = set_auth.post_auth(permission_list)
        code, ret = self.auth.get_users_role(user_id)
        print(code)
        print(ret)
        for key, value in ret["roles"][self.graph].items():
            if key == "DELETE":
                self.assertIn(value[0]["type"], "TASK", msg="role type check fail")
            elif key == "WRITE":
                self.assertIn(value[0]["type"], "TASK", msg="role type check fail")
            else:
                pass

        # check Authorize--write
        gremlin = "g.V().limit(5); "
        code, ret = self.auth.post_gremlin_task(gremlin, auth=self.user)
        print(code)
        print(ret)
        self.assertEqual(code, 201, msg="unAuthorize code check fail")
        self.assertEqual(ret['task_id'], 1, msg="unAuthorize code check fail")

        time.sleep(5)
        # check Authorize--delete
        code, ret = self.auth.delete_task("1", auth=self.user)
        print(code)
        print(ret)
        self.assertEqual(code, 204, msg="Authorize code check fail")

    def test_useGroup_read_34(self):
        """
        user_group 读权限
        :return:
        """
        # check role
        permission_list = [
            {
                "target_list": [
                    {"type": "USER_GROUP"},
                    {"type": "STATUS"}
                ],
                "permission": "READ",
                "name": "userGroup_read"
            }
        ]
        user_id = set_auth.post_auth(permission_list)
        code, ret = self.auth.get_users_role(user_id)
        print(code)
        print(ret)
        for key, value in ret["roles"][self.graph].items():
            if key == "READ":
                self.assertIn(value[0]["type"], "USER_GROUP", msg="role type check fail")
            else:
                pass

        # check Authorize--read
        code, ret = self.auth.get_groups(auth=self.user)
        print(code)
        print(ret)
        self.assertEqual(code, 200, msg="unAuthorize code check fail")

        # check unAuthorize--write
        body = {"group_name": "gremlin", "group_description": "group can execute gremlin"}
        code, ret = self.auth.post_groups(body, auth=self.user)
        print(code)
        print(ret)
        self.assertNotEqual(code, 200, msg="unAuthorize code check fail")

        # check unAuthorize--delete
        code, ret = self.auth.delete_groups("-63:gremlin", auth=self.user)
        print(code)
        print(ret)
        self.assertNotEqual(code, 200, msg="unAuthorize code check fail")

    def test_useGroup_write_35(self):
        """
        user_group 写权限
        :return:
        """
        # check role
        permission_list = [
            {
                "target_list": [
                    {"type": "USER_GROUP"}
                ],
                "permission": "WRITE",
                "name": "userGroup_write"
            }
        ]
        user_id = set_auth.post_auth(permission_list)
        code, ret = self.auth.get_users_role(user_id)
        print(code)
        print(ret)
        for key, value in ret["roles"][self.graph].items():
            if key == "WRITE":
                self.assertIn(value[0]["type"], "USER_GROUP", msg="role type check fail")
            else:
                pass

        # check Authorize--write
        body = {"group_name": "gremlin", "group_description": "group can execute gremlin"}
        code, ret = self.auth.post_groups(body, auth=self.user)
        print(code)
        print(ret)
        self.assertEqual(code, 201, msg="unAuthorize code check fail")

        # check unAuthorize--read
        code, ret = self.auth.get_groups(auth=self.user)
        print(code)
        print(ret)
        self.assertNotEqual(code, 200, msg="unAuthorize code check fail")

        # check unAuthorize--delete
        code, ret = self.auth.delete_groups("-63:gremlin", auth=self.user)
        print(code)
        print(ret)
        self.assertNotEqual(code, 200, msg="unAuthorize code check fail")

    def test_useGroup_delete_36(self):
        """
        user_group 删除权限  ---- 删除权限依赖写权限
        :return:
        """
        # check role
        permission_list = [
            {
                "target_list": [
                    {"type": "USER_GROUP"}
                ],
                "permission": "DELETE",
                "name": "userGroup_delete"
            },
            {
                "target_list": [
                    {"type": "USER_GROUP"}
                ],
                "permission": "WRITE",
                "name": "userGroup_write"
            }
        ]
        user_id = set_auth.post_auth(permission_list)
        code, ret = self.auth.get_users_role(user_id)
        print(code)
        print(ret)
        for key, value in ret["roles"][self.graph].items():
            if key == "DELETE":
                self.assertIn(value[0]["type"], "USER_GROUP", msg="role type check fail")
            else:
                pass

        # check Authorize--delete
        code, ret = self.auth.delete_groups("-63:userGroup_delete_group", auth=self.user)
        print(code)
        print(ret)
        self.assertEqual(code, 204, msg="Authorize code check fail")

        # check unAuthorize--write
        body = {"group_name": "gremlin", "group_description": "group can execute gremlin"}
        code, ret = self.auth.post_groups(body, auth=self.user)
        print(code)
        print(ret)
        self.assertEqual(code, 201, msg="unAuthorize code check fail")

        # check unAuthorize--read
        code, ret = self.auth.get_groups(auth=self.user)
        print(code)
        print(ret)
        self.assertNotEqual(code, 200, msg="unAuthorize code check fail")

    def test_target_read_37(self):
        """
        target 读权限
        :return:
        """
        # check role
        permission_list = [
            {
                "target_list": [
                    {"type": "TARGET"},
                    {"type": "STATUS"}
                ],
                "permission": "READ",
                "name": "target_read"
            }
        ]
        user_id = set_auth.post_auth(permission_list)
        code, ret = self.auth.get_users_role(user_id)
        print(code)
        print(ret)
        for key, value in ret["roles"][self.graph].items():
            if key == "READ":
                self.assertIn(value[0]["type"], "TARGET", msg="role type check fail")
            else:
                pass

        # check Authorize--read
        code, ret = self.auth.get_targets(auth=self.user)
        print(code)
        print(ret)
        self.assertEqual(code, 200, msg="unAuthorize code check fail")

        # check unAuthorize--write
        body = {
            "target_url": "%s:%d" % (self.host, self.port),
            "target_name": "gremlin",
            "target_graph": "%s" % self.graph,
            "target_resources": [
                {"type": "GREMLIN"}
            ]
        }
        code, ret = self.auth.post_targets(body, auth=self.user)
        print(code)
        print(ret)
        self.assertNotEqual(code, 201, msg="unAuthorize code check fail")

        # check unAuthorize--delete
        code, ret = self.auth.delete_targets("-71:gremlin", auth=self.user)
        print(code)
        print(ret)
        self.assertNotEqual(code, 200, msg="unAuthorize code check fail")

    def test_target_write_38(self):
        """
        target 写权限
        :return:
        """
        # check role
        permission_list = [
            {
                "target_list": [
                    {"type": "TARGET"}
                ],
                "permission": "WRITE",
                "name": "target_write"
            }
        ]
        user_id = set_auth.post_auth(permission_list)
        code, ret = self.auth.get_users_role(user_id)
        print(code)
        print(ret)
        for key, value in ret["roles"][self.graph].items():
            if key == "WRITE":
                self.assertIn(value[0]["type"], "TARGET", msg="role type check fail")
            else:
                pass

        # check Authorize--write
        body = {
            "target_url": "%s:%d" % (self.host, self.port),
            "target_name": "gremlin",
            "target_graph": "%s" % self.graph,
            "target_resources": [
                {"type": "GREMLIN"}
            ]
        }
        code, ret = self.auth.post_targets(body, auth=self.user)
        print(code)
        print(ret)
        self.assertEqual(code, 201, msg="unAuthorize code check fail")

        # check unAuthorize--read
        code, ret = self.auth.get_targets(auth=self.user)
        print(code)
        print(ret)
        self.assertNotEqual(code, 200, msg="unAuthorize code check fail")

        # check unAuthorize--delete
        code, ret = self.auth.delete_targets("-71:gremlin", auth=self.user)
        print(code)
        print(ret)
        self.assertNotEqual(code, 200, msg="unAuthorize code check fail")

    def test_target_delete_39(self):
        """
        target 删除权限
        :return:
        """
        # check role
        permission_list = [
            {
                "target_list": [
                    {"type": "TARGET"}
                ],
                "permission": "DELETE",
                "name": "target_delete"
            }
        ]
        user_id = set_auth.post_auth(permission_list)
        code, ret = self.auth.get_users_role(user_id)
        print(code)
        print(ret)
        for key, value in ret["roles"][self.graph].items():
            if key == "DELETE":
                self.assertIn(value[0]["type"], "TARGET", msg="role type check fail")
            else:
                pass

        # check Authorize--delete
        code, ret = self.auth.delete_targets("-71:target_delete_target", auth=self.user)
        print(code)
        print(ret)
        self.assertEqual(code, 204, msg="Authorize code check fail")

        # check unAuthorize--write
        body = {
            "target_url": "%s:%d" % (self.host, self.port),
            "target_name": "gremlin",
            "target_graph": "%s" % self.graph,
            "target_resources": [
                {"type": "GREMLIN"}
            ]
        }
        code, ret = self.auth.post_targets(body, auth=self.user)
        print(code)
        print(ret)
        self.assertNotEqual(code, 201, msg="unAuthorize code check fail")

        # check unAuthorize--read
        code, ret = self.auth.get_targets(auth=self.user)
        print(code)
        print(ret)
        if code == 200:
            self.assertEqual(ret['targets'], [], msg="unAuthorize code check fail")
        else:
            self.assertNotEqual(code, 200, msg="unAuthorize code check fail")

    def test_all_read_40(self):
        """
        all 读权限
        :return:
        """
        # add graph
        self.p.init_data("basic")

        # check role
        permission_list = [
            {
                "target_list": [
                    {"type": "ALL"}
                ],
                "permission": "READ",
                "name": "all_read"
            },
            {
                "target_list": [
                    {"type": "ALL"}
                ],
                "permission": "EXECUTE",
                "name": "all_execute"
            }
        ]
        user_id = set_auth.post_auth(permission_list)
        code, ret = self.auth.get_users_role(user_id)
        print(code)
        print(ret)
        for key, value in ret["roles"][self.graph].items():
            if key == "READ":
                self.assertIn(value[0]["type"], "ALL", msg="role type check fail")
            else:
                pass

        # check Authorize--read
        body = {
            "gremlin": "g.E().limit(10).count()",
            "bindings": {},
            "language": "gremlin-groovy",
            "aliases": {"graph": "%s" % self.graph, "g": "__g_%s" % self.graph}
        }
        code, ret = self.auth.post_gremlin(body, auth=self.user)
        print(code)
        print(ret)
        self.assertEqual(code, 200, msg="Authorize code check fail")

        # check unAuthorize--write
        body = {
            "label": "person",
            "properties": {
                "name": "graphTest",
                "age": 29,
                "city": "baoDing"
            }
        }
        code, ret = self.auth.post_vertex(body, auth=self.user)
        print(code)
        print(ret)
        self.assertNotEqual(code, 201, msg="unAuthorize code check fail")

        # check unAuthorize--delete
        code, ret = self.auth.delete_vertex('1:marko', auth=self.user)
        print(code)
        print(ret)
        self.assertNotEqual(code, 200, msg="unAuthorize code check fail")

        # check unAuthorize--grant
        code, ret = self.auth.get_targets(auth=self.user)
        print(code)
        print(ret)
        if code == 200:
            self.assertEqual(ret['targets'], [], msg="unAuthorize code check fail")
        else:
            self.assertNotEqual(code, 200, msg="unAuthorize code check fail")

    def test_all_write_41(self):
        """
        all 写权限
        :return:
        """
        # add graph
        self.p.init_data("basic")

        # check role
        permission_list = [
            {
                "target_list": [
                    {"type": "ALL"}
                ],
                "permission": "WRITE",
                "name": "all_write"
            },
            {
                "target_list": [
                    {"type": "ALL"}
                ],
                "permission": "EXECUTE",
                "name": "all_execute"
            }
        ]
        user_id = set_auth.post_auth(permission_list)
        code, ret = self.auth.get_users_role(user_id)
        print(code)
        print(ret)
        for key, value in ret["roles"][self.graph].items():
            if key == "WRITE":
                self.assertIn(value[0]["type"], "ALL", msg="role type check fail")
            else:
                pass

        # check Authorize--write
        body = {
            "label": "person",
            "properties": {
                "name": "graphTest",
                "age": 29,
                "city": "baoDing"
            }
        }
        code, ret = self.auth.post_vertex(body, auth=self.user)
        print(code)
        print(ret)
        # self.assertEqual(code, 201, msg="unAuthorize code check fail")

        # check unAuthorize--read
        body = {
            "gremlin": "g.E().limit(10).count()",
            "bindings": {},
            "language": "gremlin-groovy",
            "aliases": {"graph": "%s" % self.graph, "g": "__g_%s" % self.graph}
        }
        code, ret = self.auth.post_gremlin(body, auth=self.user)
        print(code)
        print(ret)
        self.assertEqual(code, 200, msg="unAuthorize code check fail")
        self.assertEqual(ret['result']['data'], [0], msg="unAuthorize code check fail")

        # check unAuthorize--delete
        code, ret = self.auth.delete_vertex('1:marko', auth=self.user)
        print(code)
        print(ret)
        self.assertNotEqual(code, 200, msg="unAuthorize code check fail")

        # check unAuthorize--grant
        body = {
            "target_url": "%s:%d" % (self.host, self.port),
            "target_name": "gremlin",
            "target_graph": "%s" % self.graph,
            "target_resources": [
                {"type": "GREMLIN"}
            ]
        }
        code, ret = self.auth.post_targets(body, auth=self.user)
        print(code)
        print(ret)
        self.assertNotEqual(code, 201, msg="unAuthorize code check fail")

    def test_all_delete_42(self):
        """
        all 删除权限
        :return:
        """
        # add graph
        self.p.init_data("basic")

        # check role
        permission_list = [
            {
                "target_list": [
                    {"type": "ALL"}
                ],
                "permission": "DELETE",
                "name": "all_delete"
            },
            {
                "target_list": [
                    {"type": "ALL"}
                ],
                "permission": "EXECUTE",
                "name": "all_execute"
            }
        ]
        user_id = set_auth.post_auth(permission_list)
        code, ret = self.auth.get_users_role(user_id)
        print(code)
        print(ret)
        for key, value in ret["roles"][self.graph].items():
            if key == "DELETE":
                self.assertIn(value[0]["type"], "ALL", msg="role type check fail")
            else:
                pass

        # check Authorize--delete
        code, ret = self.auth.delete_vertex('1:marko', auth=self.user)
        print(code)
        print(ret)
        # self.assertEqual(code, 200, msg="unAuthorize code check fail")

        # check unAuthorize--write
        body = {
            "label": "person",
            "properties": {
                "name": "graphTest",
                "age": 29,
                "city": "baoDing"
            }
        }
        code, ret = self.auth.post_vertex(body, auth=self.user)
        print(code)
        print(ret)
        self.assertNotEqual(code, 201, msg="unAuthorize code check fail")

        # check unAuthorize--read
        body = {
            "gremlin": "g.E().limit(10).count()",
            "bindings": {},
            "language": "gremlin-groovy",
            "aliases": {"graph": "%s" % self.graph, "g": "__g_%s" % self.graph}
        }
        code, ret = self.auth.post_gremlin(body, auth=self.user)
        print(code)
        print(ret)
        self.assertEqual(code, 200, msg="unAuthorize code check fail")
        self.assertEqual(ret['result']['data'], [0], msg="unAuthorize code check fail")


        # check unAuthorize-- target_delete
        code, ret = self.auth.delete_targets("-71:all_delete_target", auth=self.user)
        print(code)
        print(ret)
        self.assertNotEqual(code, 204, msg="Authorize code check fail")

    def test_grant_read_43(self):
        """
        grant 读权限
        :return:
        """
        # check role
        permission_list = [
            {
                "target_list": [
                    {"type": "GRANT"},
                    {"type": "STATUS"}
                ],
                "permission": "READ",
                "name": "grant_read"
            }
        ]
        user_id = set_auth.post_auth(permission_list)
        code, ret = self.auth.get_users_role(user_id)
        print(code)
        print(ret)
        for key, value in ret["roles"][self.graph].items():
            if key == "READ":
                self.assertIn(value[0]["type"], "GRANT", msg="role type check fail")
            else:
                pass

        # check Authorize--read
        code, ret = self.auth.get_accesses(auth=self.user)
        print(code)
        print(ret)
        self.assertEqual(code, 200, msg="unAuthorize code check fail")

        # check unAuthorize--write
        body = {"group": "-63:gremlin", "target": "-71:gremlin", "access_permission": "EXECUTE"}
        code, ret = self.auth.post_accesses(body, auth=self.user)
        print(code)
        print(ret)
        self.assertNotEqual(code, 200, msg="unAuthorize code check fail")

        # check unAuthorize--delete
        code, ret = self.auth.delete_accesses("S-63:gremlin>-82>18>S-71:gremlin", auth=self.user)
        print(code)
        print(ret)
        self.assertNotEqual(code, 200, msg="unAuthorize code check fail")

    def test_grant_write_44(self):
        """
        grant 写权限
        :return:
        """
        # check role
        permission_list = [
            {
                "target_list": [
                    {"type": "USER_GROUP"}
                ],
                "permission": "WRITE",
                "name": "userGroup_write"
            }
        ]
        user_id = set_auth.post_auth(permission_list)
        code, ret = self.auth.get_users_role(user_id)
        print(code)
        print(ret)
        for key, value in ret["roles"][self.graph].items():
            if key == "WRITE":
                self.assertIn(value[0]["type"], "USER_GROUP", msg="role type check fail")
            else:
                pass

        # check Authorize--write
        body = {"group_name": "gremlin", "group_description": "group can execute gremlin"}
        code, ret = self.auth.post_groups(body, auth=self.user)
        print(code)
        print(ret)
        self.assertEqual(code, 201, msg="unAuthorize code check fail")

        # check unAuthorize--read
        code, ret = self.auth.get_groups(auth=self.user)
        print(code)
        print(ret)
        self.assertNotEqual(code, 200, msg="unAuthorize code check fail")

        # check unAuthorize--delete
        code, ret = self.auth.delete_groups("-63:gremlin", auth=self.user)
        print(code)
        print(ret)
        self.assertNotEqual(code, 200, msg="unAuthorize code check fail")

    def test_grant_delete_45(self):
        """
        user_group 删除权限  ---- 删除权限依赖写权限
        :return:
        """
        # check role
        permission_list = [
            {
                "target_list": [
                    {"type": "USER_GROUP"}
                ],
                "permission": "DELETE",
                "name": "userGroup_delete"
            },
            {
                "target_list": [
                    {"type": "USER_GROUP"}
                ],
                "permission": "WRITE",
                "name": "userGroup_write"
            }
        ]
        user_id = set_auth.post_auth(permission_list)
        code, ret = self.auth.get_users_role(user_id)
        print(code)
        print(ret)
        for key, value in ret["roles"][self.graph].items():
            if key == "DELETE":
                self.assertIn(value[0]["type"], "USER_GROUP", msg="role type check fail")
            else:
                pass

        # check Authorize--delete
        code, ret = self.auth.delete_groups("-63:userGroup_delete_group", auth=self.user)
        print(code)
        print(ret)
        self.assertEqual(code, 204, msg="Authorize code check fail")

        # check unAuthorize--write
        body = {"group_name": "gremlin", "group_description": "group can execute gremlin"}
        code, ret = self.auth.post_groups(body, auth=self.user)
        print(code)
        print(ret)
        self.assertEqual(code, 201, msg="unAuthorize code check fail")

        # check unAuthorize--read
        code, ret = self.auth.get_groups(auth=self.user)
        print(code)
        print(ret)
        self.assertNotEqual(code, 200, msg="unAuthorize code check fail")


if __name__ == '__main__':
    # # run all cases
    # unittest.main(verbosity=2)

    # run one case
    suite = unittest.TestSuite()
    suite.addTest(TestCommonAuth("test_grant_read_43"))
    runner = unittest.TextTestRunner()
    runner.run(suite)

    # code, ret = Auths().get_propertykeys(auth={"graphTest": "123456"})
    # print ret
