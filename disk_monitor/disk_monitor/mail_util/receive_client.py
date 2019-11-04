#!/usr/bin/python3.7
# _*_ coding: utf-8 _*_
import configparser
import signal
import time

from email.header import Header
from email.mime.text import MIMEText
from log.util_log import CreateLog
from load_conf import ConfOperate
from poplib import POP3
from smtplib import SMTP

from disk_util import util_constant as const

log = CreateLog('disk_monitor', 'console.log').get_logger()


class ReceiveClient(object):

    def __init__(self):
        self.conf_file = const.CONF_FILE_PATH
        self.__email_info = None
    # def sigint_handler(self, signum, frame):
    #     global is_sigint_up
    #     is_sigint_up = True
    #     log.info("catched interrupt signal!")

    # 接受用户邮箱密码
    def mail_prepare(self):
        login_info = {}
        account_list = []
        # signal.signal(signal.SIGINT, self.sigint_handler)
        # # signal.signal(signal.SIGHUP, self.sigint_handler)
        # signal.signal(signal.SIGTERM, self.sigint_handler)
        # is_sigint_up = False
        cg = ConfOperate().conf_opt(self.conf_file)
        support_agent = cg.get('email', 'support_agent')

        while True:
            try:
                print("We can sopport email agent is %s" % support_agent)
                mail_type = input(
                    "Please input your email agent type,(example qq or 163): ")
                mail_type = mail_type + '_email'
                user = input("Please input your email account: ")
                password = input("Give the password of account: ")
                login_info[mail_type] = account_list.append({user: password})
                end_flag = input("You can input quit or q to cancel input: ")
                if end_flag == 'quit' or end_flag == 'q':
                    break
                else:
                    log.warning("Input illegal, canceled failure")
                    continue
                # if is_sigint_up:
                # log.warning("Input programe stop, You have canceled input!")
                #     break
            except Exception as e:
                log.warning("{}".format(e))
                log.warning("appear some error! please input again!")
                continue
        return login_info

    # 判断接受邮件的邮箱类型
    def mail_type(self):
        cg = ConfOperate().conf_opt(self.conf_file)
        login_info = self.mail_prepare()
        input_type = set(login_info.keys())
        allow_type = set([section for section in cg.sections()
                          if section.endswith('_email')])
        if not input_type.issubset(allow_type):
            print("Sorry, unsupport this email client to receive email!")
            unsupport_type = input_type.difference(allow_type)
            for item in unsupport_type:
                print(
                    """
                We can not support this account, because email agent type: \n
                    %s
                    """ % login_info[item]
                )
            return False
        else:
            self.__email_info = login_info
            return True

    # 处理重试场景
    def retry_action(self):
        cg = ConfOperate().conf_opt(self.conf_file)
        retry_count = cg.get('base', 'retry_count')
        retry_status = True
        count = 0
        while True:
            count += 1
            if self.mail_type():
                break
            if count > retry_count - 1:
                retry_status = False
                break
        return retry_status

    def mail_review(self, conf_section):
        pass

    def mail_receive(self):
        if self.mail_type():
            for section in self.__email_info.keys():
                self.mail_review(section)

        else:
            try:
                if not self.retry_action():
                    raise BaseException(
                        "Sorry! the input contain unsupported email agent.\n"
                        "Please checkout and do it again")
            except Exception as e:
                log.error(e)

        # pop3_serv = cg.get('email', 'pop3_server')
        # recv_opt = POP3(pop3_serv)
        # # for pepole in recvers:
        # #
        # #     recv_opt.user(sender)
        #     # recv_opt.pass_(send_pass)
        #     # rsp, msg, siz = recv_opt.retr(recv_opt.stat()[0])
        #     # print(rsp)


if __name__ == '__main__':
    mail_agent = ReceiveClient()
    mail_agent.mail_receive()
