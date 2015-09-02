# coding:UTF-8

"""
django数据库路由
"""


import windPlugConfig
import random


class MasterAndSlaveRoute(object):
    """主从库路由"""
    def db_for_read(self, model, **hints):
        length = len(windPlugConfig.DB_ROUTE_SLAVE)
        index = int(random.uniform(0, length))
        return windPlugConfig.DB_ROUTE_SLAVE[index]

    def db_for_write(self, model, **hints):
        return windPlugConfig.DB_ROUTE_MASTER

    def allow_relation(self, obj1, obj2, **hints):
        return None

    def allow_syncdb(self, db, model):
        return True
