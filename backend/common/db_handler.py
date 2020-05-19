from threading import Lock

from DBUtils.PooledDB import PooledDB
import pymysql


class MysqlPool:

    def __init__(self, db):
        self.config = {
            'creator': pymysql,
            'host': db['db_host'],
            'port': db['db_port'],
            'user': db['db_user'],
            'password': db['db_password'],
            'database': db['db_name'],
            'charset': db['charset'],
            'maxconnections': 70,  # 连接池最大连接数量
            'cursorclass': pymysql.cursors.DictCursor
        }

        self.pool = PooledDB(**self.config)

    def __enter__(self):
        self.conn = self.pool.connection()
        self.cursor = self.conn.cursor()
        return self

    def __exit__(self, type, value, trace):
        self.cursor.close()
        self.conn.close()

