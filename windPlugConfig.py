# coding:UTF-8

"""
windPlug配置文件
"""

# 主库路由名字（与setting文件的名字对应）
DB_ROUTE_MASTER = 'master'
# 从库路由名字（与setting文件的名字对应）
DB_ROUTE_SLAVE = ('slave',)
# 从库路由选择策略，0为随机
DB_ROUTE_SELECT_OPTION = 0


# 页面缓存key前缀
PAGE_CACHE_PREFIX = "pageCache"


# 自定义headers
OWN_HEADERS = {
    'windPlugVersion': '1.0.0(bate)',
}
