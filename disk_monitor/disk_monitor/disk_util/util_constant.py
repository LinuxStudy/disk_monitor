#!/usr/bin/python3.7
# _*_ coding: utf-8 _*_

import os

ROOT_PATH = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
JSON_FILE_PATH = os.path.join(ROOT_PATH, 'disk_info.json')
CONF_FILE_PATH = os.path.join(ROOT_PATH, 'config', 'disk_monitor.ini')

DISK_SPACE_SECTION = 'disk'
DISK_USED_OPTION = 'used_value'
LOG_FILE_SECTION = 'log'
LOG_DIR_OPTION = 'log_dir'

EMIAL_INFO_SECTION = 'email'
EMIAL_CUSTOM_OPTION = 'custom_mail'
EMIAL_DUPLICATE_OPTION = 'duplicate_mail'

MYSQL_LOGIN_SECTION = 'mysql'
