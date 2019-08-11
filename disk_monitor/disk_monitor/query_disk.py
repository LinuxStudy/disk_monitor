#!/usr/bin/python3.7
# _*_ coding: utf-8 _*_

import os
import paramiko

from datetime import datetime
from IPy import IP

PARENT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class query_info(object):

    def __init__(self, **args):
        self.ip = args.get('addr')
        self.user = args.get('user')
        self.password = args.get('password')

    def judge_ip(self):
        ip_version = IP(self.ip).version()
        return ip_version

    def register_info(self, disk_str):
        disk_info_file = os.path.join(PARENT_DIR, 'disk_info')
        if os.path.exists(disk_info_file):
            with open(disk_info_file, 'a') as f:
                f.write("-------------- start register info ----------------\n")
                register_date = datetime.now()
                f.write(register_date.strftime("%Y-%m-%d %H:%M:%S"))
                f.write("\n")
                f.write(disk_str)
                f.write("-------------- end register info ---------------- \n")
        else:
            with open(disk_info_file, 'w') as f:
                f.write("-------------- start register info ----------------\n")
                register_date = datetime.now()
                f.write(register_date.strftime("%Y-%m-%d %H:%M:%S"))
                f.write("\n")
                f.write(disk_str)
                f.write("-------------- end register info ---------------- \n")

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
            ssh.connect(hostname=self.ip, username=self.user,
                        password=self.password)

            print("login %s successful" % self.ip)
            return ssh
        else:
            print("ip type is ipv6")

    def get_info(self):
            ssh_opt = self.login_node()
            print("start to exec cmd......")
            cmd_content = self.host_cmd(ssh_opt, 'df -h').read().decode('utf-8')
            ssh_opt.close()
            self.register_info(cmd_content)
