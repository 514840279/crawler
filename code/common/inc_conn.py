#!/usr/bin/env python
# -*- coding: UTF-8 -*-  

'''
{
"版权":"LDAE工作室",
"author":{
"1":"腾辉",
"2":"吉更"
}
"初创时间:"2017年3月",
}
'''

#--------- 外部模块处理<<开始>> ---------#

#-----系统自带必备模块引用-----
import sys
import os
#-----系统外部需安装库模块引用-----
import pymysql
#-----DIY自定义库模块引用-----
sys.path.append("..")
#--------- 外部模块处理<<结束>> ---------#


#--------- 内部模块处理<<开始>> ---------#

# ---外部参变量处理

# ---全局变量处理
# mysql数据库对象
class Conn_mysql():

    def __init__(self, host='localhost', user='root', passwd='root', db='application', port=3306):
        try:
            self.conn = pymysql.connect(host=host, user=user, passwd=passwd, db=db, port=port, charset="utf8")
            self.cur = self.conn.cursor()
        except Exception as e:
            print('事务处理失败', e)
    
    # 全表读数据方法
    def read_sql(self, sql):
        res = 0
        data = ()
        try:
            res = self.cur.execute(sql)
            data = self.cur.fetchall()
        except:
            pass
        return res, data
    
    # 分页读数据方法
    def read_sql_page(self, sql, values_p):
        res = 0
        data = ()
        try:
            res = self.cur.execute(sql)
            if (values_p > res):
                print ("number of pages is out \n")
                sys.exit(0)
            self.cur.scroll(values_p,'relative')
            data = self.cur.fetchall()
        except:
            pass
        return res, data
    
    # 数据写操作方法
    def write_sql(self, sql, *args):
        try:
            self.cur.execute(sql, *args)
            self.conn.commit()
            return True
        except:
            return False
        
    # 传递连接对象
    def get_conn(self):
        return self.conn
    
    # 关闭连接对象
    def close(self):
        self.conn.commit()
        self.cur.close()
        self.conn.close()
        
#--------- 内部模块处理<<结束>> ---------#

#---------- 主过程<<开始>> -----------#
def main():

    print ("")  # 防止代码外泄 只输出一个空字符

if __name__ == '__main__':
    main()
#---------- 主过程<<结束>> -----------#