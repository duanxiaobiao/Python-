#SELECT DISTINCT education FROM informations03;
import cv2
import jieba
from sqlalchemy import create_engine
from collections import Counter

import pandas

import MySQLdb
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
#-*- coding:utf-8 -*-
from pyecharts import Geo
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

#---------------------因数据录入完毕，因此此段代码隐去。--------------------------------------------------
"""
#读取liepin_analysis.py文件生成的CSV文件,将其保存到数据库.
print('读入CSV文件数据,并把不合法的数据删除.')
liepin_new_data=pd.read_csv('liepin_new_data.csv',header=None,sep=None,engine='python',names=['index','name','company','salary','address','min_salary','max_salary','avg_salary','experience','education','welfare'])

#-------------------对属性（experience、education列）不匹配的数据进行筛选---------------------------------
    #对experience字段中不合理的记录进行删除
for index,cols in liepin_new_data.iterrows():
    if (('及' in cols['experience'])|(cols['experience']=='统招本科')|(cols['experience']=='学历不限')|(cols['experience']=='博士')):
        liepin_new_data = liepin_new_data.drop(index=index)
    #对education字段中不合理的记录进行删除
for index,cols in liepin_new_data.iterrows():
    if (('北京' in cols['education']) | ('洛杉矶' in cols['education']) | ('日本' in cols['education'])):
        liepin_new_data = liepin_new_data.drop(index=index)
liepin_new_data =liepin_new_data
print('数据整理结束,导入数据库表.')
#------------------------筛选结束---------------------------------------------------
try:
    ##将数据写入mysql的数据库，但需要先通过sqlalchemy.create_engine建立连接,且字符编码设置为utf8，否则有些latin字符不能处理
    conn = create_engine('mysql+pymysql://root:root@localhost:3306/liepin_information',encoding='utf-8')
    #写入数据，table_name为表名，‘replace’表示如果同名表存在就替换掉
    pd.io.sql.to_sql(liepin_new_data, "informations01", conn, if_exists='replace',index=False,index_label =False)
    print('新数据导入成功!')
except:
    print('新数据导入失败!')

print('至此，数据清洗结束.接下来进行数据分析.')
"""

print('======================读取数据库文件============================')
mysql_cn= MySQLdb.connect(host='localhost',
                          port=3306,
                          user='root',
                          passwd='root',
                          db='liepin_information',
                          charset='utf8'
                          )
df = pd.read_sql("select * from informations01", con=mysql_cn)
#
print('数据一共%s条'%len(df)+'.....')    #数据记录的长度

#筛选开始

#数据清洗：
#1. 首先去除重复值
zhaopin = df.drop_duplicates(inplace = False)
print('=='*30)
print('去除重复值之后的数据记录为%s条'%len(zhaopin))
# print(zhaopin)
#2.过滤无效数据
#3.缺失值处理
zhaopin.isnull().sum()



#4.数据加工
#
names =zhaopin.name    #选取属性name列
#含有java字符的name记录
java_names =names.str.contains('java|Java|JAVA')
#python
python_names =names.str.contains('Python|python|PYTHON')
#php
php_names =names.str.contains('PHP|php')
#UI设计
ui_names =names.str.contains('ui|UI')
#Android
Android_names =names.str.contains('android|安卓|Android')
#算法工程师
Algorithm_names =names.str.contains('算法')
#hadoop
hadoop_names =names.str.contains('hadoop|Hadoop')
#数据分析
DA_names =names.str.contains('数据分析')
#人工智能
AI_names =names.str.contains('AI|ai|人工智能')
#区块链
blockchain_names =names.str.contains('区块链')
print('java岗位数：',len(names[java_names]))
print('python岗位数：',len(names[python_names]))
print('PHP岗位数：',len(names[php_names]))
print('UI设计岗位数：',len(names[ui_names]))
print('Android岗位数：',len(names[Android_names]))
print('算法岗位数：',len(names[Android_names]))
print('hadoop岗位数:',len(names[hadoop_names]))
print('数据分析岗位数:',len(names[DA_names]))
print('人工智能岗位数:',len(names[AI_names]))
print('区块链岗位数：',len(names[blockchain_names]))
print('--'*20+'探索计算机软件就业岗位的状况'+'-'*20)
print('.....')
print('条形图绘图如下...')
#x坐标列表
xlabel_list =['java','python','php','UI设计','Android','算法','hadoop','数据分析','人工智能','区块链']
#y坐标列表
ylabel_list =[len(names[java_names]),len(names[python_names]),len(names[php_names]),len(names[ui_names]),len(names[Android_names]),len(names[Algorithm_names]),len(names[hadoop_names]),len(names[DA_names]),len(names[AI_names]),len(names[blockchain_names])]
#循环添加柱顶数值
for a, b in zip(xlabel_list,ylabel_list):
    plt.text(a, b + 0.05, '%.0f' % b, ha='center', va='bottom', fontsize=7)
