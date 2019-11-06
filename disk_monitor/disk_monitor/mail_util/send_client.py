#!/usr/bin/python3.7
# _*_ coding: utf-8 _*_
import configparser
import time

from email.header import Header
from email.mime.text import MIMEText
from poplib import POP3
from smtplib import SMTP

from disk_util import util_constant as const
from load_conf import ConfOperate
from log.util_log import CreateLog

log = CreateLog('disk_monitor', 'console.log').get_logger()


class SendClient(object):

    def __init__(self):
        self.conf_file = const.CONF_FILE_PATH

    # 邮件内容组装
    def mail_msg(self, sender, recvers, subject, body):
        recvers = ','.join(recvers)
        msg = MIMEText(body, 'plain', 'utf-8')
        msg['Subject'] = Header(subject, 'utf-8')
        msg['From'] = sender
        msg['To'] = recvers
        return msg

    # 发送邮件
    def mail_send(self):
        cg = ConfOperate().conf_opt(self.conf_file)
        smtp_serv = cg.get('163_email', 'smtp_server')
        sender = cg.get('email', 'admin_mail')
        send_pass = cg.get('email', 'admin_password')
        recvers = [cg.get('email', 'custom_mail')]
        duplicates = [cg.get('email', 'duplicate_mail')]
        recvers.extend(duplicates)

        subject = "Mail function of disk_monitor"
        disk_str = cg.get(const.DISK_SPACE_SECTION, 'used_value')
        body = "Your disk available percent is %s!" % disk_str
        send_msg = self.mail_msg(sender, recvers, subject, body)
        send_opt = SMTP(smtp_serv)
        send_opt.connect(smtp_serv, '25')
        send_opt.login(sender, send_pass)
        log.info("Login %s succeful!" % sender)
        # send_opt.starttls()
        send_status = send_opt.sendmail(sender, recvers,
                                        send_msg.as_string())
        print(type(send_status))
        log.info("Send email to %s succeful!" % recvers)
        send_opt.quit()
