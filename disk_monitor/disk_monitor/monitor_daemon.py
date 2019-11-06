#!/usr/bin/python3.7
# _*_ coding: utf-8 _*_

import os
import time

from datetime import datetime

from disk_util.query_info import QueryInfo
from disk_util.load_info import LoadInfo
from disk_util import util_constant as const
from load_conf import ConfOperate
from mail_util.send_client import SendClient
from sql_conn.db_prepare import DbBaseOperate


class DaemonProcess(object):
    def __init__(self):
        self.__conf_file = const.CONF_FILE_PATH

    def monitor_action(self, login_info):
        cg = ConfOperate().conf_opt(self.__conf_file)
        current_time = datetime.now()
        current_stamp = current_time.timestamp()

        query_opt = QueryInfo(**login_info)
        query_opt.get_info()
        load_opt = LoadInfo(**login_info)
        load_opt.read_info()
        used_percent = cg.get(const.DISK_SPACE_SECTION, const.DISK_USED_OPTION)

        db_info = {'time': current_stamp, 'used': used_percent}
        return db_info

    def daemon_opt(self):
        cg = ConfOperate().conf_opt(self.__conf_file)
        email_value = cg.get(const.DISK_SPACE_SECTION, 'warn_value')
        email_string = cg.get(
            const.EMIAL_INFO_SECTION, const.EMIAL_CUSTOM_OPTION) + "+" + \
                cg.get(const.EMIAL_INFO_SECTION, const.EMIAL_DUPLICATE_OPTION)
        db_static_data = {'email': email_string}
        query_count = 0
        options_list = ['addr', 'user', 'password']
        conf_dict = ConfOperate().get_conf(
            'host', self.__conf_file, *options_list)
        while True:
            time.sleep(60)
            db_info = self.monitor_action(conf_dict)
            query_count += 1
            db_static_data['query_id'] = int(query_count)
            db_info.update(db_static_data)
            print(db_info)
            if db_info['used'] > email_value:
                SendClient().mail_send()
            # DbBaseOperate().db_operate(db_info)
            db_info.clear()


if __name__ == '__main__':
    daemon_opt = DaemonProcess()
    daemon_opt.daemon_opt()