#x轴标签
plt.xlabel('职位')
#y轴标签
plt.ylabel('职位数量')
#y轴刻度限制范围
plt.ylim(0, 5000,1000)
#bar()函数绘制条形图
plt.bar(xlabel_list,ylabel_list, width=0.5, alpha=0.8, color='red',edgecolor = 'black')
#条形图的标题
plt.title("计算机软件就业岗位条形图")
plt.savefig('images/计算机软件就业岗位条形图.jpg')
#显示
plt.show()
print('计算机软件就业岗位条形图绘制完成.')

print('饼图绘制中...')
"""
    #柱形图的绘制
    plt.bar(left, height, width, color, align, yerr)函数：绘制柱形图。
    eft为x轴的位置序列，一般采用arange函数产生一个序列；
    height为y轴的数值序列，也就是柱形图的高度，一般就是我们需要展示的数据；
    width为柱形图的宽度，一般这是为1即可.一般默认，除非在交错图中会用到；
    color为柱形图填充的颜色;
    align设置plt.xticks()函数中的标签的位置,一般是center；
    yerr让柱形图的顶端空出一部分。

"""
#绘制饼图
print('-'*20+'探索计算机软件就业岗位的比例分配。'+'-'*20)
xlabel_list =['java','python','php','UI设计','Android','算法','hadoop','数据分析','人工智能','区块链']
#y坐标列表
ylabel_list =[len(names[java_names]),len(names[python_names]),len(names[php_names]),len(names[ui_names]),len(names[Android_names]),len(names[Algorithm_names]),len(names[hadoop_names]),len(names[DA_names]),len(names[AI_names]),len(names[blockchain_names])]
#颜色
color =['red','#7FFF00','yellow','green','cyan','blue','purple','orange','gray','pink']
# 各部分突出值
explode = [0,0.1, 0, 0,0,0,0,0,0,0]
#绘制饼图
patches, l_text, p_text = plt.pie(ylabel_list, explode=explode, colors=color, labels=xlabel_list, labeldistance=1.1, autopct="%1.1f%%", shadow=False, startangle=90, pctdistance=0.6)
plt.axis("equal")    # 设置横轴和纵轴大小相等，这样饼才是圆的

plt.legend(loc=0,ncol=1)
plt.title("计算机软件就业岗位比例饼状图")
plt.savefig('images/计算机软件就业岗位比例饼状图.jpg')
plt.show()
print('计算机软件就业岗位比例饼状图绘制完成.')


#---------------------------------------------------------------
print('-'*20+'探索计算机软件就业和教育的关系'+'-'*20)
#学历不限
xuelibuxian_job_num =zhaopin.education.str.contains('学历不限').sum()
#大专
dazhuan_job_num =zhaopin.education.str.contains('大专及以上').sum()
#本科
benke_job_num =zhaopin.education.str.contains('本科及以上').sum()
#硕士
shuoshi_job_num =zhaopin.education.str.contains('硕士及以上').sum()
#博士
boshi_job_num =zhaopin.education.str.contains('博士').sum()
#画图
plt.figure(1)
plt.subplot(1,2,1)
#x坐标列表
xlabel_list =['学历不限','大专','本科','硕士','博士']
#y坐标列表
ylabel_list =[xuelibuxian_job_num,dazhuan_job_num,benke_job_num,shuoshi_job_num,boshi_job_num]
for a, b in zip(xlabel_list,ylabel_list):
    plt.text(a, b + 0.05, '%.0f' % b, ha='center', va='bottom', fontsize=7)
#x轴标签
plt.xlabel('学历')
#y轴标签
plt.ylabel('职位数量')
#y轴刻度限制范围
plt.ylim(0, 21000,2000)
#bar()函数绘制条形图
plt.bar(xlabel_list,ylabel_list, width=0.5, alpha=0.8, color='blue',edgecolor = 'black')
#条形图的标题
plt.title("计算机软件就业岗位与学历关系条形图")
print('计算机软件就业岗位与学历关系条形图绘制完成.')

