#!/usr/bin/python3.7
# _*_ coding: utf-8 _*_
import mysql.connector

from base_util.network_util import NetworkConn
from disk_util import util_constant as const
from load_conf import ConfOperate
from log.util_log import CreateLog

log = CreateLog('disk_monitor', 'console.log').get_logger()


class DbBaseOperate(object):
    def __init__(self):
        pass

    def init_connector(self):
        cg = ConfOperate().conf_opt(const.CONF_FILE_PATH)
        host = cg.get(const.MYSQL_LOGIN_SECTION, 'host')
        user = cg.get(const.MYSQL_LOGIN_SECTION, 'user')
        password = cg.get(const.MYSQL_LOGIN_SECTION, 'password')
        database = cg.get(const.MYSQL_LOGIN_SECTION, 'database')
        if not NetworkConn(host).ping_action():
            con_opt = mysql.connector.connect(
                host=host, user=user,
                password=password, database=database
            )
            return con_opt
        else:
            log.error("Ping %s failure!" % host)

    def db_operate(self, data):
        con_opt = self.init_connector()
        cursor = con_opt.cursor()
        cursor.execute(
            'CREATE TABLE query_info(query_id VARCHAR(10) PRIMARY KEY, '
            'time TIMESTAMP, used INT, email VARCHAR(50))')

        print(cursor.rowcount)
        con_opt.commit()
        cursor.close()


# if __name__ == '__main__':
#     db_opt = DbBaseOperate()
#     db_opt.db_operate()
