#!/usr/bin/python3.7
# _*_ coding: utf-8 _*_

from query_disk import query_info


def conctrol_opt(args):
    args_dict = {
        'addr': args.address,
        'limit': args.limit,
        'user': args.user,
        'password': args.password
    }
    query_opt = query_info(**args_dict)
    query_opt.get_info()
