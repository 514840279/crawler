#!/usr/bin/env python
# -*- coding: UTF-8 -*-  

#--------- 外部模块处理<<开始>> ---------#

#-----系统自带必备模块引用-----

#-----DIY自定义库模块引用-----
from common.inc_conn import *
from common.Rule import Rule
# ---全局变量处理

applicationDb = Conn_mysql() # 读取配置信息
resultDb = Conn_mysql(db="result") # 结果入库

# ---本模块内部类或函数定义区
def run_it():


    # 读取网页地址列表
    sql = '''
           SELECT `md5`,`url`,`flag`
            FROM `result`.`sys_url_info`
            where flag = 0
            and url like '%https://www.qidian.com/all%'
    '''
    res,list_a = applicationDb.read_sql(sql)

    # 读取所有配置信息
    sql = '''
        SELECT 
          `uuid`,
          `delete_flag`,
          `discription`,
          `seed_name`,
          `seed_type`,
          `seed_url`,
          `request_proxy`
        FROM `application`.`sys_seed_url_info`
        WHERE delete_flag = 0
        LIMIT 0, 100
    '''
    rec,config_list = resultDb.read_sql(sql)

    # 判断每一个地址是否有配置信息
    # 引入通用模块
    name_model = "Currency"
    run_model = __import__(name_model)
    flag = True
    for a in  list_a: # 地址列表
        print("验证链接地址： " ,a )
        for  config in config_list: # 配置列表
            # 如果有进入采集程序
            if a[1].find(config[5]) > -1:
                print("开始分析网页")
                flag = False
                # 通用模块调用
                run_model.run_it(uuid=config[0],url=a[1],uri=config[5])
        if flag:
            print("缺少采集配置信息")
            # 如果没有自动添加新的配置信息，并提示用户进行修改 状态修改-1
            sql = "update sys_url_info set flag =-1 where md5='"+config[0]+"'"
            rule = Rule()
            applicationDb.write_sql(sql)
            sql = "INSERT INTO application.sys_seed_url_info(UUID,delete_flag, seed_url)VALUES ('%s','-1','%s') " %(rule.get_md5_value(rule.get_url_root(a[1])),a[1])
            applicationDb.write_sql(sql)
            # 并提示用户进行修改 TODO

        # 更新url
        sql = '''
                UPDATE `result`.`sys_url_info`
                SET `flag` = -1
                WHERE `url` = '%s'
            ''' % (a)
        resultDb.write_sql(sql)


#--------- 内部模块处理<<结束>> ---------#

#---------- 主过程<<开始>> -----------#

def main():
    #while True:
        run_it()

if __name__ == '__main__':
    main()
    
#---------- 主过程<<结束>> -----------#