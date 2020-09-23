# -*- coding:utf-8 -*-
"""
author     : lxb
note       : 设置用户的多种权限
create_time: 2020/4/22 5:17 下午
"""
import sys
import os
import time
import json
import importlib

sys.path.append('%s/..' % os.path.split(os.path.realpath(__file__))[0])
sys.path.append('../../')
importlib.reload(sys)

from IntegrationTest.graphTest.serverTest.common.hugegraph_api.auth_api import Auths
from IntegrationTest.graphTest.serverTest.common.hugegraph_api.basic_cls import BasicClassMethod
from IntegrationTest.graphTest.serverTest.common.config.produce_data import ProduceData


class AuthBody(object):
    """
    权限公共方法
    """

    def __init__(self):
        """初始化"""
        self.auth = Auths()
        self.target_graph = BasicClassMethod().graph
        self.target_url = BasicClassMethod().host + ":" + str(BasicClassMethod().port)
        self.name = "graphTest"
        self.pw = "123456"

    def create_target(self, target_list, name):
        """
        创建资源
        """
        body = {
            "target_name": name + "_target",
            "target_graph": self.target_graph,
            "target_url": self.target_url,
            "target_resources": target_list
        }
        code, ret = self.auth.post_targets(body)
        return ret["id"]

    def create_group(self, name):
        """创建组"""
        body = {
            "group_name": name + "_group",
            "group_description": "%s graphTest" % (name + "_group")
        }
        code, ret = self.auth.post_groups(body)
        return ret["id"]

    def create_access(self, group, target, premission):
        """创建group到target的连接"""
        body = {
            "group": group,
            "target": target,
            "access_permission": premission
        }
        code, ret = self.auth.post_accesses(body)
        return ret["id"]

    def create_user(self):
        """创建用户user"""
        body = {
            "user_name": self.name,
            "user_password": self.pw,
        }
        code, ret = self.auth.post_users(body)
        return ret["id"]

    def create_belong(self, user, group):
        """创建用户的授权"""
        body = {
            "user": user,
            "group": group,
        }
        code, ret = self.auth.post_belongs(body)

    def get_user_role(self, user_id, permission, type):
        """获取用户role"""
        code, ret = self.auth.get_users_role(user_id)
        for key, value in ret["roles"]["algorithm"].items():
            if key == permission:
                print ("permission check pass: %s" % key)
            else:
                print ("permission check fail")
            if value[0]["type"] == type:
                print ("type check pass: %s" % value[0]["type"])
            else:
                print ("type check fail")

    def create_auth(self, type_list, permission, target_name="target_name",
                    groupname="group_test", name="test001", pw="123456"):
        """创建一个用户，并为其指定权限"""
        target_id = self.create_target(type_list, target_name)
        group_id = self.create_group(groupname)
        access_id = self.create_access(group_id, target_id, permission)
        user_id = self.create_user(name, pw)
        self.create_belong(user_id, group_id)
        return user_id

    def get_taskid(self, id, auth):
        """
        通过id获取详情，并返回详情数据供下一步做校验
        :param id:
        :return:
        """
        code, ret = self.auth.get_tasks(id, auth)
        for i in range(10):
            if code == 200:
                if ret["task_status"] == "failed":
                    return ret["task_status"], ret
                elif ret["task_status"] == "success":
                    result = json.loads(ret["task_result"])
                    return ret["task_status"], result
                else:
                    time.sleep(10)
                    code, ret = self.auth.get_tasks(id, auth)


def post_auth(auth_list):
    """
    处理给用户赋权
    :param auth_json:
    """
    auth_body = AuthBody()
    user_id = auth_body.create_user()
    # print ("user_id --- " + user_id)
    for each in auth_list:
        target_id = auth_body.create_target(each["target_list"], each["name"])
        # print ("target_id --- " + target_id)
        group_id = auth_body.create_group(each["name"])
        # print ("group_id --- " + group_id)
        access_id = auth_body.create_access(group_id, target_id, each["permission"])
        # print ("access_id --- " + access_id)
        auth_body.create_belong(user_id, group_id)
    return user_id


if __name__ == '__main__':
    code, ret = ProduceData().init_data("clear")
    permission_list = [
        {"target_list": [{"type": "STATUS"}], "permission": "READ", "name": "status_read"}
    ]
    post_auth(permission_list)
