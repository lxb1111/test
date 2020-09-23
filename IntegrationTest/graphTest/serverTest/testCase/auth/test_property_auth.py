# -*- coding:utf-8 -*-
"""
author     : lxb
note       : 细粒度权限的鉴权和越权
create_time: 2020/4/27 11:17 上午
"""
import sys
import os
import unittest
import importlib

sys.path.append('%s/..' % os.path.split(os.path.realpath(__file__))[0])
sys.path.append('../../')
importlib.reload(sys)

from IntegrationTest.graphTest.serverTest.common.hugegraph_api.auth_api import Auths
from IntegrationTest.graphTest.serverTest.testCase.auth import set_auth
from IntegrationTest.graphTest.serverTest.common.config.produce_data import ProduceData
from IntegrationTest.graphTest.serverTest.common.hugegraph_api.basic_cls import BasicClassMethod

TYPE = "basic"


class TestDetailAuth(unittest.TestCase):
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
        self.user = {"graphTest": "123456"}
        # 清空图数据，只保留超管权限
        self.p.init_data("clear")

    def test_vertex_pro_single_string_read_01(self):
        """
        vertex 读单个限制string属性权限
        :return:
        """
        # add graph
        self.p.init_data("basic")

        # check role
        permission_list = [
            {"target_list": [{"type": "PROPERTY_KEY"},
                             {"type": "VERTEX_LABEL"},
                             {"type": "VERTEX", "label": "person", "properties": {"city": "Shanghai"}}],
             "permission": "READ",
             "name": "vertex_read"},
        ]
        print(permission_list)
        user_id = set_auth.post_auth(permission_list)
        code, ret = self.auth.get_users_role(user_id)
        # print ret
        for key, value in ret["roles"][self.graph].items():
            if key == "READ":
                self.assertIn(value[0]["type"], "PROPERTY_KEY", msg="role type check fail")
                self.assertIn(value[1]["type"], "VERTEX_LABEL", msg="role type check fail")
                self.assertIn(value[2]["type"], "VERTEX", msg="role type check fail")
            else:
                pass

        # check Authorize--read
        code, ret = self.auth.get_vertex_all(auth=self.user)
        # print code, ret
        self.assertEqual(code, 200, msg=ret)

        # check Unauthorized--write
        body = {
            "label": "person",
            "properties": {
                "name": "marko",
                "age": 29
            }
        }
        code, ret = self.auth.post_vertex(body, auth=self.user)
        self.assertNotEqual(code, 201, msg=ret)
        self.assertEqual(ret["message"], "User not authorized.", msg="Unauthorized result check fail")

        # check Unauthorized--delete
        name = "1:marko"
        code, ret = self.auth.delete_vertex(name, auth=self.user)
        self.assertNotEqual(code, 204, msg=ret)
        self.assertEqual(ret["message"], "User not authorized.", msg="Unauthorized result check fail")

    # 不加read权限去读,不加write权限去写,不加delete权限去删
    def test_vertex_pro_single_string_read_01_noread_nowrite_nodelete(self):
        """
        vertex 读单个限制string属性权限
        :return:
        """
        # add graph
        self.p.init_data("basic")

        # check role
        permission_list = [
            {"target_list": [{"type": "PROPERTY_KEY"},
                             {"type": "VERTEX_LABEL"}],
             "permission": "READ",
             "name": "vertex_read"},
        ]
        print(permission_list)
        user_id = set_auth.post_auth(permission_list)
        code, ret = self.auth.get_users_role(user_id)
        for key, value in ret["roles"][self.graph].items():
            if key == "READ":
                self.assertIn(value[0]["type"], "PROPERTY_KEY", msg="role type check fail")
                self.assertIn(value[1]["type"], "VERTEX_LABEL", msg="role type check fail")
            else:
                pass

        # check Authorize--read
        code, ret = self.auth.get_vertex_all(auth=self.user)
        # print code, ret
        self.assertEqual(code, 200, msg=ret)
        self.assertEqual(ret["vertex"], "[]", msg="Unauthorized result check fail")

        # check Unauthorized--write
        body = {
            "label": "person",
            "properties": {
                "name": "marko",
                "age": 29
            }
        }
        code, ret = self.auth.post_vertex(body, auth=self.user)
        self.assertEqual(code, 403, msg=ret)
        self.assertEqual(ret["message"], "User not authorized.", msg="Unauthorized result check fail")

        # check Unauthorized--delete
        name = "1:marko"
        code, ret = self.auth.delete_vertex(name, auth=self.user)
        self.assertEqual(code, 403, msg=ret)
        self.assertEqual(ret["message"], "User not authorized.", msg="Unauthorized result check fail")

    def test_vertex_pro_single_string_write_02(self):
        """
        vertex 写单个限制string属性权限
        :return:
        """
        # add graph
        self.p.init_data("basic")

        # check role
        permission_list = [
            {"target_list": [{"type": "PROPERTY_KEY"}, {"type": "VERTEX_LABEL"}], "permission": "READ",
             "name": "vertexlabel_pro_read"},
            {"target_list": [{"type": "VERTEX", "label": "person", "properties": {"city": "Shanghai"}}],
             "permission": "WRITE", "name": "vertex_write"}
        ]

        user_id = set_auth.post_auth(permission_list)
        code, ret = self.auth.get_users_role(user_id)
        for key, value in ret["roles"][self.graph].items():
            if key == "WRITE":
                self.assertIn(value[0]["type"], "VERTEX", msg="role type check fail")
            elif key == "READ":
                self.assertIn(value[0]["type"], "PROPERTY_KEY", msg="role type check fail")

        # check Unauthorized--write
        body = {
            "label": "person",
            "properties": {
                "name": "new1",
                "age": 45,
                "city": "Shanghai"
            }
        }

        code, ret = self.auth.post_vertex(body, auth=self.user)
        self.assertEqual(code, 201, msg=ret)

        # check Authorize--read
        code, ret = self.auth.get_vertex_all(auth=self.user)
        # # print code, ret
        self.assertEqual(code, 200, msg=ret)
        self.assertEqual(ret["vertices"], [], msg="Unauthorized result check fail")

        # check Unauthorized--delete
        name = "1:marko"
        code, ret = self.auth.delete_vertex(name, auth=self.user)
        self.assertNotEqual(code, 204, msg=ret)
        self.assertEqual(ret["message"], "User not authorized.", msg="Unauthorized result check fail")

    def test_vertex_pro_single_string_delete_03(self):
        """
        vertex 删除单个限制string属性权限
        :return:
        """
        # add graph
        self.p.init_data("basic")

        # check role
        permission_list = [
            {"target_list": [{"type": "PROPERTY_KEY"}, {"type": "VERTEX_LABEL"}, {"type": "VERTEX"}],
             "permission": "READ", "name": "vertexlabel_pro_read"},
            {"target_list": [{"type": "VERTEX", "label": "person", "properties": {"city": "Shanghai"}}],
             "permission": "DELETE", "name": "vertex_delete"}
        ]
        user_id = set_auth.post_auth(permission_list)
        code, ret = self.auth.get_users_role(user_id)
        # print code, ret
        for key, value in ret["roles"][self.graph].items():
            if key == "DELETE":
                self.assertIn(value[0]["type"], "VERTEX_LABEL", msg="role type check fail")
            elif key == "READ":
                self.assertIn(value[0]["type"], "PROPERTY_KEY", msg="role type check fail")
                self.assertIn(value[1]["type"], "VERTEX_LABEL", msg="role type check fail")
                self.assertIn(value[2]["type"], "VERTEX", msg="role type check fail")
            else:
                pass

        # check Unauthorized--delete
        # vertex_id = "1:marko"
        vertex_id = "1:r"
        code, ret = self.auth.delete_vertex(vertex_id, auth=self.user)
        self.assertEqual(code, 204, msg=ret)

        # check Authorize--read
        code, ret = self.auth.get_vertex_all(auth=self.user)
        # print code, ret
        self.assertEqual(code, 200, msg=ret)

        # check Unauthorized--write
        body = {
            "label": "person",
            "properties": {
                "name": "marko",
                "age": 29
            }
        }
        code, ret = self.auth.post_vertex(body, auth=self.user)
        self.assertNotEqual(code, 201, msg=ret)
        self.assertEqual(ret["message"], "User not authorized.", msg="Unauthorized result check fail")

    # 不加读的权限，不可以删除
    def test_vertex_pro_single_string_delete_03_noread(self):
        """
        vertex 删除单个限制string属性权限
        :return:
        """
        # add graph
        self.p.init_data("basic")

        # check role
        permission_list = [
            {"target_list": [{"type": "PROPERTY_KEY"}, {"type": "VERTEX_LABEL"}], "permission": "READ",
             "name": "vertexlabel_pro_read"},
            {"target_list": [{"type": "VERTEX", "label": "person", "properties": {"city": "Shanghai"}}],
             "permission": "DELETE", "name": "vertex_delete"}
        ]
        user_id = set_auth.post_auth(permission_list)
        code, ret = self.auth.get_users_role(user_id)
        for key, value in ret["roles"][self.graph].items():
            if key == "DELETE":
                self.assertIn(value[0]["type"], "VERTEX_LABEL", msg="role type check fail")
            elif key == "READ":
                self.assertIn(value[0]["type"], "PROPERTY_KEY", msg="role type check fail")
                self.assertIn(value[1]["type"], "VERTEX_LABEL", msg="role type check fail")
            else:
                pass

        # check Unauthorized--delete
        # vertex_id = "1:marko"
        vertex_id = "1:r"
        code, ret = self.auth.delete_vertex(vertex_id, auth=self.user)
        self.assertEqual(code, 403, msg=ret)

        # check Authorize--read
        code, ret = self.auth.get_vertex_all(auth=self.user)
        # print code, ret
        self.assertEqual(code, 200, msg=ret)
        self.assertEqual(ret["vertices"], [], msg=ret)

        # check Unauthorized--write
        body = {
            "label": "person",
            "properties": {
                "name": "marko",
                "age": 29
            }
        }
        code, ret = self.auth.post_vertex(body, auth=self.user)
        self.assertNotEqual(code, 201, msg=ret)
        self.assertEqual(ret["message"], "User not authorized.", msg="Unauthorized result check fail")

    def test_vertex_pro_single_int_read_04(self):

        """
        vertex 读单个限制int属性权限
        :return:
        """
        # add graph
        self.p.init_data("basic")

        # check role
        permission_list = [
            {"target_list": [{"type": "PROPERTY_KEY"},
                             {"type": "VERTEX_LABEL"},
                             {"type": "VERTEX", "label": "person", "properties": {"age": "P.gte(30)"}}],
             "permission": "READ",
             "name": "vertex_read"}
        ]
        print(permission_list)
        user_id = set_auth.post_auth(permission_list)
        code, ret = self.auth.get_users_role(user_id)
        for key, value in ret["roles"][self.graph].items():
            self.assertEqual(key, "READ", msg="role permission check fail")
            self.assertEqual(value[2]["type"], "VERTEX", msg="role type check fail")

        # check Authorize--read
        code, ret = self.auth.get_vertex_all(auth=self.user)
        # print code, ret
        self.assertEqual(code, 200, msg=ret)

        # check Unauthorized--write
        body = {
            "label": "person",
            "properties": {
                "name": "marko",
                "age": 45
            }
        }
        code, ret = self.auth.post_vertex(body, auth=self.user)
        self.assertNotEqual(code, 201, msg=ret)
        self.assertEqual(ret["message"], "User not authorized.", msg="Unauthorized result check fail")

        # check Unauthorized--delete
        name = "1:marko"
        code, ret = self.auth.delete_vertex(name, auth=self.user)
        self.assertNotEqual(code, 204, msg=ret)
        self.assertEqual(ret["message"], "User not authorized.", msg="Unauthorized result check fail")

    def test_vertex_pro_single_int_write_05(self):
        """
        vertex 写单个限制int属性权限
        :return:
        """
        # add graph
        self.p.init_data("basic")

        # check role
        permission_list = [
            {"target_list": [{"type": "PROPERTY_KEY"}, {"type": "VERTEX_LABEL"}], "permission": "READ",
             "name": "vertexlabel_pro_read"},
            {"target_list": [{"type": "VERTEX", "label": "person", "properties": {"age": "P.gte(30)"}}],
             "permission": "WRITE", "name": "vertex_write"}
        ]

        print(permission_list)
        user_id = set_auth.post_auth(permission_list)
        code, ret = self.auth.get_users_role(user_id)
        for key, value in ret["roles"][self.graph].items():
            if key == "WRITE":
                self.assertIn(value[0]["type"], "VERTEX", msg="role type check fail")
            elif key == "READ":
                self.assertIn(value[0]["type"], "PROPERTY_KEY", msg="role type check fail")

        # check Unauthorized--write
        body = {
            "label": "person",
            "properties": {
                "name": "new1",
                "age": 45,
                "city": "Shanghai"
            }
        }

        code, ret = self.auth.post_vertex(body, auth=self.user)
        self.assertEqual(code, 201, msg=ret)

        # check Authorize--read
        code, ret = self.auth.get_vertex_all(auth=self.user)
        # print code, ret
        self.assertNotEqual(code, 200, msg=ret)
        self.assertEqual(ret["message"], "User not authorized.", msg="Unauthorized result check fail")

        # check Unauthorized--delete
        name = "1:marko"
        code, ret = self.auth.delete_vertex(name, auth=self.user)
        self.assertNotEqual(code, 204, msg=ret)
        self.assertEqual(ret["message"], "User not authorized.", msg="Unauthorized result check fail")

    def test_vertex_pro_single_int_delete_06(self):
        """
        vertex 删除单个限制int属性权限
        :return:
        """
        # add graph
        self.p.init_data("basic")

        # check role
        permission_list = [
            {"target_list": [{"type": "PROPERTY_KEY"}, {"type": "VERTEX_LABEL"}, {"type": "VERTEX"}],
             "permission": "READ",
             "name": "vertexlabel_pro_read"},
            {"target_list": [{"type": "VERTEX", "label": "person", "properties": {"age": "P.gte(30)"}}],
             "permission": "DELETE", "name": "vertex_delete"}
        ]
        user_id = set_auth.post_auth(permission_list)
        code, ret = self.auth.get_users_role(user_id)
        for key, value in ret["roles"][self.graph].items():
            if key == "DELETE":
                self.assertIn(value[0]["type"], "VERTEX", msg="role type check fail")
            elif key == "READ":
                self.assertIn(value[0]["type"], "PROPERTY_KEY", msg="role type check fail")
                self.assertIn(value[1]["type"], "VERTEX_LABEL", msg="role type check fail")
                self.assertIn(value[2]["type"], "VERTEX", msg="role type check fail")
            else:
                pass

        # check Unauthorized--delete                                  # 删除的时候报没有这个顶点的ID
        # vertex_id = "1:marko"
        vertex_id = "1:h"
        code, ret = self.auth.delete_vertex(vertex_id, auth=self.user)
        self.assertEqual(code, 204, msg=ret)

        # check Authorize--read
        code, ret = self.auth.get_vertex_all(auth=self.user)
        # print code, ret
        self.assertNotEqual(code, 200, msg=ret)

        # check Unauthorized--write
        body = {
            "label": "person",
            "properties": {
                "name": "marko",
                "age": 56
            }
        }
        code, ret = self.auth.post_vertex(body, auth=self.user)
        self.assertNotEqual(code, 201, msg=ret)
        self.assertEqual(ret["message"], "User not authorized.", msg="Unauthorized result check fail")

    def test_vertex_pro_list_string_read_07(self):

        """
        vertex 读单个限制list属性权限
        :return:
        """
        # add graph
        self.p.init_data("list_pro")

        # check role
        permission_list = [
            {"target_list": [{"type": "PROPERTY_KEY"},
                             {"type": "VERTEX_LABEL"},
                             {"type": "VERTEX", "label": "person", "properties": {"city": "P.contains(\"Shanxi\")"}}],
             "permission": "READ",
             "name": "vertex_read"}
        ]
        user_id = set_auth.post_auth(permission_list)
        code, ret = self.auth.get_users_role(user_id)
        for key, value in ret["roles"][self.graph].items():
            if key == "READ":
                self.assertIn(value[2]["type"], "VERTEX_LABEL", msg="role type check fail")
            else:
                pass

        # check Authorize--read
        code, ret = self.auth.get_vertex_all(auth=self.user)
        # print code, ret
        self.assertEqual(code, 200, msg=ret)

        # check Unauthorized--write
        body = {
            "label": "person",
            "properties": {
                "name": "new1",
                "age": 46,
                "city": ["Shanxi", "qwe"]
            }
        }
        code, ret = self.auth.post_vertex(body, auth=self.user)
        self.assertNotEqual(code, 201, msg=ret)
        self.assertEqual(ret["message"], "User not authorized.", msg="Unauthorized result check fail")

        # check Unauthorized--delete
        name = "1:peter"
        code, ret = self.auth.delete_vertex(name, auth=self.user)
        self.assertNotEqual(code, 204, msg=ret)
        self.assertEqual(ret["message"], "User not authorized.", msg="Unauthorized result check fail")

    def test_vertex_pro_list_string_write_08(self):
        """
        string属性基数为list，vertex写权限
        :return:
        """
        # add graph
        self.p.init_data("list_pro")

        # check role
        permission_list = [
            {"target_list": [{"type": "PROPERTY_KEY"}, {"type": "VERTEX_LABEL"}], "permission": "READ",
             "name": "vertexlabel_pro_read"},
            {"target_list": [{"type": "VERTEX", "label": "person", "properties": {"city": "P.contains(\"Shanxi\")"}}],
             "permission": "WRITE", "name": "vertex_write"}
        ]

        user_id = set_auth.post_auth(permission_list)
        code, ret = self.auth.get_users_role(user_id)
        for key, value in ret["roles"][self.graph].items():
            if key == "WRITE":
                self.assertIn(value[0]["type"], "VERTEX", msg="role type check fail")
            elif key == "READ":
                self.assertIn(value[0]["type"], "PROPERTY_KEY", msg="role type check fail")
            elif key == "EXECUTE":
                self.assertIn(value[0]["type"], "GREMLIN", msg="role type check fail")
            else:
                pass

        # check Unauthorized--write
        body = {
            "label": "person",
            "properties": {
                "name": "new1",
                "age": 46,
                "city": ["Shanxi", "qwe"]
            }
        }

        code, ret = self.auth.post_vertex(body, auth=self.user)
        self.assertEqual(code, 201, msg=ret)

        # check Authorize--read
        code, ret = self.auth.get_vertex_all(auth=self.user)
        # print code, ret
        self.assertEqual(code, 200, msg=ret)
        self.assertEqual(ret['vertices'], [], msg=ret)

        # check Unauthorized--delete
        name = "1:marko"
        code, ret = self.auth.delete_vertex(name, auth=self.user)
        self.assertNotEqual(code, 204, msg=ret)
        self.assertEqual(ret["message"], "User not authorized.", msg="Unauthorized result check fail")

    def test_vertex_pro_list_string_delete_09(self):
        """
        string属性基数为list，vertex删除权限
        :return:
        """
        # add graph
        self.p.init_data("list_pro")

        # check role
        permission_list = [
            {"target_list": [{"type": "PROPERTY_KEY"}, {"type": "VERTEX_LABEL"}, {"type": "VERTEX"}],
             "permission": "READ",
             "name": "vertexlabel_pro_read"},
            {"target_list": [{"type": "VERTEX", "label": "person", "properties": {"city": "P.contains(\"Shanxi\")"}}],
             "permission": "DELETE", "name": "vertex_delete"}
        ]
        user_id = set_auth.post_auth(permission_list)
        code, ret = self.auth.get_users_role(user_id)
        for key, value in ret["roles"][self.graph].items():
            if key == "DELETE":
                self.assertIn(value[0]["type"], "VERTEX", msg="role type check fail")
            elif key == "READ":
                self.assertIn(value[0]["type"], "PROPERTY_KEY", msg="role type check fail")
                self.assertIn(value[1]["type"], "VERTEX_LABEL", msg="role type check fail")
                self.assertIn(value[2]["type"], "VERTEX", msg="role type check fail")
            else:
                pass

        # check Unauthorized--delete                                               删除定点报没有此顶点ID
        vertex_id = "1:peter"
        # vertex_id = "1:r"
        code, ret = self.auth.delete_vertex(vertex_id, auth=self.user)
        self.assertEqual(code, 204, msg=ret)

        # check Authorize--read
        code, ret = self.auth.get_vertex_all(auth=self.user)
        # print code, ret
        self.assertNotEqual(code, 200, msg=ret)

        # check Unauthorized--write
        body = {
            "label": "person",
            "properties": {
                "name": "marko",
                "age": 56,
                "city": ["Shanxi", "qwe"]

            }
        }
        code, ret = self.auth.post_vertex(body, auth=self.user)
        self.assertNotEqual(code, 201, msg=ret)
        self.assertEqual(ret["message"], "User not authorized.", msg="Unauthorized result check fail")

    def test_vertex_read_Multiple_10(self):

        """
        vertex 读多个限制属性权限
        :return:
        """
        # add graph
        self.p.init_data("basic")

        # check role
        permission_list = [
            {"target_list": [{"type": "PROPERTY_KEY"},
                             {"type": "VERTEX_LABEL"},
                             {"type": "VERTEX", "label": "person",
                              "properties": {"city": "Shanxi", "age": "P.gte(20)"}}],
             "permission": "READ",
             "name": "vertex_read"}
        ]
        user_id = set_auth.post_auth(permission_list)
        code, ret = self.auth.get_users_role(user_id)
        for key, value in ret["roles"][self.graph].items():
            if key == "READ":
                self.assertIn(value[2]["type"], "VERTEX_LABEL", msg="role type check fail")
            else:
                pass

        # check Authorize--read
        code, ret = self.auth.get_vertex_all(auth=self.user)
        self.assertEqual(code, 200, msg=ret)

        # check Unauthorized--write
        body = {
            "label": "person",
            "properties": {
                "name": "marko",
                "age": 45
            }
        }
        code, ret = self.auth.post_vertex(body, auth=self.user)
        self.assertNotEqual(code, 201, msg=ret)
        self.assertEqual(ret["message"], "User not authorized.", msg="Unauthorized result check fail")

        # check Unauthorized--delete
        name = "1:marko"
        code, ret = self.auth.delete_vertex(name, auth=self.user)
        self.assertNotEqual(code, 201, msg=ret)
        self.assertEqual(ret["message"], "User not authorized.", msg="Unauthorized result check fail")

    def test_vertex_write_Multiple_11(self):
        """
        vertex 写多个限制属性权限
        :return:
        """
        # add graph
        self.p.init_data("basic")

        # check role
        permission_list = [
            {"target_list": [{"type": "PROPERTY_KEY"}, {"type": "VERTEX_LABEL"}], "permission": "READ",
             "name": "vertexlabel_pro_read"},
            {"target_list": [{"type": "VERTEX", "label": "person",
                              "properties": {"city": "Shanxi", "age": "P.gte(20)"}}],
             "permission": "WRITE", "name": "vertex_write"}
        ]

        user_id = set_auth.post_auth(permission_list)
        code, ret = self.auth.get_users_role(user_id)
        for key, value in ret["roles"][self.graph].items():
            if key == "WRITE":
                self.assertIn(value[0]["type"], "VERTEX", msg="role type check fail")
            elif key == "READ":
                self.assertIn(value[0]["type"], "PROPERTY_KEY", msg="role type check fail")
            elif key == "EXECUTE":
                self.assertIn(value[0]["type"], "GREMLIN", msg="role type check fail")
            else:
                pass

        # check Unauthorized--write
        body = {
            "label": "person",
            "properties": {
                "name": "new1",
                "age": 20,
                "city": "Shanxi"
            }
        }

        code, ret = self.auth.post_vertex(body, auth=self.user)
        self.assertEqual(code, 201, msg=ret)

        # check Authorize--read
        code, ret = self.auth.get_vertex_all(auth=self.user)
        # print code, ret
        self.assertEqual(code, 200, msg=ret)
        self.assertEqual(ret['vertices'], [], msg=ret)

        # check Unauthorized--delete
        name = "1:marko"
        code, ret = self.auth.delete_vertex(name, auth=self.user)
        self.assertNotEqual(code, 201, msg=ret)
        self.assertEqual(ret["message"], "User not authorized.", msg="Unauthorized result check fail")

    def test_vertex_delete_Multiple_12(self):
        """
        vertex 删除多个限制属性权限
        :return:
        """
        # add graph
        self.p.init_data("basic")

        # check role
        permission_list = [
            {"target_list": [{"type": "PROPERTY_KEY"}, {"type": "VERTEX_LABEL"}, {"type": "VERTEX"}],
             "permission": "READ",
             "name": "vertexlabel_pro_read"},
            {"target_list": [
                {"type": "VERTEX", "label": "person",
                 "properties": {"city": "Shanghai", "age": "P.gte(20)"}}],
                "permission": "DELETE", "name": "vertex_delete"}
        ]
        user_id = set_auth.post_auth(permission_list)
        code, ret = self.auth.get_users_role(user_id)
        for key, value in ret["roles"][self.graph].items():
            if key == "DELETE":
                self.assertIn(value[0]["type"], "VERTEX", msg="role type check fail")
            elif key == "READ":
                self.assertIn(value[0]["type"], "PROPERTY_KEY", msg="role type check fail")
                self.assertIn(value[1]["type"], "VERTEX_LABEL", msg="role type check fail")
                self.assertIn(value[2]["type"], "VERTEX", msg="role type check fail")
            else:
                pass

        # check Unauthorized--delete                                               删除定点报没有此顶点ID
        vertex_id = "1:peter"
        # vertex_id = "1:r"
        code, ret = self.auth.delete_vertex(vertex_id, auth=self.user)
        self.assertEqual(code, 204, msg=ret)

        # check Authorize--read
        code, ret = self.auth.get_vertex_all(auth=self.user)
        # print code, ret
        self.assertNotEqual(code, 200, msg=ret)

        # check Unauthorized--write
        body = {
            "label": "person",
            "properties": {
                "name": "marko",
                "age": 56,
                "city": ["Shanxi", "qwe"]

            }
        }
        code, ret = self.auth.post_vertex(body, auth=self.user)
        self.assertNotEqual(code, 201, msg=ret)
        self.assertEqual(ret["message"], "User not authorized.", msg="Unauthorized result check fail")

    def test_vertex_read_Multiple_13(self):

        """
        vertex 读多个限制属性权限-不同的target
        :return:
        """
        # add graph
        self.p.init_data("basic")

        # check role
        permission_list = [
            {"target_list": [{"type": "PROPERTY_KEY"}, {"type": "VERTEX_LABEL"}], "permission": "READ",
             "name": "property_read"},
            {"target_list": [{"type": "VERTEX", "label": "person",
                              "properties": {"city": "Shanxi"}}],
             "permission": "READ",
             "name": "vertex_read_city"},
            {"target_list": [{"type": "VERTEX", "label": "person",
                              "properties": {"age": "P.gte(20)"}}],
             "permission": "READ",
             "name": "vertex_read_age"}
        ]
        user_id = set_auth.post_auth(permission_list)
        code, ret = self.auth.get_users_role(user_id)
        # print ret
        for key, value in ret["roles"][self.graph].items():
            if key == "READ":
                self.assertIn(value[2]["type"], "VERTEX_LABEL", msg="role type check fail")
            else:
                pass

        # check Authorize--read
        code, ret = self.auth.get_vertex_all(auth=self.user)
        self.assertEqual(code, 200, msg=ret)

        # check Unauthorized--write
        body = {
            "label": "person",
            "properties": {
                "name": "marko",
                "age": 45
            }
        }
        code, ret = self.auth.post_vertex(body, auth=self.user)
        self.assertNotEqual(code, 201, msg=ret)
        self.assertEqual(ret["message"], "User not authorized.", msg="Unauthorized result check fail")

        # check Unauthorized--delete
        name = "1:marko"
        code, ret = self.auth.delete_vertex(name, auth=self.user)
        self.assertNotEqual(code, 201, msg=ret)
        self.assertEqual(ret["message"], "User not authorized.", msg="Unauthorized result check fail")

    def test_vertex_write_Multiple_14(self):
        """
        vertex 写多个限制属性权限-不同的target
        :return:
        """
        # add graph
        self.p.init_data("basic")

        # check role
        permission_list = [
            {"target_list": [{"type": "PROPERTY_KEY"}, {"type": "VERTEX_LABEL"}], "permission": "READ",
             "name": "vertexlabel_pro_read"},
            {"target_list": [{"type": "VERTEX", "label": "person",
                              "properties": {"city": "Shanxi"}}],
             "permission": "WRITE", "name": "vertex_write_city"},
            {"target_list": [{"type": "VERTEX", "label": "person",
                              "properties": {"age": "P.gte(20)"}}],
             "permission": "WRITE", "name": "vertex_write_age"}
        ]

        user_id = set_auth.post_auth(permission_list)
        code, ret = self.auth.get_users_role(user_id)
        # print ret
        for key, value in ret["roles"][self.graph].items():
            if key == "WRITE":
                self.assertIn(value[0]["type"], "VERTEX", msg="role type check fail")
            elif key == "READ":
                self.assertIn(value[0]["type"], "PROPERTY_KEY", msg="role type check fail")
            else:
                pass

        # check Unauthorized--write
        body = {
            "label": "person",
            "properties": {
                "name": "new1",
                "age": 20,
                "city": "Shanxi"
            }
        }

        code, ret = self.auth.post_vertex(body, auth=self.user)
        self.assertEqual(code, 201, msg=ret)

        # check Authorize--read
        code, ret = self.auth.get_vertex_all(auth=self.user)
        # print code, ret
        self.assertEqual(code, 200, msg=ret)
        self.assertEqual(ret['vertices'], [], msg=ret)

        # check Unauthorized--delete
        name = "1:marko"
        code, ret = self.auth.delete_vertex(name, auth=self.user)
        self.assertNotEqual(code, 201, msg=ret)
        self.assertEqual(ret["message"], "User not authorized.", msg="Unauthorized result check fail")

    def test_vertex_delete_Multiple_15(self):
        """
        vertex 删除多个限制属性权限-不同的target
        :return:
        """
        # add graph
        self.p.init_data("basic")

        # check role
        permission_list = [
            {"target_list": [{"type": "PROPERTY_KEY"}, {"type": "VERTEX_LABEL"}, {"type": "VERTEX"}],
             "permission": "READ",
             "name": "vertexlabel_pro_read"},
            {"target_list": [
                {"type": "VERTEX", "label": "person",
                 "properties": {"city": "Beijing"}}],
                "permission": "DELETE", "name": "vertex_delete_city"},
            {"target_list": [
                {"type": "VERTEX", "label": "person",
                 "properties": {"age": "P.gte(20)"}}],
                "permission": "DELETE", "name": "vertex_delete_age"}
        ]
        user_id = set_auth.post_auth(permission_list)
        code, ret = self.auth.get_users_role(user_id)
        for key, value in ret["roles"][self.graph].items():
            if key == "DELETE":
                self.assertIn(value[0]["type"], "VERTEX", msg="role type check fail")
            elif key == "READ":
                self.assertIn(value[0]["type"], "PROPERTY_KEY", msg="role type check fail")
                self.assertIn(value[1]["type"], "VERTEX_LABEL", msg="role type check fail")
                self.assertIn(value[2]["type"], "VERTEX", msg="role type check fail")
            else:
                pass

        # check Unauthorized--delete                                               删除定点报没有此顶点ID
        vertex_id = "1:peter"
        # vertex_id = "1:r"
        code, ret = self.auth.delete_vertex(vertex_id, auth=self.user)
        self.assertEqual(code, 204, msg=ret)

        # check Authorize--read
        code, ret = self.auth.get_vertex_all(auth=self.user)
        # print code, ret
        self.assertNotEqual(code, 200, msg=ret)

        # check Unauthorized--write
        body = {
            "label": "person",
            "properties": {
                "name": "marko",
                "age": 56,
                "city": ["Shanxi", "qwe"]

            }
        }
        code, ret = self.auth.post_vertex(body, auth=self.user)
        self.assertNotEqual(code, 201, msg=ret)
        self.assertEqual(ret["message"], "User not authorized.", msg="Unauthorized result check fail")

    def test_edge_pro_single_string_read_16(self):
        """
        edge 读单个限制string属性权限
        :return:
        """
        # add graph
        self.p.init_data("basic")

        # check role
        permission_list = [
            {"target_list": [{"type": "PROPERTY_KEY"},
                             {"type": "VERTEX_LABEL"},
                             {"type": "EDGE_LABEL"},
                             {"type": "EDGE", "label": "created", "properties": {"city": "Shanghai"}}],
             "permission": "READ",
             "name": "edge_read"}
        ]
        user_id = set_auth.post_auth(permission_list)
        code, ret = self.auth.get_users_role(user_id)
        # print ret
        for key, value in ret["roles"][self.graph].items():
            if key == "READ":
                self.assertIn(value[0]["type"], "PROPERTY_KEY", msg="role type check fail")
                self.assertIn(value[1]["type"], "VERTEX_LABEL", msg="role type check fail")
                self.assertIn(value[2]["type"], "EDGE_LABEL", msg="role type check fail")
                self.assertIn(value[3]["type"], "EDGE", msg="role type check fail")
            else:
                pass

                # check Authorize--read
        code, ret = self.auth.get_edge_all(auth=self.user)
        self.assertEqual(code, 200, msg=ret)

        # check Unauthorized--write
        body = {
            "label": "created",
            "outV": "1:peter",
            "inV": "2:lop",
            "outVLabel": "person",
            "inVLabel": "software",
            "properties": {
                "date": "2017-5-18",
                "city": "Shanghai"
            }
        }
        code, ret = self.auth.post_edge(body, auth=self.user)
        self.assertNotEqual(code, 201, msg=ret)
        self.assertEqual(ret["message"], "User not authorized.", msg="Unauthorized result check fail")

        # check Unauthorized--delete
        name = "S1:peter>2>>S2:lop"
        code, ret = self.auth.delete_edge(name, auth=self.user)
        self.assertNotEqual(code, 201, msg=ret)
        self.assertEqual(ret["message"], "User not authorized.", msg="Unauthorized result check fail")

    def test_edge_pro_single_string_read_16_nogremlin(self):
        """
        edge 读单个限制string属性权限
        :return:
        """
        # add graph
        self.p.init_data("basic")

        # check role
        permission_list = [
            {"target_list": [{"type": "PROPERTY_KEY"},
                             {"type": "VERTEX_LABEL"},
                             {"type": "EDGE_LABEL"},
                             {"type": "EDGE", "label": "created", "properties": {"city": "Shanghai"}}],
             "permission": "READ",
             "name": "edge_read"}
        ]
        user_id = set_auth.post_auth(permission_list)
        code, ret = self.auth.get_users_role(user_id)
        for key, value in ret["roles"][self.graph].items():
            if key == "READ":
                self.assertIn(value[0]["type"], "PROPERTY_KEY", msg="role type check fail")
                self.assertIn(value[1]["type"], "VERTEX_LABEL", msg="role type check fail")
                self.assertIn(value[2]["type"], "EDGE_LABEL", msg="role type check fail")
                self.assertIn(value[3]["type"], "EDGE", msg="role type check fail")
            else:
                pass

        # check Authorize--read
        code, ret = self.auth.get_edge_all(auth=self.user)
        self.assertEqual(code, 200, msg=ret)

        # check Unauthorized--write
        body = {
            "label": "created",
            "outV": "1:peter",
            "inV": "2:lop",
            "outVLabel": "person",
            "inVLabel": "software",
            "properties": {
                "date": "2017-5-18",
                "city": "Shanghai"
            }
        }
        code, ret = self.auth.post_edge(body, auth=self.user)
        self.assertNotEqual(code, 201, msg=ret)
        self.assertEqual(ret["message"], "User not authorized.", msg="Unauthorized result check fail")

        # check Unauthorized--delete
        name = "S1:peter>2>>S2:lop"
        code, ret = self.auth.delete_edge(name, auth=self.user)
        self.assertNotEqual(code, 201, msg=ret)
        self.assertEqual(ret["message"], "User not authorized.", msg="Unauthorized result check fail")

    def test_edge_pro_single_string_read_16_noread(self):
        """
        edge 读单个限制string属性权限
        :return:
        """
        # add graph
        self.p.init_data("basic")

        # check role
        permission_list = [
            {"target_list": [{"type": "PROPERTY_KEY"},
                             {"type": "VERTEX_LABEL"},
                             {"type": "EDGE_LABEL"}],
             "permission": "READ",
             "name": "edge_read"}
        ]
        user_id = set_auth.post_auth(permission_list)
        code, ret = self.auth.get_users_role(user_id)
        # print ret
        for key, value in ret["roles"][self.graph].items():
            if key == "READ":
                self.assertIn(value[0]["type"], "PROPERTY_KEY", msg="role type check fail")
                self.assertIn(value[1]["type"], "VERTEX_LABEL", msg="role type check fail")
                self.assertIn(value[2]["type"], "EDGE_LABEL", msg="role type check fail")
            elif key == "EXECUTE":
                self.assertIn(value[0]["type"], "GREMLIN", msg="role type check fail")
            else:
                pass

        # check Authorize--read
        edge_id = "S1:peter>2>>S2:lop"
        code, ret = self.auth.get_edge_all_01(auth=self.user, id=edge_id)
        # print code, ret
        self.assertEqual(code, 400, msg=ret)

        # check Unauthorized--write
        body = {
            "label": "created",
            "outV": "1:peter",
            "inV": "2:lop",
            "outVLabel": "person",
            "inVLabel": "software",
            "properties": {
                "date": "2017-5-18",
                "city": "Shanghai"
            }
        }
        code, ret = self.auth.post_edge(body, auth=self.user)
        self.assertNotEqual(code, 201, msg=ret)
        self.assertEqual(ret["message"], "User not authorized.", msg="Unauthorized result check fail")

        # check Unauthorized--delete
        name = "S1:peter>2>>S2:lop"
        code, ret = self.auth.delete_edge(name, auth=self.user)
        self.assertNotEqual(code, 201, msg=ret)
        self.assertEqual(ret["message"], "User not authorized.", msg="Unauthorized result check fail")

    def test_edge_pro_single_string_write_17(self):
        """
        edge 写单个限制string属性权限
        :return:
        """
        # add graph
        self.p.init_data("basic")

        # check role
        permission_list = [
            {"target_list": [{"type": "PROPERTY_KEY"}, {"type": "VERTEX_LABEL"}, {"type": "EDGE_LABEL"},
                             {"type": "VERTEX"}], "permission": "READ", "name": "vertexlabel_pro_read"},
            {"target_list": [{"type": "EDGE", "label": "created", "properties": {"city": "Shanghai"}}],
             "permission": "WRITE", "name": "edge_write"}
        ]

        user_id = set_auth.post_auth(permission_list)
        code, ret = self.auth.get_users_role(user_id)
        for key, value in ret["roles"][self.graph].items():
            if key == "WRITE":
                self.assertIn(value[0]["type"], "EDGE", msg="role type check fail")
            elif key == "READ":
                self.assertIn(value[0]["type"], "PROPERTY_KEY", msg="role type check fail")
                self.assertIn(value[1]["type"], "VERTEX_LABEL", msg="role type check fail")
                self.assertIn(value[2]["type"], "EDGE_LABEL", msg="role type check fail")
                self.assertIn(value[3]["type"], "VERTEX", msg="role type check fail")

        # check Unauthorized--write
        body = {
            "label": "created",
            "outV": "1:peter",
            "inV": "2:zhao",
            "outVLabel": "person",
            "inVLabel": "software",
            "properties": {
                "city": "Shanghai",
                "date": "2017-5-18"
            }
        }

        code, ret = self.auth.post_edge(body, auth=self.user)
        self.assertEqual(code, 201, msg=ret)

        # check Authorize--read
        code, ret = self.auth.get_edge_all(auth=self.user)
        self.assertNotEqual(code, 200, msg=ret)
        self.assertEqual(ret["message"], "User not authorized.", msg="Unauthorized result check fail")

        # check Unauthorized--delete
        name = "S1:peter>2>>S2:lop"
        code, ret = self.auth.delete_edge(name, auth=self.user)
        self.assertNotEqual(code, 201, msg=ret)
        self.assertEqual(ret["message"], "User not authorized.", msg="Unauthorized result check fail")

    def test_edge_pro_single_string_delete_18(self):
        """
        edge 删除单个限制string属性权限
        :return:
        """
        # add graph
        self.p.init_data("basic")

        # check role
        permission_list = [
            {"target_list": [{"type": "PROPERTY_KEY"}, {"type": "VERTEX_LABEL"}, {"type": "EDGE_LABEL"},
                             {"type": "EDGE"}], "permission": "READ", "name": "vertexlabel_pro_read"},
            {"target_list": [{"type": "EDGE", "label": "created", "properties": {"city": "Beijing"}}],
             "permission": "DELETE", "name": "edge_delete"}
        ]
        user_id = set_auth.post_auth(permission_list)
        code, ret = self.auth.get_users_role(user_id)
        for key, value in ret["roles"][self.graph].items():
            if key == "DELETE":
                self.assertIn(value[0]["type"], "EDGE", msg="role type check fail")
            elif key == "READ":
                self.assertIn(value[0]["type"], "PROPERTY_KEY", msg="role type check fail")
                self.assertIn(value[1]["type"], "VERTEX_LABEL", msg="role type check fail")
                self.assertIn(value[2]["type"], "EDGE_LABEL", msg="role type check fail")
                self.assertIn(value[3]["type"], "EDGE", msg="role type check fail")
            else:
                pass

        # check Unauthorized--delete
        edge_id = "S1:peter>2>>S2:lop"
        code, ret = self.auth.delete_edge(edge_id, auth=self.user)

        self.assertEqual(code, 204)

        # check Authorize--read
        code, ret = self.auth.get_edge_all(auth=self.user)
        self.assertNotEqual(code, 200, msg=ret)

        # check Unauthorized--write
        body = {
            "label": "created",
            "outV": "1:peter",
            "inV": "2:lop",
            "outVLabel": "person",
            "inVLabel": "software",
            "properties": {
                "date": "2017-5-18",
                "city": "Beijing"
            }
        }
        code, ret = self.auth.post_edge(body, auth=self.user)
        self.assertNotEqual(code, 201, msg=ret)
        self.assertEqual(ret["message"], "User not authorized.", msg="Unauthorized result check fail")

    def test_edge_pro_single_int_read_19(self):
        """
        edge 读单个限制int属性权限
        :return:
        """
        # add graph
        self.p.init_data("edge_use")

        # check role
        permission_list = [
            {"target_list": [{"type": "PROPERTY_KEY"},
                             {"type": "VERTEX_LABEL"},
                             {"type": "EDGE_LABEL"},
                             {"type": "EDGE", "label": "knows", "properties": {"price": "P.gte(200)"}}],
             "permission": "READ",
             "name": "edge_read"}
        ]
        user_id = set_auth.post_auth(permission_list)
        code, ret = self.auth.get_users_role(user_id)
        for key, value in ret["roles"][self.graph].items():
            if key == "READ":
                self.assertIn(value[0]["type"], "PROPERTY_KEY", msg="role type check fail")
                self.assertIn(value[1]["type"], "VERTEX_LABEL", msg="role type check fail")
                self.assertIn(value[2]["type"], "EDGE_LABEL", msg="role type check fail")
                self.assertIn(value[3]["type"], "EDGE", msg="role type check fail")
            else:
                pass

        # check Authorize--read
        code, ret = self.auth.get_edge_all(auth=self.user)
        self.assertEqual(code, 200, msg=ret)

        # check Unauthorized--write
        body = {
            "label": "knows",
            "outV": "1:peter",
            "inV": "1:qian",
            "outVLabel": "person",
            "inVLabel": "person",
            "properties": {
                "date": "2017-5-18",
                "price": 234
            }
        }
        code, ret = self.auth.post_edge(body, auth=self.user)
        self.assertNotEqual(code, 201, msg=ret)
        self.assertEqual(ret["message"], "User not authorized.", msg="Unauthorized result check fail")

        # check Unauthorized--delete
        name = "S1:li>1>>S1:wang"
        code, ret = self.auth.delete_edge(name, auth=self.user)
        self.assertNotEqual(code, 204, msg=ret)
        self.assertEqual(ret["message"], "User not authorized.", msg="Unauthorized result check fail")

    def test_edge_pro_single_int_write_20(self):
        """
        edge 写单个限制int属性权限
        :return:
        """
        # add graph
        self.p.init_data("edge_use")

        # check role
        permission_list = [
            {"target_list": [{"type": "PROPERTY_KEY"}, {"type": "VERTEX_LABEL"}, {"type": "EDGE_LABEL"},
                             {"type": "VERTEX"}], "permission": "READ", "name": "vertexlabel_pro_read"},
            {"target_list": [{"type": "EDGE", "label": "knows", "properties": {"price": "P.gte(200)"}}],
             "permission": "WRITE", "name": "edge_write"}
        ]

        user_id = set_auth.post_auth(permission_list)
        code, ret = self.auth.get_users_role(user_id)
        for key, value in ret["roles"][self.graph].items():
            # print key,value
            if key == "WRITE":
                self.assertIn(value[0]["type"], "EDGE", msg="role type check fail")
            elif key == "READ":
                self.assertIn(value[0]["type"], "PROPERTY_KEY", msg="role type check fail")
                self.assertIn(value[1]["type"], "VERTEX_LABEL", msg="role type check fail")
                self.assertIn(value[2]["type"], "EDGE_LABEL", msg="role type check fail")
                self.assertIn(value[3]["type"], "VERTEX", msg="role type check fail")

        # check Unauthorized--write
        body = {
            "label": "knows",
            "outV": "1:peter",
            "inV": "1:qian",
            "outVLabel": "person",
            "inVLabel": "person",
            "properties": {
                "date": "2017-5-18",
                "price": 234
            }
        }

        code, ret = self.auth.post_edge(body, auth=self.user)
        self.assertEqual(code, 201, msg=ret)

        # check Authorize--read
        code, ret = self.auth.get_edge_all(auth=self.user)
        # print code, ret
        self.assertNotEqual(code, 200, msg=ret)
        self.assertEqual(ret["message"], "User not authorized.", msg="Unauthorized result check fail")

        # check Unauthorized--delete
        name = "S1:peter>2>>S2:lop"
        code, ret = self.auth.delete_edge(name, auth=self.user)
        self.assertNotEqual(code, 204, msg=ret)
        self.assertEqual(ret["message"], "User not authorized.", msg="Unauthorized result check fail")

    def test_edge_pro_single_int_delete_21(self):
        """
        edge 删除单个限制int属性权限
        :return:
        """
        # add graph
        self.p.init_data("edge_use")

        # check role
        permission_list = [
            {"target_list": [{"type": "PROPERTY_KEY"}, {"type": "VERTEX_LABEL"}, {"type": "EDGE_LABEL"},
                             {"type": "EDGE"}], "permission": "READ", "name": "vertexlabel_pro_read"},
            {"target_list": [{"type": "EDGE", "label": "knows", "properties": {"price": "P.gte(200)"}}],
             "permission": "DELETE", "name": "vertex_delete"}
        ]
        user_id = set_auth.post_auth(permission_list)
        code, ret = self.auth.get_users_role(user_id)
        for key, value in ret["roles"][self.graph].items():
            if key == "DELETE":
                self.assertIn(value[0]["type"], "EDGE", msg="role type check fail")
            elif key == "READ":
                self.assertIn(value[0]["type"], "PROPERTY_KEY", msg="role type check fail")
                self.assertIn(value[1]["type"], "VERTEX_LABEL", msg="role type check fail")
                self.assertIn(value[2]["type"], "EDGE_LABEL", msg="role type check fail")
                self.assertIn(value[3]["type"], "EDGE", msg="role type check fail")
            else:
                pass

        # check Unauthorized--delete
        edge_id = "S1:marko>1>>S1:josh"
        code, ret = self.auth.delete_edge(edge_id, auth=self.user)
        self.assertEqual(code, 204)

        # check Authorize--read
        code, ret = self.auth.get_edge_all(auth=self.user)
        self.assertNotEqual(code, 200, msg=ret)

        # check Unauthorized--write
        body = {
            "label": "knows",
            "outV": "1:peter",
            "inV": "1:qian",
            "outVLabel": "person",
            "inVLabel": "person",
            "properties": {
                "date": "2017-5-18",
                "price": 234
            }
        }
        code, ret = self.auth.post_edge(body, auth=self.user)
        self.assertNotEqual(code, 201, msg=ret)
        self.assertEqual(ret["message"], "User not authorized.", msg="Unauthorized result check fail")

    def test_edge_pro_list_string_read_22(self):
        """
        edge 读单个限制list属性权限
        :return:
        """
        # add graph
        self.p.init_data("list_pro")

        # check role
        permission_list = [
            {"target_list": [{"type": "PROPERTY_KEY"},
                             {"type": "VERTEX_LABEL"},
                             {"type": "EDGE_LABEL"},
                             {"type": "EDGE", "label": "knows", "properties": {"address": "P.contains(\"北京市海淀区\")"}}],
             "permission": "READ",
             "name": "edge_read"}
        ]
        user_id = set_auth.post_auth(permission_list)
        code, ret = self.auth.get_users_role(user_id)
        for key, value in ret["roles"][self.graph].items():
            if key == "READ":
                self.assertIn(value[0]["type"], "PROPERTY_KEY", msg="role type check fail")
                self.assertIn(value[1]["type"], "VERTEX_LABEL", msg="role type check fail")
                self.assertIn(value[2]["type"], "EDGE_LABEL", msg="role type check fail")
                self.assertIn(value[3]["type"], "EDGE", msg="role type check fail")
            else:
                pass

        # check Authorize--read
        code, ret = self.auth.get_edge_all(auth=self.user)
        self.assertEqual(code, 200, msg=ret)

        # check Unauthorized--write
        body = {
            "label": "knows",
            "outV": "1:peter",
            "inV": "1:qian",
            "outVLabel": "person",
            "inVLabel": "person",
            "properties": {
                "date": "2017-5-18",
                "address": "北京市海淀区"
            }
        }
        code, ret = self.auth.post_edge(body, auth=self.user)
        self.assertNotEqual(code, 201, msg=ret)
        self.assertEqual(ret["message"], "User not authorized.", msg="Unauthorized result check fail")

        # check Unauthorized--delete
        name = "S1:li>1>>S1:wang"
        code, ret = self.auth.delete_edge(name, auth=self.user)
        self.assertNotEqual(code, 204, msg=ret)
        self.assertEqual(ret["message"], "User not authorized.", msg="Unauthorized result check fail")

    def test_edge_pro_list_string_write_23(self):
        """
        edge 写单个限制list属性权限
        :return:
        """
        # add graph
        self.p.init_data("list_pro")

        # check role
        permission_list = [
            {"target_list": [{"type": "PROPERTY_KEY"}, {"type": "VERTEX_LABEL"}, {"type": "EDGE_LABEL"},
                             {"type": "VERTEX"}], "permission": "READ", "name": "vertexlabel_pro_read"},
            {"target_list": [{"type": "EDGE", "label": "knows", "properties": {"address": "P.contains(\"北京市海淀区\")"}}],
             "permission": "WRITE", "name": "edge_write"}
        ]
        user_id = set_auth.post_auth(permission_list)
        code, ret = self.auth.get_users_role(user_id)
        for key, value in ret["roles"][self.graph].items():
            if key == "WRITE":
                self.assertIn(value[0]["type"], "EDGE", msg="role type check fail")
            elif key == "READ":
                self.assertIn(value[0]["type"], "PROPERTY_KEY", msg="role type check fail")
                self.assertIn(value[1]["type"], "VERTEX_LABEL", msg="role type check fail")
                self.assertIn(value[2]["type"], "EDGE_LABEL", msg="role type check fail")
                self.assertIn(value[3]["type"], "VERTEX", msg="role type check fail")

        # check Unauthorized--write
        body = {
            "label": "knows",
            "outV": "1:peter",
            "inV": "1:qian",
            "outVLabel": "person",
            "inVLabel": "person",
            "properties": {
                "date": "2017-5-18",
                "address": "北京市海淀区"
            }
        }

        code, ret = self.auth.post_edge(body, auth=self.user)
        self.assertEqual(code, 201, msg=ret)

        # check Authorize--read
        code, ret = self.auth.get_edge_all(auth=self.user)
        self.assertNotEqual(code, 200, msg=ret)
        self.assertEqual(ret["message"], "User not authorized.", msg="Unauthorized result check fail")

        # check Unauthorized--delete
        name = "S1:marko>1>>S1:vadas"
        code, ret = self.auth.delete_edge(name, auth=self.user)
        self.assertNotEqual(code, 204, msg=ret)
        self.assertEqual(ret["message"], "User not authorized.", msg="Unauthorized result check fail")

    def test_edge_pro_list_string_delete_24(self):
        """
        edge 删除单个限制list属性权限
        :return:
        """
        # add graph
        self.p.init_data("list_pro")

        # check role
        permission_list = [
            {"target_list": [{"type": "PROPERTY_KEY"}, {"type": "VERTEX_LABEL"}, {"type": "EDGE_LABEL"},
                             {"type": "EDGE"}], "permission": "READ", "name": "vertexlabel_pro_read"},
            {"target_list": [{"type": "EDGE", "label": "knows", "properties": {"address": "P.contains(\"北京市海淀区\")"}}],
             "permission": "DELETE", "name": "vertex_delete"}
        ]
        user_id = set_auth.post_auth(permission_list)
        code, ret = self.auth.get_users_role(user_id)
        # print code, ret
        for key, value in ret["roles"][self.graph].items():
            if key == "DELETE":
                self.assertIn(value[0]["type"], "EDGE", msg="role type check fail")
            elif key == "READ":
                self.assertIn(value[0]["type"], "PROPERTY_KEY", msg="role type check fail")
                self.assertIn(value[1]["type"], "VERTEX_LABEL", msg="role type check fail")
                self.assertIn(value[2]["type"], "EDGE_LABEL", msg="role type check fail")
                self.assertIn(value[3]["type"], "EDGE", msg="role type check fail")  # 删除边需要读边的权限（应该不用读的）
            else:
                pass

        # check Unauthorized--delete
        edge_id = "S1:marko>1>>S1:vadas"
        code, ret = self.auth.delete_edge(edge_id, auth=self.user)
        self.assertEqual(code, 204)

        # check Authorize--read
        code, ret = self.auth.get_edge_all(auth=self.user)
        self.assertNotEqual(code, 200, msg=ret)

        # check Unauthorized--write
        body = {
            "label": "knows",
            "outV": "1:peter",
            "inV": "1:qian",
            "outVLabel": "person",
            "inVLabel": "person",
            "properties": {
                "date": "2017-5-18",
                "address": "北京市海淀区"
            }
        }
        code, ret = self.auth.post_edge(body, auth=self.user)
        self.assertNotEqual(code, 201, msg=ret)
        self.assertEqual(ret["message"], "User not authorized.", msg="Unauthorized result check fail")

    def test_edge_pro_read_Multiple_25(self):
        """
        edge 读多个限制属性权限
        :return:
        """
        # add graph
        self.p.init_data("edge_use")

        # check role
        permission_list = [
            {"target_list": [{"type": "PROPERTY_KEY"},
                             {"type": "VERTEX_LABEL"},
                             {"type": "EDGE_LABEL"},
                             {"type": "EDGE", "label": "knows",
                              "properties": {"date": "20160110", "price": "P.gte(400)"}}],
             "permission": "READ",
             "name": "edge_read"}
        ]
        user_id = set_auth.post_auth(permission_list)
        code, ret = self.auth.get_users_role(user_id)
        for key, value in ret["roles"][self.graph].items():
            if key == "READ":
                self.assertIn(value[0]["type"], "PROPERTY_KEY", msg="role type check fail")
                self.assertIn(value[1]["type"], "VERTEX_LABEL", msg="role type check fail")
                self.assertIn(value[2]["type"], "EDGE_LABEL", msg="role type check fail")
                self.assertIn(value[3]["type"], "EDGE", msg="role type check fail")
            else:
                pass

        # check Authorize--read
        code, ret = self.auth.get_edge_all(auth=self.user)
        self.assertEqual(code, 200, msg=ret)

        # check Unauthorized--write
        body = {
            "label": "knows",
            "outV": "1:peter",
            "inV": "1:qian",
            "outVLabel": "person",
            "inVLabel": "person",
            "properties": {
                "date": "20170518",
                "price": 567
            }
        }
        code, ret = self.auth.post_edge(body, auth=self.user)
        self.assertNotEqual(code, 201, msg=ret)
        self.assertEqual(ret["message"], "User not authorized.", msg="Unauthorized result check fail")

        # check Unauthorized--delete
        name = "S1:li>1>>S1:wang"
        code, ret = self.auth.delete_edge(name, auth=self.user)
        self.assertNotEqual(code, 204, msg=ret)
        self.assertEqual(ret["message"], "User not authorized.", msg="Unauthorized result check fail")

    def test_edge_pro_write_Multiple_26(self):
        """
        edge 写多个限制属性权限
        :return:
        """
        # add graph
        self.p.init_data("edge_use")

        # check role
        permission_list = [
            {"target_list": [{"type": "PROPERTY_KEY"}, {"type": "VERTEX_LABEL"}, {"type": "EDGE_LABEL"},
                             {"type": "VERTEX"}], "permission": "READ", "name": "vertexlabel_pro_read"},
            {"target_list": [
                {"type": "EDGE", "label": "knows", "properties": {"date": "20160110", "price": "P.gte(400)"}}],
                "permission": "WRITE", "name": "vertex_write"}
        ]
        user_id = set_auth.post_auth(permission_list)
        code, ret = self.auth.get_users_role(user_id)
        for key, value in ret["roles"][self.graph].items():
            if key == "WRITE":
                self.assertIn(value[0]["type"], "EDGE", msg="role type check fail")
            elif key == "READ":
                self.assertIn(value[0]["type"], "PROPERTY_KEY", msg="role type check fail")
                self.assertIn(value[1]["type"], "VERTEX_LABEL", msg="role type check fail")
                self.assertIn(value[2]["type"], "EDGE_LABEL", msg="role type check fail")
                self.assertIn(value[3]["type"], "VERTEX", msg="role type check fail")

        # check Unauthorized--write
        body = {
            "label": "knows",
            "outV": "1:peter",
            "inV": "1:qian",
            "outVLabel": "person",
            "inVLabel": "person",
            "properties": {
                "date": "20170518",
                "price": 567
            }
        }

        code, ret = self.auth.post_edge(body, auth=self.user)
        self.assertEqual(code, 201, msg=ret)

        # check Authorize--read
        code, ret = self.auth.get_edge_all(auth=self.user)
        self.assertNotEqual(code, 200, msg=ret)
        self.assertEqual(ret["message"], "User not authorized.", msg="Unauthorized result check fail")

        # check Unauthorized--delete
        name = "S1:li>1>>S1:wang"
        code, ret = self.auth.delete_edge(name, auth=self.user)
        self.assertNotEqual(code, 204, msg=ret)
        self.assertEqual(ret["message"], "User not authorized.", msg="Unauthorized result check fail")

    def test_edge_pro_delete_Multiple_27(self):
        """
        edge 删除多个限制属性权限
        :return:
        """
        # add graph
        self.p.init_data("edge_use")

        # check role
        permission_list = [
            {"target_list": [{"type": "PROPERTY_KEY"}, {"type": "VERTEX_LABEL"}, {"type": "EDGE_LABEL"},
                             {"type": "EDGE"}], "permission": "READ", "name": "vertexlabel_pro_read"},
            {"target_list": [
                {"type": "EDGE", "label": "knows", "properties": {"date": "20160110", "price": "P.gte(400)"}}],
                "permission": "DELETE", "name": "vertex_delete"}
        ]
        user_id = set_auth.post_auth(permission_list)
        code, ret = self.auth.get_users_role(user_id)
        for key, value in ret["roles"][self.graph].items():
            if key == "DELETE":
                self.assertIn(value[0]["type"], "EDGE", msg="role type check fail")
            elif key == "READ":
                self.assertIn(value[0]["type"], "PROPERTY_KEY", msg="role type check fail")
                self.assertIn(value[1]["type"], "VERTEX_LABEL", msg="role type check fail")
                self.assertIn(value[2]["type"], "EDGE_LABEL", msg="role type check fail")
                self.assertIn(value[3]["type"], "EDGE", msg="role type check fail")
            else:
                pass

        # check Unauthorized--delete
        edge_id = "S1:li>1>>S1:wang"
        code, ret = self.auth.delete_edge(edge_id, auth=self.user)
        self.assertEqual(code, 204)

        # check Authorize--read
        code, ret = self.auth.get_edge_all(auth=self.user)
        # print code, ret
        self.assertNotEqual(code, 200, msg=ret)

        # check Unauthorized--write
        body = {
            "label": "knows",
            "outV": "1:peter",
            "inV": "1:qian",
            "outVLabel": "person",
            "inVLabel": "person",
            "properties": {
                "date": "20170518",
                "price": 567
            }
        }
        code, ret = self.auth.post_edge(body, auth=self.user)
        self.assertNotEqual(code, 201, msg=ret)
        self.assertEqual(ret["message"], "User not authorized.", msg="Unauthorized result check fail")

    def test_edge_read_Multiple_28(self):

        """
        EDGE 读多个限制属性权限-不同的target
        :return:
        """
        # add graph
        self.p.init_data("edge_use")

        # check role
        permission_list = [
            {"target_list": [{"type": "PROPERTY_KEY"}, {"type": "VERTEX_LABEL"}, {"type": "EDGE_LABEL"}],
             "permission": "READ", "name": "property_read"},
            {"target_list": [{"type": "EDGE", "label": "knows",
                              "properties": {"date": "20160110"}}],
             "permission": "READ",
             "name": "edge_read_date"},
            {"target_list": [{"type": "EDGE", "label": "knows",
                              "properties": {"price": "P.gte(400)"}}],
             "permission": "READ",
             "name": "edge_read_price"}
        ]
        user_id = set_auth.post_auth(permission_list)
        code, ret = self.auth.get_users_role(user_id)
        # print ret
        for key, value in ret["roles"][self.graph].items():
            if key == "READ":
                self.assertIn(value[0]["type"], "PROPERTY_KEY", msg="role type check fail")
                self.assertIn(value[1]["type"], "VERTEX_LABEL", msg="role type check fail")
                self.assertIn(value[2]["type"], "EDGE_LABEL", msg="role type check fail")
                self.assertIn(value[3]["type"], "EDGE", msg="role type check fail")
                self.assertIn(value[3]["properties"]["date"], "20160110", msg="role type check fail")
                self.assertIn(value[4]["type"], "EDGE", msg="role type check fail")
                self.assertIn(value[4]["properties"]["price"], "P.gte(400)", msg="role type check fail")
            else:
                pass

        # check Authorize--read
        code, ret = self.auth.get_edge_all(auth=self.user)
        self.assertEqual(code, 200, msg=ret)

        # check Unauthorized--write
        body = {
            "label": "knows",
            "outV": "1:peter",
            "inV": "1:qian",
            "outVLabel": "person",
            "inVLabel": "person",
            "properties": {
                "date": "20170518",
                "price": 567
            }
        }
        code, ret = self.auth.post_edge(body, auth=self.user)
        self.assertNotEqual(code, 201, msg=ret)
        self.assertEqual(ret["message"], "User not authorized.", msg="Unauthorized result check fail")

        # check Unauthorized--delete
        name = "S1:li>1>>S1:wang"
        code, ret = self.auth.delete_edge(name, auth=self.user)
        self.assertNotEqual(code, 204, msg=ret)
        self.assertEqual(ret["message"], "User not authorized.", msg="Unauthorized result check fail")

    def test_edge_write_Multiple_29(self):
        """
        vertex 写多个限制属性权限-不同的target
        :return:
        """
        # add graph
        self.p.init_data("edge_use")

        # check role
        permission_list = [
            {"target_list": [{"type": "PROPERTY_KEY"}, {"type": "VERTEX_LABEL"}, {"type": "EDGE_LABEL"},
                             {"type": "VERTEX"}], "permission": "READ",
             "name": "edgelabel_pro_read"},
            {"target_list": [{"type": "EDGE", "label": "knows",
                              "properties": {"date": "20160110"}}],
             "permission": "WRITE", "name": "edge_write_date"},
            {"target_list": [{"type": "EDGE", "label": "knows",
                              "properties": {"price": "P.gte(400)"}}],
             "permission": "WRITE", "name": "edge_write_price"}
        ]

        user_id = set_auth.post_auth(permission_list)
        code, ret = self.auth.get_users_role(user_id)
        # print ret
        for key, value in ret["roles"][self.graph].items():
            print(key, value)
            if key == "WRITE":
                self.assertIn(value[0]["type"], "EDGE", msg="role type check fail")
                self.assertIn(value[0]["properties"]["date"], "20160110", msg="role type check fail")
                self.assertIn(value[1]["type"], "EDGE", msg="role type check fail")
                self.assertIn(value[1]["properties"]["price"], "P.gte(400)", msg="role type check fail")
            elif key == "READ":
                self.assertIn(value[0]["type"], "PROPERTY_KEY", msg="role type check fail")
                self.assertIn(value[1]["type"], "VERTEX_LABEL", msg="role type check fail")
                self.assertIn(value[2]["type"], "EDGE_LABEL", msg="role type check fail")
                self.assertIn(value[3]["type"], "VERTEX", msg="role type check fail")
            else:
                pass

        # check Unauthorized--write
        body = {
            "label": "knows",
            "outV": "1:peter",
            "inV": "1:qian",
            "outVLabel": "person",
            "inVLabel": "person",
            "properties": {
                "date": "20160110",
                "price": 567
            }
        }

        code, ret = self.auth.post_edge(body, auth=self.user)
        self.assertEqual(code, 201, msg=ret)

        # check Authorize--read
        code, ret = self.auth.get_edge_all(auth=self.user)
        self.assertEqual(code, 200, msg=ret)
        self.assertEqual(ret['edges'], [], msg=ret)

        # check Unauthorized--delete
        name = "1:marko"
        code, ret = self.auth.delete_edge(name, auth=self.user)
        self.assertNotEqual(code, 204, msg=ret)
        self.assertEqual(ret["message"], "User not authorized.", msg="Unauthorized result check fail")

    def test_edge_delete_Multiple_30(self):
        """
        vertex 删除多个限制属性权限-不同的target
        :return:
        """
        # add graph
        self.p.init_data("edge_use")

        # check role
        permission_list = [
            {"target_list": [{"type": "PROPERTY_KEY"}, {"type": "VERTEX_LABEL"}, {"type": "EDGE_LABEL"},
                             {"type": "EDGE"}], "permission": "READ",
             "name": "vertexlabel_pro_read"},
            {"target_list": [{"type": "EDGE", "label": "knows",
                              "properties": {"date": "20160110"}}],
             "permission": "DELETE", "name": "edge_delete_date"},
            {"target_list": [{"type": "EDGE", "label": "knows",
                              "properties": {"price": "P.gte(400)"}}],
             "permission": "DELETE", "name": "edge_delete_price"},
        ]
        user_id = set_auth.post_auth(permission_list)
        code, ret = self.auth.get_users_role(user_id)
        for key, value in ret["roles"][self.graph].items():
            if key == "DELETE":
                self.assertIn(value[0]["type"], "EDGE", msg="role type check fail")
                self.assertIn(value[0]["properties"]["date"], "20160110", msg="role type check fail")
                self.assertIn(value[1]["type"], "EDGE", msg="role type check fail")
                self.assertIn(value[1]["properties"]["price"], "P.gte(400)", msg="role type check fail")
            elif key == "READ":
                self.assertIn(value[0]["type"], "PROPERTY_KEY", msg="role type check fail")
                self.assertIn(value[1]["type"], "VERTEX_LABEL", msg="role type check fail")
                self.assertIn(value[2]["type"], "EDGE_LABEL", msg="role type check fail")
                self.assertIn(value[3]["type"], "EDGE", msg="role type check fail")
            else:
                pass

        # check Unauthorized--delete
        edge_id = "S1:o>1>>S1:s"
        code, ret = self.auth.delete_edge(edge_id, auth=self.user)
        self.assertEqual(code, 204, msg=ret)

        # check Authorize--read
        code, ret = self.auth.get_edge_all(auth=self.user)
        self.assertEqual(code, 200, msg=ret)
        self.assertEqual(ret['edges'], [], msg=ret)

        # check Unauthorized--write
        body = {
            "label": "knows",
            "outV": "1:peter",
            "inV": "1:qian",
            "outVLabel": "person",
            "inVLabel": "person",
            "properties": {
                "date": "20160110",
                "price": 567
            }
        }
        code, ret = self.auth.post_edge(body, auth=self.user)
        self.assertNotEqual(code, 201, msg=ret)
        self.assertEqual(ret["message"], "User not authorized.", msg="Unauthorized result check fail")

    def test_edge_delete_Multiple_30_noread(self):
        """
        vertex 删除多个限制属性权限-不同的target
        :return:
        """
        # add graph
        self.p.init_data("edge_use")

        # check role
        permission_list = [
            {"target_list": [{"type": "PROPERTY_KEY"}, {"type": "VERTEX_LABEL"}, {"type": "EDGE_LABEL"}],
             "permission": "READ",
             "name": "vertexlabel_pro_read"},
            {"target_list": [{"type": "EDGE", "label": "knows",
                              "properties": {"date": "20160110"}}],
             "permission": "DELETE", "name": "edge_delete_date"},
            {"target_list": [{"type": "EDGE", "label": "knows",
                              "properties": {"price": "P.gte(400)"}}],
             "permission": "DELETE", "name": "edge_delete_price"},
        ]
        user_id = set_auth.post_auth(permission_list)
        code, ret = self.auth.get_users_role(user_id)
        for key, value in ret["roles"][self.graph].items():
            if key == "DELETE":
                self.assertIn(value[0]["type"], "EDGE", msg="role type check fail")
                self.assertIn(value[0]["properties"]["date"], "20160110", msg="role type check fail")
                self.assertIn(value[1]["type"], "EDGE", msg="role type check fail")
                self.assertIn(value[1]["properties"]["price"], "P.gte(400)", msg="role type check fail")
            elif key == "READ":
                self.assertIn(value[0]["type"], "PROPERTY_KEY", msg="role type check fail")
                self.assertIn(value[1]["type"], "VERTEX_LABEL", msg="role type check fail")
                self.assertIn(value[2]["type"], "EDGE_LABEL", msg="role type check fail")
            else:
                pass

        # check Unauthorized--delete                                               删除定点报没有此顶点ID
        edge_id = "S1:o>1>>S1:s"
        code, ret = self.auth.delete_edge(edge_id, auth=self.user)
        self.assertEqual(code, 204, msg=ret)

        # check Authorize--read
        code, ret = self.auth.get_edge_all(auth=self.user)
        # print code, ret
        self.assertEqual(code, 200, msg=ret)
        self.assertEqual(ret['edges'], [], msg=ret)

        # check Unauthorized--write
        body = {
            "label": "knows",
            "outV": "1:peter",
            "inV": "1:qian",
            "outVLabel": "person",
            "inVLabel": "person",
            "properties": {
                "date": "20160110",
                "price": 567
            }
        }
        code, ret = self.auth.post_edge(body, auth=self.user)
        self.assertNotEqual(code, 201, msg=ret)
        self.assertEqual(ret["message"], "User not authorized.", msg="Unauthorized result check fail")

    def test_root_read_00(self):

        """
        EDGE 读多个限制属性权限-不同的target
        :return:
        """
        # add graph
        self.p.init_data("basic")

        # check role
        permission_list = [
            {"target_list": [{"type": "ALL"}], "permission": "READ", "name": "property_read"},
            {"target_list": [{"type": "ALL"}], "permission": "DELETE", "name": "root_delete"},
            {"target_list": [{"type": "ALL"}], "permission": "WRITE", "name": "root_write"},
            # {"target_list": [{"type": "ALL"}],"permission": "READ","name": "property_read"},
            # {"target_list": [{"type": "TASK"}],"permission": "DELETE","name": "delete_task"},
            {"target_list": [{"type": "GREMLIN"}, {"type": "TASK"}], "permission": "EXECUTE", "name": "gremlin"}
            # 此权限不应该添加
        ]
        user_id = set_auth.post_auth(permission_list)
        code, ret = self.auth.get_users_role(user_id)
        # print ret
        for key, value in ret["roles"][self.graph].items():
            if key == "READ":
                # self.assertIn(value[0]["type"], "ROOT", msg="role type check fail")
                self.assertIn(value[0]["type"], "ALL", msg="role type check fail")
                # self.assertIn(value[1]["type"], "VERTEX_LABEL", msg="role type check fail")
                # self.assertIn(value[2]["type"], "EDGE_LABEL", msg="role type check fail")
                # self.assertIn(value[3]["type"], "EDGE", msg="role type check fail")
                # self.assertIn(value[3]["properties"]["date"], "20160110", msg="role type check fail")
                # self.assertIn(value[4]["type"], "EDGE", msg="role type check fail")
                # self.assertIn(value[4]["properties"]["price"], "P.gte(400)", msg="role type check fail")
            elif key == "EXECUTE":
                self.assertIn(value[0]["type"], "GREMLIN", msg="role type check fail")
                self.assertIn(value[1]["type"], "TASK", msg="role type check fail")
            elif key == "DELETE":
                # self.assertIn(value[0]["type"], "ROOT", msg="role type check fail")
                self.assertIn(value[0]["type"], "ALL", msg="role type check fail")
            elif key == "WRITE":
                # self.assertIn(value[0]["type"], "ROOT", msg="role type check fail")
                self.assertIn(value[0]["type"], "ALL", msg="role type check fail")
            else:
                pass

        # check Authorize--read
        self.auth.get_edge_all(auth=self.user)
        self.auth.get_edge_allLabel(auth=self.user)
        self.auth.get_vertex_all(auth=self.user)
        self.auth.get_edge_allLabel(auth=self.user)
        self.auth.get_accesses(auth=self.user)
        self.auth.get_users(auth=self.user)
        self.auth.get_groups(auth=self.user)
        self.auth.delete_EdgeLabel(auth=self.user, name="tree")  # 删除边类型
        self.auth.get_task_all(auth=self.user)
        # print code, ret
        body = {
            "gremlin": "g.V()",
            "bindings": {},
            "language": "gremlin-groovy",
            "aliases": {
                "graph": "hugegraph",
                "g": "__g_hugegraph"

            }
        }
        code, ret = self.auth.post_gremlin(auth=self.user, body=body)
        # print code, ret
        self.assertEqual(code, 200, msg=ret)

    def test_task_read_01(self):
        """
        EDGE 读多个限制属性权限-不同的target
        :return:
        """
        # add graph
        self.p.init_data("basic")

        # check role
        permission_list = [
            {"target_list": [{"type": "TASK"}], "permission": "READ", "name": "task_read"},
            {"target_list": [{"type": "TASK"}], "permission": "EXECUTE", "name": "task_e"},
            # {"target_list": [{"type": "ALL"}], "permission": "DELETE", "name": "root_delete"},
            {"target_list": [{"type": "TASK"}], "permission": "WRITE", "name": "root_write"},
            # # {"target_list": [{"type": "ALL"}],"permission": "READ","name": "property_read"},
            # # {"target_list": [{"type": "TASK"}],"permission": "DELETE","name": "delete_task"},
            {"target_list": [{"type": "GREMLIN"}, {"type": "TASK"}], "permission": "EXECUTE", "name": "gremlin"}

            # 此权限不应该添加
        ]
        user_id = set_auth.post_auth(permission_list)
        code, ret = self.auth.get_users_role(user_id)
        # print ret
        for key, value in ret["roles"][self.graph].items():
            if key == "READ":
                # self.assertIn(value[0]["type"], "ROOT", msg="role type check fail")
                self.assertIn(value[0]["type"], "TASK", msg="role type check fail")
                # self.assertIn(value[1]["type"], "VERTEX_LABEL", msg="role type check fail")
                # self.assertIn(value[2]["type"], "EDGE_LABEL", msg="role type check fail")
                # self.assertIn(value[3]["type"], "EDGE", msg="role type check fail")
                # self.assertIn(value[3]["properties"]["date"], "20160110", msg="role type check fail")
                # self.assertIn(value[4]["type"], "EDGE", msg="role type check fail")
                # self.assertIn(value[4]["properties"]["price"], "P.gte(400)", msg="role type check fail")
            elif key == "EXECUTE":
                # self.assertIn(value[0]["type"], "GREMLIN", msg="role type check fail")
                self.assertIn(value[0]["type"], "TASK", msg="role type check fail")
            elif key == "DELETE":
                # self.assertIn(value[0]["type"], "ROOT", msg="role type check fail")
                self.assertIn(value[0]["type"], "ALL", msg="role type check fail")
            elif key == "WRITE":
                # self.assertIn(value[0]["type"], "ROOT", msg="role type check fail")
                self.assertIn(value[0]["type"], "TASK", msg="role type check fail")
            else:
                pass

        # check Authorize--read
        body = {
            "gremlin": "g.V('1:marko')",
            "bindings": {},
            "language": "gremlin-groovy",
            "aliases": {
                # "graph": "hugegraph",
                # "g": "__g_hugegraph"
            }
        }
        self.auth.post_job_gremlin(auth=self.user, body=body)
        # print code, ret
        # code, ret = self.auth.delete_EdgeLabel(auth=self.user, name="tree")  # 删除边类型
        code, ret = self.auth.get_task_all(auth=self.user)
        # print code, ret
        self.assertEqual(code, 200, msg=ret)

        # # check Unauthorized--write
        # body = {
        #     "label": "knows",
        #     "outV": "1:peter",
        #     "inV": "1:qian",
        #     "outVLabel": "person",
        #     "inVLabel": "person",
        #     "properties": {
        #         "date": "20170518",
        #         "price": 567
        #     }
        # }
        # code, ret = self.auth.post_edge(body, auth=self.user)
        # self.assertNotEqual(code, 201, msg=ret)
        # self.assertEqual(ret["message"], "User not authorized.", msg="Unauthorized result check fail")
        # 
        #
        # # check Unauthorized--delete
        # name = "S1:li>1>>S1:wang"
        # code, ret = self.auth.delete_edge(name, auth=self.user)
        # self.assertNotEqual(code, 204, msg=ret)
        # self.assertEqual(ret["message"], "User not authorized.", msg="Unauthorized result check fail")
        # 

    def test_edge_gremlin(self):
        """
        edge 用g.V()读单个限制string属性权限
        :return:
        """
        # add graph
        self.p.init_data("basic")

        # check role
        permission_list = [
            {"target_list": [{"type": "PROPERTY_KEY"},
                             {"type": "VERTEX_LABEL"},
                             {"type": "EDGE_LABEL"},
                             {"type": "EDGE", "label": "created", "properties": {"city": "Shanghai"}}],
             "permission": "READ",
             "name": "edge_read"},
            {"target_list": [{"type": "GREMLIN"}], "permission": "EXECUTE", "name": "gremlin"}
        ]
        user_id = set_auth.post_auth(permission_list)
        code, ret = self.auth.get_users_role(user_id)
        for key, value in ret["roles"][self.graph].items():
            if key == "READ":
                self.assertIn(value[0]["type"], "PROPERTY_KEY", msg="role type check fail")
                self.assertIn(value[1]["type"], "VERTEX_LABEL", msg="role type check fail")
                self.assertIn(value[2]["type"], "EDGE_LABEL", msg="role type check fail")
                self.assertIn(value[3]["type"], "EDGE", msg="role type check fail")
            elif key == "EXECUTE":
                self.assertIn(value[0]["type"], "GREMLIN", msg="role type check fail")
            else:
                pass

        # check Authorize--read
        body = {
            "gremlin": "g.E()",
            "bindings": {},
            "language": "gremlin-groovy",
            "aliases": {
                "graph": "hugegraph",
                "g": "__g_hugegraph"

            }
        }
        code, ret = self.auth.post_gremlin(auth=self.user, body=body)
        self.assertEqual(code, 200, msg=ret)

        # check Unauthorized--write
        body = {
            "label": "created",
            "outV": "1:peter",
            "inV": "2:lop",
            "outVLabel": "person",
            "inVLabel": "software",
            "properties": {
                "date": "2017-5-18",
                "city": "Shanghai"
            }
        }
        code, ret = self.auth.post_edge(body, auth=self.user)
        self.assertNotEqual(code, 201, msg=ret)
        self.assertEqual(ret["message"], "User not authorized.", msg="Unauthorized result check fail")

        # check Unauthorized--delete
        name = "S1:peter>2>>S2:lop"
        code, ret = self.auth.delete_edge(name, auth=self.user)
        self.assertNotEqual(code, 201, msg=ret)
        self.assertEqual(ret["message"], "User not authorized.", msg="Unauthorized result check fail")


if __name__ == '__main__':
    # # run all cases
    # unittest.main(verbosity=2)

    # run one case
    suite = unittest.TestSuite()
    suite.addTest(TestDetailAuth("test_vertex_pro_single_string_write_02"))
    runner = unittest.TextTestRunner()
    runner.run(suite)
