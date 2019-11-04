#!/usr/local/python3.7
# _*_ coding: utf-8 _*_
import platform


def system_type():
    sys_type = ''
    if platform.system() == 'Windows':
        sys_type = 'Windows'
        return sys_type
    elif platform.system() == 'Linux':
        sys_type = 'Linux'
        return sys_type
    else:
        return sys_type