#------------------------------------------------------------------------------------
print('-'*20+'探索计算机软件就业岗位与学历的关系'+'-'*20)
print('绘制Python就业岗位与学历关系条形图')
Python_xuelibuxian_job_num =zhaopin[zhaopin.name.str.contains('Python|python|PYTHON')&zhaopin.education.str.contains('学历不限')].shape[0]
# print(Python_xuelibuxian_job_num[['name','education']])
Python_dazhuan_job_num =zhaopin[zhaopin.name.str.contains('Python|python|PYTHON')&zhaopin.education.str.contains('大专|大专及以上|中专/中技及以上')].shape[0]
Python_benke_job_num =zhaopin[zhaopin.name.str.contains('Python|python|PYTHON')&zhaopin.education.str.contains('统招本科|本科及以上|本科')].shape[0]
Python_shuoshi_job_num =zhaopin[zhaopin.name.str.contains('Python|python|PYTHON')&zhaopin.education.str.contains('硕士及以上|MBA')].shape[0]
Python_boshi_job_num =zhaopin[zhaopin.name.str.contains('Python|python|PYTHON')&zhaopin.education.str.contains('博士')].shape[0]
xlabel_list =['学历不限','大专','本科','硕士','硕士']
ylabel_list =[Python_xuelibuxian_job_num,Python_dazhuan_job_num,Python_benke_job_num,Python_shuoshi_job_num,Python_boshi_job_num]
plt.subplot(1,2,2)
plt.xlabel('学历')
#y轴标签
plt.ylabel('Python职位数量')
#y轴刻度限制范围
plt.ylim(0, 21000,2000)
#bar()函数绘制条形图
plt.bar(xlabel_list,ylabel_list, width=0.5, alpha=0.8, color='green',edgecolor = 'black')
#条形图的标题
plt.title("Python就业岗位与学历关系条形图")
plt.savefig('images/Python就业岗位与学历关系条形图.jpg')
#显示
plt.show()
print('Python就业岗位与学历关系条形图绘制结束.')


#--------------------------------------------------------------------------------------
print('-'*20+'探索计算机工作经验和月工资的关系'+'-'*20)
zhaopin_new_data =zhaopin.loc[1:,['name','max_salary','avg_salary','experience']]
zhaopin_new_data =zhaopin_new_data[zhaopin_new_data['avg_salary']!='面议']
print("此时去掉带有面议字段之后的数据长度为：",len(zhaopin_new_data))
zhaopin_new_data =zhaopin_new_data.replace(["1年以上","2年以上","3年以上","4年以上","5年以上","6年以上","7年以上","8年以上","9年以上","10年以上","12年以上","15年以上"],[1,2,3,4,5,6,7,8,9,10,12,15])
#强制转换数据类型
zhaopin_new_data['experience'] =zhaopin_new_data['experience'].astype(int)
zhaopin_new_data['avg_salary'] =zhaopin_new_data['avg_salary'].astype(float)
#返回不同职业的月工资列表
def salary_list(string,df):
    name_avg_salary_list =[]
    for i in range(1,11):
        #如果查询结果为空DataFrame
        if (df[(df['experience'] ==i)&(df['name'].str.contains(string))].empty):
            java_avg_salary =0.0
            name_avg_salary_list.append(java_avg_salary)
        else:
            java_avg_salary = round((df[(df['name'].str.contains(string)) & (df['experience'] == i)]['avg_salary'].mean()) / 12,2)  # 保留两位小数
            name_avg_salary_list.append(java_avg_salary)
    return name_avg_salary_list
