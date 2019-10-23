#!/usr/bin/python3.7
# _*_ coding: utf-8 _*_

import json
import os
import re
import paramiko

from datetime import datetime
from IPy import IP

PARENT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class QueryInfo(object):

    def __init__(self, **args):
        self.__ip = args.get('addr')
        self.__user = args.get('user')
        self.__password = args.get('password')

    def judge_ip(self):
        ip_version = IP(self.__ip).version()
        return ip_version

    def register_info(self, disk_str, write_mode='w'):
        disk_info_file = os.path.join(
            os.path.dirname(PARENT_DIR), 'disk_info.json')
        with open(disk_info_file, write_mode) as f:
            register_date = datetime.now()
            query_time = register_date.strftime("%Y-%m-%d %H:%M:%S")
            mount_point_data = {}
            for line in disk_str.split('\n')[1:-1]:
                mount_point_name = re.split(r'\s+', line)[-1]
                mount_point_detail = {}
                max_volume = len(re.split(r'\s+', line)[:-1])
                for index, info_key in enumerate(
                        re.split(r'\s+', disk_str.split('\n')[0])[:max_volume]):
                    mount_point_detail[info_key] = re.split(r'\s+', line)[index]
                mount_point_data[mount_point_name] = mount_point_detail
            disk_info_dict = {query_time: mount_point_data}

            json.dump(disk_info_dict, f)

    def host_cmd(self, ssh_oop, cmd_str):
        stdin, stdout, stderr = ssh_oop.exec_command(cmd_str)
        return stdout

    def login_node(self):
        print("ip version type is %s" % type(self.judge_ip()))
        if self.judge_ip() == 4:
            paramiko.util.log_to_file('syslogin.log')
            ssh = paramiko.SSHClient()
            ssh.load_system_host_keys()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=self.__ip, username=self.__user,
                        password=self.__password)

            print("login %s successful" % self.__ip)
            return ssh
        else:
            print("ip type is ipv6")

    def get_info(self):
            ssh_opt = self.login_node()
            print("start to exec cmd......")
            cmd_content = self.host_cmd(ssh_opt, 'df -h').read().decode('utf-8')
            ssh_opt.close()
            self.register_info(cmd_content)
