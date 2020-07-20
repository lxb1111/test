# -*- coding:utf-8 -*-
"""
author     : lxb
note       : graph组件的配置-部署方式（wget,git）分别为：人工获取,wget官网获取包,GitHub自己拉代码打包
create_time: 2020/4/22 5:17 下午
"""
server = {
    "mode": "git",
    "wget": "https://github.com/hugegraph/hugegraph/releases/download/v0.10.4/hugegraph-0.10.4.tar.gz",
    "git": "https://github.com/hugegraph/hugegraph.git",
    "branch": "release-0.11",
    "graph": {
        "server_host": "127.0.0.1",
        "server_port": 8066,
        "gremlin_port": 8056,
    }
}


loader = {
    "mode": "git",
    "wget": "https://github.com/hugegraph/hugegraph-loader/releases/download/v0.10.0/hugegraph-loader-0.10.0.tar.gz",
    "git": "https://github.com/hugegraph/hugegraph-loader.git",
    "branch": "release-0.10.1"
}


tools = {
    "mode": "git",
    "wget": "https://github.com/hugegraph/hugegraph-tools/releases/download/v1.4.0/hugegraph-tools-1.4.0.tar.gz",
    "git": "https://github.com/hugegraph/hugegraph-tools.git",
    "branch": "release-1.4.0"
}


hubble = {
    "mode": "git",
    "wget": "",
    "git": "https://github.com/hugegraph/hugegraph-hubble.git",
    "host": "127.0.0.1",
    "branch": "master",
    "host": "127.0.0.1",
    "port": 8088
}