#java工作的、学历从1-10年的一个 月工资列表。
java_avg_salary =salary_list("java|Java|JAVA",zhaopin_new_data)
#Python
Python_avg_salary =salary_list("Python|python|PYTHON",zhaopin_new_data)
#PHP
PHP_avg_salary =salary_list("PHP|php",zhaopin_new_data)
#UI
ui_avg_salary =salary_list("ui|UI",zhaopin_new_data)
#Android
Android_avg_salary =salary_list("android|安卓|Android",zhaopin_new_data)
#算法
Algorithm_avg_salary =salary_list("算法",zhaopin_new_data)
#hadoop
hadoop_avg_salary =salary_list("hadoop|Hadoop",zhaopin_new_data)
#数据分析
DA_avg_salary =salary_list("数据分析",zhaopin_new_data)
#人工智能
AI_avg_salary =salary_list("AI|ai|人工智能",zhaopin_new_data)
x_range =[1,2,3,4,5,6,7,8,9,10]
print(java_avg_salary)
plt.bar([x-0.6 for x in x_range],java_avg_salary, width=0.07, alpha=0.8, color='red',edgecolor = 'black',label='Java')
plt.bar([x-0.53 for x in x_range],Python_avg_salary, width=0.07, alpha=0.8, color='purple',edgecolor = 'black',label ='Python')
plt.bar([x-0.46 for x in x_range],PHP_avg_salary, width=0.07, alpha=0.8, color='yellow',edgecolor = 'black',label ='PHP')
plt.bar([x-0.39 for x in x_range],ui_avg_salary, width=0.07, alpha=0.8, color='green',edgecolor = 'black',label ='UI')
plt.bar([x-0.32 for x in x_range],Android_avg_salary, width=0.07, alpha=0.8, color='blue',edgecolor = 'black',label ='Android')
plt.bar([x-0.25 for x in x_range],Algorithm_avg_salary, width=0.07, alpha=0.8, color='orange',edgecolor = 'black',label ='算法')
plt.bar([x-0.18 for x in x_range],hadoop_avg_salary, width=0.07, alpha=0.8, color='gray',edgecolor = 'black',label ='Handoop')
plt.bar([x-0.11 for x in x_range],DA_avg_salary, width=0.07, alpha=0.8, color='pink',edgecolor = 'black',label='数据分析')
plt.bar([x-0.04 for x in x_range],AI_avg_salary, width=0.07, alpha=0.8, color='black',edgecolor = 'black',label ='人工智能')
plt.xlabel('经验/年')
#y轴标签
plt.ylabel('月平均工资/万')
#x轴刻度限制范围
plt.xlim(0,11,1)
#y轴刻度限制范围
plt.ylim(0, 14,2)

#循环添加柱顶数值
for a, b in zip([x-0.6 for x in x_range],java_avg_salary):
    plt.text(a, b + 0.1, '%.2f' % b, ha='center', va='bottom', fontsize=6)
for a, b in zip([x-0.53 for x in x_range],Python_avg_salary):
    plt.text(a, b + 0.2, '%.2f' % b, ha='center', va='bottom', fontsize=6)
for a, b in zip([x-0.46 for x in x_range],PHP_avg_salary):
    plt.text(a, b + 0.1, '%.2f' % b, ha='center', va='bottom', fontsize=6)
for a, b in zip([x-0.39 for x in x_range],ui_avg_salary):
    plt.text(a, b + 0.20, '%.2f' % b, ha='center', va='bottom', fontsize=6)
for a, b in zip([x-0.32 for x in x_range],Android_avg_salary):
    plt.text(a, b + 0.1, '%.2f' % b, ha='center', va='bottom', fontsize=6)
for a, b in zip([x-0.25 for x in x_range],Algorithm_avg_salary):
    plt.text(a, b + 0.2, '%.2f' % b, ha='center', va='bottom', fontsize=6)
for a, b in zip([x-0.18 for x in x_range],hadoop_avg_salary):
    plt.text(a, b + 0.1, '%.2f' % b, ha='center', va='bottom', fontsize=6)
for a, b in zip([x-0.11 for x in x_range],DA_avg_salary):
    plt.text(a, b + 0.2, '%.2f' % b, ha='center', va='bottom', fontsize=6)
for a, b in zip([x-0.04 for x in x_range],AI_avg_salary):
    plt.text(a, b + 0.2, '%.2f' % b, ha='center', va='bottom', fontsize=6)
#添加title
plt.title('经验与月工资的关系')
#添加图例
plt.legend(loc=0,ncol=2)#图例及位置： 1右上角，2 左上角
plt.savefig('images/月平均工资条形图.jpg') #保存
plt.show() #显示
print('经验与月工资的关系条形图绘制完毕.')
#--------------------------------------------------------------------------------------

print('-'*20+'薪资待遇的词云绘制'+'-'*20)
welfare =zhaopin['welfare']
welfare_list =list(welfare)

cut_text =" ".join(jieba.cut(str(welfare_list)))
color_mask = cv2.imread('niu.jpg')
cloud = WordCloud(
       #设置字体，不指定就会出现乱码
       font_path=" C:\\Windows\\Fonts\\STXINGKA.TTF",
       #font_path=path.join(d,'simsun.ttc'),
       #设置背景色
       background_color='black',
       #词云形状
       mask=color_mask,
       #允许最大词汇
       max_words=2000,
       #最大号字体
       max_font_size=60
   )
