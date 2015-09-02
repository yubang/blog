# coding:UTF-8

"""
windPlug配置文件
"""

#主库路由名字（与setting文件的名字对应）
DB_ROUTE_MASTER = 'master'
#从库路由名字（与setting文件的名字对应）
DB_ROUTE_SLAVE = ('salve',)
#丛库路由选择策略，0为随机
DB_ROUTE_SELECT_OPTION = 0