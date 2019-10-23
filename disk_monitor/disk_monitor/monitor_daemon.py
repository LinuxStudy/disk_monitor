#!/usr/bin/python3.7
# _*_ coding: utf-8 _*_

import configparser
import os

from disk_util.query_info import QueryInfo
from disk_util.load_info import LoadInfo

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def daemon_opt():
    cg = configparser.ConfigParser()
    cg.read(os.path.join(root_dir, 'config', 'disk_monitor.ini'))
    addr = cg.get('host', 'addr')
    user = cg.get('host', 'user')
    password = cg.get('host', 'password')
    query_dict = {'addr': addr, 'user': user, 'password': password}
    query_opt = QueryInfo(**query_dict)
    query_opt.get_info()
    load_opt = LoadInfo(**query_dict)
    load_opt.read_info()


if __name__ == '__main__':
    daemon_opt()
