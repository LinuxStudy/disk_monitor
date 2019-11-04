#!/usr/bin/python3.7
# _*_ conding: utf-8 _*_

import configparser

from configobj import ConfigObj
from disk_util import util_constant as const


class ConfOperate(object):

    def __init__(self):
        self.conf_file = const.CONF_FILE_PATH

    def conf_opt(self, conf_file=None):
        cg = configparser.ConfigParser()
        if conf_file is None:
            cg.read(self.conf_file)
        else:
            cg.read(conf_file)
        return cg

    def change_options(self, in_section, conf_file=None, **conf_dict):
        if conf_file is None:
            cgj = ConfigObj(self.conf_file)
        else:
            cgj = ConfigObj(conf_file)
        for key, value in conf_dict.items():
            cgj[in_section][key] = value

        cgj.write()

    def get_conf(self, in_section, conf_file=None, *in_options):
        cg = self.conf_opt()
        conf_info = {}
        for key in in_options:
            conf_info[key] = cg.get(in_section, key)

        return conf_info
