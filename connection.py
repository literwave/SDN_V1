#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020-07-28 21:46
# @Author : Curry
# @Site : https://github.com/zengxiaobo2000/SDN_V1
# @File : connection.py
# @Software: PyCharm


from netmiko import ConnectHandler
from ncclient import manager
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import requests, json

# 忽略ssh警告连接
requests.packages.urllib3.disable_warnings()
# 构造头部信息
headers = {"Accept": "application/yang-data+json",
           "Content-type": "application/yang-data+json"
           }
# 验证信息
remoteInfo = ("cisco", "cisco123!")
# 设备地址
devices = ["192.168.0.101", "192.168.0.103", "192.168.0.107"]


def connection():
    """

    :return: 连接字典
    """
    s_connect = []
    m_connect = []
    r_connect = []
    cnt = 0
    for i in range(0, len(devices)):
        try:
            # ssh cli session
            sshCli = ConnectHandler(device_type='cisco_ios',
                                    host=devices[i], port=22,
                                    username=remoteInfo[0],
                                    password=remoteInfo[1])

            # NETCONF session
            m = manager.connect(
                host=devices[i],
                port=830,
                username=remoteInfo[0],
                password=remoteInfo[1],
                hostkey_verify=False
            )

            # RESTCONF session
            api_url = "https://{}/restconf/data/ietf-interfaces:interfaces".format(devices[i])
            resp = requests.get(api_url, auth=remoteInfo, headers=headers, verify=False)
            s_connect.append(sshCli)
            m_connect.append(m)
            r_connect.append(resp)
        except Exception as e:
            cnt += 1
            if i == len(devices) - 1:
                print("有{}台设备连接不上".format(cnt))

    # print(s_connect)
    # print(m_connect)
    # print(r_connect)
    result = {"sshcli": s_connect, "manager": m_connect, "resp": r_connect}
    # print(result)
    return result
