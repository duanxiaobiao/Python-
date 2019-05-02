import re
import time
from collections import Counter

import pandas

import MySQLdb
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
#-*- coding:utf-8 -*-
from pyecharts import Geo
from sqlalchemy import create_engine

print('======================读取数据库============================')
mysql_cn= MySQLdb.connect(host='localhost',
                          port=3306,
                          user='root',
                          passwd='root',
                          db='liepin_information',
                          charset='utf8'
                          )
df = pd.read_sql("select * from informations01", con=mysql_cn)

print('原始数据一共%s条'%len(df)+'.....')    #数据记录的长度
print('接下来进行数据的清洗.')
#数据清洗：
#1. 首先去除重复值
liepin_data = df.drop_duplicates(inplace = False)
print('=='*30)
print('去除重复值之后的数据记录为:%s 条'%len(liepin_data))
#3.缺失值处理
liepin_data.isnull().sum()

#4.数据清洗

#-------------------对 salary属性列进行数据清洗 -----------------------------------
#对工资salary进行分析,插入三列，min_salary,max_salary,avg_salary
liepin_data.insert(4,column ='min_salary',value=np.nan)  #增加的最低工资
liepin_data.insert(5,column ='max_salary',value=np.nan)  #增加的最高工资
liepin_data.insert(6,column ='avg_salary',value=np.nan)  #增加的平均工资
#拿到工资属性列的所有值
salary_data =liepin_data['salary']
#声明三个list列表
min_salary =[]
max_salary =[]
avg_salary =[]
for i in salary_data:
    if i.strip() =='面议':
        min_salary.append('面议')
        avg_salary.append('面议')
        max_salary. append('面议')
    else:
        pattern =r'(\d+)-(\d+).*'
        regex =re.compile(pattern)
        m =regex.match(i)
        min_salary.append(m.group(1))
        max_salary.append(m.group(2))
        int_min =int(m.group(1))
        int_max =int(m.group(2))
        avg_salary.append(format((int_min+int_max)/2,'.2f'))
liepin_data.loc[:,'min_salary'] =min_salary
liepin_data.loc[:,'max_salary'] =max_salary
liepin_data.loc[:,'avg_salary'] =avg_salary

#--------------------------salary属性列数据清洗结束----------------------------


#---------------------------对address属性列进行标准化---------------------------

address =[]
for a in liepin_data['address']:
    if '-' in a:
        a = a[0:a.index('-')]
    address.append(a)
liepin_data['address'] =address

#对多地址address进行标准化
#首先声明一个list盛放多地址的记录。
new_DataFrame =[]
for index,cols in liepin_data.iterrows():
    if ',' in cols['address']:
        for i in cols['address'].split(','):
            new =pd.DataFrame({'name':[cols['name']],
                               'company':[cols['company']],
                               'salary':[cols['salary']],
                               'min_salary':[cols['min_salary']],
                               'max_salary':[cols['max_salary']],
                               'avg_salary':[cols['avg_salary']],
                               'address':[i],
                               'experience':[cols['experience']],
                               'education':[cols['education']],
                               'welfare':[cols['welfare']]
                               })
            liepin_data =liepin_data.append(new,sort=False)
    else:
        pass
#再次进行去除重复值
liepin_data = liepin_data.drop_duplicates(inplace = False)

#删除多地址记录
for index,cols in liepin_data.iterrows():
    if ',' in cols['address']:
        liepin_data =liepin_data.drop(index=index)

print('去除重复值、去除多地址后的数据记录数为:', len(liepin_data))
#---------------------------address属性列标准化结束---------------------------
print('数据清洗后保存到CSV文件.')
liepin_data.to_csv("liepin_new_data.csv", index_label="index_label",index=True)
print("数据保存成功...")
print('数据清洗工作结束.')






















