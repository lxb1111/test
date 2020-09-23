# -*- coding:utf-8 -*-
"""
author     : lxb
note       : 
create_time: 2020/4/22 5:17 下午
"""
import requests


if __name__ == "__main__":
    url = "http://yq01-m02-kafka02.yq01.baidu.com:8384/gremlin"
    payload = {
        "gremlin": "g.V().limit(3)",
        "bindings": {},
        "language": "gremlin-groovy",
        "aliases": {
            "graph": "movie",
            "g": "__g_movie"
        }
    }
    response = requests.request("POST", url, json=payload)
    print(response.text)
