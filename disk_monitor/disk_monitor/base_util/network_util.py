#!/usr/bin/python3.7
# _*_ coding: utf-8 _*_
import subprocess

from IPy import IP
from base_util.system_info import system_type as systp


class NetworkConn(object):
    def __init__(self, in_ip):
        self.__in_ip = in_ip

    def ping_action(self, count=4, timeout=2):
        ip_opt = IP(self.__in_ip)
        ip_version = str(ip_opt.version())
        if systp() == 'Windows':
            option_str = "-n %s -w %s" % (count, timeout)
            if ip_version == '4':
                cmd_str = "ping %s %s" % (option_str, self.__in_ip)
                results = subprocess.getstatusoutput(cmd_str)
                return results[0]
            elif ip_version == '6':
                cmd_str = "ping -6 %s %s" % (option_str, self.__in_ip)
                results = subprocess.getstatusoutput(cmd_str)
                return results[0]
            else:
                pass

        elif systp() == 'Linux':
            option_str = "-c %s -W %s" % (count, timeout)
            if ip_version == '4':
                cmd_str = "ping %s %s" % (option_str, self.__in_ip)
                results = subprocess.getstatusoutput(cmd_str)
                return results[0]
            elif ip_version == '6':
                cmd_str = "ping -6 %s %s" % (option_str, self.__in_ip)
                results = subprocess.getstatusoutput(cmd_str)
                return results[0]

        else:
            pass