wCloud = cloud.generate(cut_text)
wCloud.to_file('images/cloud.jpg')
plt.imshow(wCloud, interpolation='bilinear')
plt.axis('off')
plt.show()
#----------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------
print('-'*20+'探索计算机就业岗位的地理分布。'+'-'*20)
print('地理图绘制中...')
#绘制Geo地理图
#--java------------------------------------------------------------
def get_java_address(df):
    # 1.定义java职业所在的城市地址的列表
    java_address =[]
    for index, cols in df.iterrows():
        if (('java' in cols['name'])|('Java' in cols['name'])|('JAVA' in cols['name'])):
            java_address.append(cols['address'])
    # 计算列表中各个城市的数量
    java_address_data =Counter(java_address).most_common()
    #返回变量
    return java_address_data


#--python--------------------------------------------------------
def get_python_address(df):
    # 2.定义python职业所在的城市地址的列表
    python_address =[]
    for index, cols in df.iterrows():
        if (('Python' in cols['name'])|('python' in cols['name'])|('PYTHON' in cols['name'])):
            #将name中包含python字符的城市地址放进列表
            python_address.append(cols['address'])
    #计算列表中各个城市的数量
    python_address_data =Counter(python_address).most_common()
    #返回变量
    return python_address_data

#--php-------------------------------------------------------
def get_php_address(df):
    # 3. 定义java职业所在的城市地址的列表
    php_address =[]
    for index, cols in df.iterrows():
        if (('PHP' in cols['name'])|('php' in cols['name'])):
            # 将name中包含php字符的城市地址放进列表
            php_address.append(cols['address'])
    # 计算列表中各个城市的数量
    php_address_data =Counter(php_address).most_common()
    # 返回变量
    return php_address_data

#--UI--------------------------------------------------
def get_UI_address(df):
    # 4.定义java职业所在的城市地址的列表
    UI_address =[]
    for index, cols in df.iterrows():
        if (('ui' in cols['name'])|('UI' in cols['name'])):
            UI_address.append(cols['address'])
    # 计算列表中各个城市的数量
    UI_address_data =Counter(UI_address).most_common()
    # 返回变量
    return UI_address_data
#--Android----------------------------------------------
def get_Android_address(df):
    # 5. 定义Android职业所在的城市地址的列表
    Android_address =[]
    for index, cols in df.iterrows():
        if (('android' in cols['name'])|('安卓' in cols['name'])|('Android' in cols['name'])):
            Android_address.append(cols['address'])
    # 计算列表中各个城市的数量
    Android_address_data =Counter(Android_address).most_common()
    # 返回变量
    return Android_address_data

#--Algorithm------------------------------------------------
def get_Algorithm_address(df):
    # 6.定义算法工程师职业所在的城市地址的列表
    Algorithm_address =[]
    for index, cols in df.iterrows():
        if ('算法' in cols['name']):
            Algorithm_address.append(cols['address'])
    # 计算列表中各个城市的数量
    Algorithm_address_data =Counter(Algorithm_address).most_common()
    # 返回变量
    return Algorithm_address_data

#--hadoop------------------------------------------------
def get_hadoop_address(df):
    # 7.定义hadoop职业所在的城市地址的列表
    hadoop_address =[]
    for index, cols in df.iterrows():
        if (('hadoop|' in cols['name'])|('Hadoop' in cols['name'])):
            hadoop_address.append(cols['address'])
    # 计算列表中各个城市的数量
    hadoop_address_data =Counter(hadoop_address).most_common()
    # 返回变量
    return hadoop_address_data

#--DA--------------------------------------------------
def get_DA_address(df):
    # 8.定义数据分析职业所在的城市地址的列表
    DA_address =[]
    for index, cols in df.iterrows():
        if ('数据分析' in cols['name']):
            DA_address.append(cols['address'])
    # 计算列表中各个城市的数量
    DA_address_data =Counter(DA_address).most_common()
    # 返回变量
    return DA_address_data

#--AI-----------------------------------------------
def get_AI_address(df):
    # 9.定义人工智能职业所在的城市地址的列表
    AI_address =[]
    for index, cols in df.iterrows():
        if (('AI' in cols['name'])|('ai' in cols['name'])|('人工智能' in cols['name'])):
            AI_address.append(cols['address'])
    # 计算列表中各个城市的数量
    AI_address_data =Counter(AI_address).most_common()
    # 返回变量
    return AI_address_data

