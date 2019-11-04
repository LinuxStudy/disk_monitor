#!/usr/bin/python3.7
# _*_coding: utf-8 _*_

import logging
import os

from load_conf import ConfOperate
from disk_util import util_constant as const


class CreateLog(object):
    def __init__(self, theme, name):
        self.theme = theme
        self.name = name

    def set_level(self, log_type, log_level):
        pass

    def get_logger(self):
        cg = ConfOperate().conf_opt(const.CONF_FILE_PATH)
        log_file = cg.get(const.LOG_FILE_SECTION, const.LOG_DIR_OPTION)
        log_path = os.path.join(log_file, self.name)
        log_format = logging.Formatter(
            '%(asctime)s %(name)s %(pathname)s '
            '%(levelname)s [pid:%(process)d] '
            '[%(threadName)s] '
            '[%(filename)s:%(lineno)d '
            'function %(funcName)s] %(message)s')
        logger_obj = logging.getLogger()
        logger_obj.setLevel(logging.DEBUG)
        fhd = logging.FileHandler(log_path)
        fhd.setLevel(logging.DEBUG)

        shd = logging.StreamHandler()
        shd.setLevel(logging.WARNING)

        fhd.setFormatter(log_format)
        shd.setFormatter(log_format)

        logger_obj.addHandler(fhd)
        logger_obj.addHandler(shd)

        return logger_obj
