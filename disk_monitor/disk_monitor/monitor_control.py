#!/usr/bin/python3.7
# _*_ coding: utf-8 _*_

from disk_util.query_info import QueryInfo


def conctrol_opt(args):
    args_dict = {
        'addr': args.address,
        'limit': args.limit,
        'user': args.user,
        'password': args.password
    }
    query_opt = QueryInfo(**args_dict)
    query_opt.get_info()
