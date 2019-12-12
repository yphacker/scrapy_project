# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import MySQLdb as mysqldb


class ProxyPipeline(object):
    def process_item(self, item, spider):
        return item


class FilePipeline(object):
    def __init__(self):
        self.f = open('./data/proxy.txt', 'a')

    def __del__(self):
        self.f.close()

    def process_item(self, item, spider):
        self.f.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (item['ip'], item['port'], item['type'],
                                                       item['position'], item['speed'], item['life'],
                                                       item['last_check_time']))
        return item


class MysqlPipeline(object):
    def process_item(self, item, spider):
        DBKWARGS = spider.settings.get('DBKWARGS')
        con = mysqldb.connect(**DBKWARGS)
        cur = con.cursor()
        sql = "insert into proxy(ip, port, type, position, speed, last_check_time) values (%s,%s,%s,%s,%s,%s)"
        value = (item['ip'], int(item['port']), item['type'], item['position'],
                 item['speed'], item['last_check_time'])
        try:
            cur.execute(sql, value)
        except Exception as e:
            print("Insert error:", e)
            con.rollback()
        else:
            con.commit()
        cur.close()
        con.close()
        return item
