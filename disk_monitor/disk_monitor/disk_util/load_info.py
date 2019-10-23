#!/usr/bin/python3.7
# _*_ coding: utf-8 _*_

import configparser
import json
import os

from configobj import ConfigObj
from disk_util.query_info import QueryInfo

parent_dir = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class LoadInfo(object):

    def __init__(self, **kwargs):
        self.json_file = os.path.join(parent_dir, 'disk_info.json')
        self.query_opt = QueryInfo(**kwargs)
        self.config_file = os.path.join(
            parent_dir, 'config', 'disk_monitor.ini')

    def select_date(self):
        global mount_point, max_value
        try:
            if not os.path.exists(self.config_file):
                raise BaseException(
                    "config file not exist! please put it on target location")
        except Exception as e:
            print("ERROR: %s" % e)
            exit(1)

        cg = configparser.ConfigParser()
        cg.read(self.config_file)
        mount_point = cg.get('disk', 'mount_point')
        max_value = cg.get('disk', 'max_value')
        return mount_point, max_value

    def change_options(self, in_section, in_option, in_value=None, **conf_dict):
        cgj = ConfigObj(self.config_file)

        if not conf_dict:
            cgj[in_section][in_option] = in_value
        else:
            cgj[in_section][in_option] = in_value
            for key, value in conf_dict.items():
                cgj[in_section][key] = value

        cgj.write()

    def read_info(self):
        try:
            if not os.path.exists(self.json_file):
                raise BaseException(
                    'can not find disk information, please try query again!')

        except Exception as e:
            print("ERROR: %s" % e)
            self.query_opt.get_info()
        with open(self.json_file) as f:
            disk_info_result = json.load(f)
        mount_point, max_value = self.select_date()
        for value in disk_info_result.values():
            try:
                current_value = value[mount_point]['Use%']
                current_value = current_value.split('%')[0]

            except KeyError as e:
                print("ERROR: mount point %s is not exist on disk, "
                      "please check out input!" % mount_point)
                print("ERROR: %s" % e)

        self.change_options(
            'disk', 'current_value', current_value)
