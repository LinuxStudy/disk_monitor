#!/usr/bin/python3.7
# _*_ coding: utf-8 _*_
import argparse

from monitor_control import conctrol_opt


def main():

    parser = argparse.ArgumentParser(description="a tool to monitor disk space")
    parser.add_argument("-i", "--ip_address", help="give a server ip address",
                        dest='address', required=True)
    parser.add_argument("-l", "--limit",
                        help="the max percent value of used disk", dest='limit',
                        type=int)
    parser.add_argument("-u", "--user", help="give user name of host",
                        dest='user', required=True)
    parser.add_argument("-p", "--password", help="give user password of host",
                        dest='password', required=True)
    parser.set_defaults(func=conctrol_opt)
    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
