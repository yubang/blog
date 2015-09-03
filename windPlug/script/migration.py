# coding:UTF-8


"""
数据库迁移升级工具
@author: yubang
"""


from django.db import models
from django.db import connection, transaction
from django.core.exceptions import ObjectDoesNotExist
import os
import time
import datetime


class WindPlugMigrationModel(models.Model):
    version = models.CharField(max_length=100, unique=True, null=False)
    migrationTime = models.DateTimeField(null=False)

    def get_create_table_sql(self):
        return """
            create table if not exists windPlug_migration(
                id int(11) auto_increment,
                version varchar(100) not null,
                migrationTime datetime not null,
                primary key(id),
                unique(version)
            );
        """

    class Meta:
        db_table = "windPlug_migration"


def create_sql(sql_dir_path="windPlug/data/sql"):
    """
    创建新的sql语句
    :param sql_dir_path: SQL语句文件存放目录
    :return: str
    """
    if not os.path.exists(sql_dir_path):
        os.makedirs(sql_dir_path)
    fp_name = "sql_" + str(int(time.time())) + ".txt"
    fp_path = os.path.join(sql_dir_path, fp_name)
    open(fp_path, 'w').close()
    return fp_path


def migration_db(sql_dir_path="windPlug/data/sql"):
    """
    同步数据库
    :param sql_dir_path: SQL语句文件存放目录
    :return: int 执行的sql数目
    """

    count = 0

    try:
        dao = WindPlugMigrationModel()
        sql = dao.get_create_table_sql()
        cursor = connection.cursor()
        cursor.execute(sql)
        transaction.commit()
        cursor.close()
    except:
        pass

    fps = os.listdir(sql_dir_path)
    for fp in fps:

        try:
            WindPlugMigrationModel.objects.get(version=fp)
            continue
        except ObjectDoesNotExist:
            pass

        fp_path = os.path.join(sql_dir_path, fp)
        sql = open(fp_path, 'r').read()
        cursor = connection.cursor()
        cursor.execute(sql)
        transaction.commit()
        cursor.close()

        #记录执行
        dao = WindPlugMigrationModel(version=fp, migrationTime=datetime.datetime.now())
        dao.save()

        count += 1

    return count
