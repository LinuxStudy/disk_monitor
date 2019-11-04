#!/usr/bin/python3.7
# _*_ coding: utf-8 _*_

import json
import os

from load_conf import ConfOperate
from disk_util.query_info import QueryInfo
from disk_util import util_constant as const
from  log.util_log import CreateLog

log = CreateLog('disk_monitor', 'console.log').get_logger()


class LoadInfo(object):

    def __init__(self, **kwargs):
        self.json_file = const.JSON_FILE_PATH
        self.query_opt = QueryInfo(**kwargs)
        self.config_file = const.CONF_FILE_PATH

    def select_date(self):
        global mount_point, max_value
        try:
            if not os.path.exists(self.config_file):
                raise BaseException(
                    "config file not exist! please put it on target location")
        except Exception as e:
            log.error("{}".format(e))
            print("ERROR: %s" % e)

            exit(1)
        cg = ConfOperate().conf_opt(self.config_file)
        mount_point = cg.get(const.DISK_SPACE_SECTION, 'mount_point')
        max_value = cg.get(const.DISK_SPACE_SECTION, 'max_value')
        return mount_point, max_value

    def read_info(self):
        change_options = {}
        try:
            if not os.path.exists(self.json_file):
                raise BaseException(
                    'can not find disk information, please try query again!')

        except Exception as e:
            log.error("{}".format(e))
            print("ERROR: %s" % e)
            self.query_opt.get_info()
        with open(self.json_file) as f:
            disk_info_result = json.load(f)
        mount_point, max_value = self.select_date()
        for value in disk_info_result.values():
            try:
                current_value = value[mount_point]['Use%'].split('%')[0]
            except KeyError as e:
                log.error("ERROR: mount point %s is not exist on disk, "
                      "please check out input!" % mount_point)
                print("ERROR: mount point %s is not exist on disk, "
                      "please check out input!" % mount_point)
                log.error("{}".format(e))
                print("ERROR: %s" % e)
        change_options.update({const.DISK_USED_OPTION: current_value})
        ConfOperate().change_options(
            const.DISK_SPACE_SECTION, self.config_file, **change_options)
