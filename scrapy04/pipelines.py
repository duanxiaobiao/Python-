# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import csv
import time
from datetime import datetime

import pymysql


class Scrapy04Pipeline(object):

    def open_spider(self,spider):

        # 1. 建立数据库的连接
        self.connect = pymysql.connect(
            # localhost连接的是本地数据库
            host='localhost',
            # mysql数据库的端口号
            port=3306,
            # 数据库的用户名
            user='root',
            # 本地数据库密码
            passwd='root',
            # 表名
            db='liepin_information',
            # 编码格式
            charset='utf8'
        )
        # 2. 创建一个游标cursor, 是用来操作表。
        self.cursor = self.connect.cursor()
        print('数据库连接成功！')
        print('爬虫开始....正在写入数据库...')
        self.start_time =datetime.now()



    def process_item(self, item, spider):
        # 3. 将Item数据放入数据库，默认是同步写入。
        insert_sql = 'insert into informations01(name ,company, salary ,address,experience ,education,welfare)VALUES (%s,%s,%s,%s,%s,%s,%s)'
        insert_sql2 =(item['name'], item['company'],item['salary'] ,item['address'] ,item['experience'],item['education'],item['welfare'])
        self.cursor.execute(insert_sql,insert_sql2)
        # 4. 提交操作
        self.connect.commit()

    def close_spider(self, spider):
        # 关闭数据库
        self.cursor.close()
        print('爬虫结束.数据库关闭.')
        self.close_time = datetime.now()
        print('运行时间为:', self.close_time - self.start_time)