#--blockchain---------------------------------------
def get_blockchain_address(df):
    # 10.定义区块链职业所在的城市地址的列表
    blockchain_address =[]
    for index, cols in df.iterrows():
        if ('区块链' in cols['name']):
            blockchain_address.append(cols['address'])
    # 计算列表中各个城市的数量
    blockchain_address_data =Counter(blockchain_address).most_common()
    #返回变量
    return blockchain_address_data

#程序员岗位招聘所在城市
address =df.address

#所招聘岗位的城市和数量。

# #地理图标题设置
geo = Geo("程序员岗位分布情况", title_color="red",
          title_text_size=30,title_top=20,title_pos="center",
          width=1300,height=600,background_color='gray')
#---------------------------------------------------------
data1 = Counter(address).most_common()

java =get_java_address(df)
#------查看时可开启-----------------
"""
print('java')
print(java)
"""
python =get_python_address(df)
"""
print('python')
print(python)
"""
php =get_php_address(df)
"""
print('php')
print(php)
"""
ui =get_UI_address(df)
"""
print('ui')
print(ui)
"""
Android =get_Android_address(df)
"""
print('Android')
print(Android)
"""
Algorithm =get_Algorithm_address(df)
"""
print('Algorithm')
print(Algorithm)
"""
hadoop =get_hadoop_address(df)
"""
print('hadoop')
print(hadoop)
"""
AI =get_AI_address(df)
"""
print('AI')
print(AI)
"""
DA =get_DA_address(df)
"""
print('DA')
print(DA)
"""
blockchain =get_blockchain_address(df)
"""
print('blcokchain')
print(blockchain)
"""
#--------------------------------------------

#java
java_attr,java_value =geo.cast(java)
geo.add("java", java_attr,java_value, visual_range=[0, 150],visual_text_color='red', symbol_size=10, is_visualmap=True,effect_scale=25,type='effectScatter')
#python
python_attr,python_value =geo.cast(python)
geo.add("python", python_attr,python_value, visual_range=[0, 150],visual_text_color='red', symbol_size=10, is_visualmap=True,effect_scale=20,type ='effectScatter')
#php
php_attr,php_value =geo.cast(php)
geo.add("php", php_attr,php_value, visual_range=[0, 150],visual_text_color='red', symbol_size=10, is_visualmap=True,effect_scale=20,type ='effectScatter')
#ui
ui_attr,ui_value =geo.cast(ui)
geo.add("UI", ui_attr,ui_value, visual_range=[0, 150],visual_text_color='red', symbol_size=10, is_visualmap=True,effect_scale=25,type='effectScatter')
#Android
Android_attr,Android_value =geo.cast(Android)
geo.add("Android", Android_attr,Android_value, visual_range=[0, 150],visual_text_color='red', symbol_size=10, is_visualmap=True,effect_scale=25,type='effectScatter')
#Algorithm
Algorithm_attr,Algorithm_value =geo.cast(Algorithm)
geo.add("Algorithm", Algorithm_attr,Algorithm_value, visual_range=[0, 150],visual_text_color='red', symbol_size=10, is_visualmap=True,effect_scale=25,type='effectScatter')
#hadoop
hadoop_attr,hadoop_value =geo.cast(hadoop)
geo.add("Hadoop",hadoop_attr,hadoop_value,visual_range=[0, 150],visual_text_color='red', symbol_size=10, is_visualmap=True,effect_scale=25,type='effectScatter')
#AI
AI_attr,AI_value =geo.cast(AI)
geo.add("AI",AI_attr,AI_value,visual_range=[0, 150],visual_text_color='red', symbol_size=10, is_visualmap=True,effect_scale=25,type='effectScatter')

#DA
DA_attr,DA_value =geo.cast(DA)
geo.add("DA",DA_attr,DA_value,visual_range=[0, 150],visual_text_color='red', symbol_size=10, is_visualmap=True,effect_scale=25,type='effectScatter')
#blcokchain
blcokchain_attr,blcokchain_value =geo.cast(blockchain)
geo.add("blcokchain",blcokchain_attr,blcokchain_value,visual_range=[0, 150],visual_text_color='red', symbol_size=10, is_visualmap=True,effect_scale=25,type='effectScatter')
geo.render('岗位分布.html')
print('程序员岗位分布地理图绘制完成.')































