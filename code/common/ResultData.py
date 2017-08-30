#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# develop 514840279

from db.inc_conn import *
import re
resultDb = Conn_mysql(db="application") # 结果入库

class ResultData:

    # 检查映射配置信息
    def resultRefulence(self,rule_uuid,result,type):
        # 拼接查询映射关系表语句
        sql = "SELECT distinct  `table_uuid`FROM `application`.`sys_seed_result_ruler_info`WHERE ruler_uuid= '%s' "%(rule_uuid)
        re,data = resultDb.read_sql(sql=sql)
        # 检查有多少配置
        for table_uuid in data:
            self.writeToMysql(table_uuid[0],result,type)
    # 数据库入库
    def writeToMysql(self,table_uuid,result,type):
        # 查询入库的表名
        sql = "SELECT   `table_name` FROM  `application`.`sys_table_info` WHERE UUID = '%s'" %table_uuid
        redx, table_name = resultDb.read_sql(sql=sql)
        # 查询出完整的字段映射对应关系
        sql = "SELECT  `cols_name`,    `ruler_colum_name` FROM `application`.`sys_seed_result_ruler_info` WHERE table_uuid = '%s'"%table_uuid
        redx, data = resultDb.read_sql(sql=sql)
        # 拼接入库语句
        #sql =" insert into %s (%s) values(%s)"
        col=""
        for i in  range(len(data)):
            if(i >0):
                col = col +","
            col = col + data[i][0]

        if type == 'list':
            print("列表模板信息入库！")
            # 读取映射信息
            for info in  result:
                info = self.tupleDataToDic(info)
                value = ""
                for i in  range(len(data)):
                    if (i > 0):
                        value = value + ","
                    value = value + "'"+ re.sub(r"[','\"\]\[]","",str(info[data[i][0]])).strip() +"'"
                # 拼接入库语句
                sql = "insert into %s (%s) values(%s)"%(table_name[0][0],col,value)
                resultDb.write_sql(sql=sql)
        else:
            print("详细模板信息入库！")
            info = self.tupleDataToDic(result)
            value = ""
            for i in range(len(data)):
                if (i > 0):
                    value = value + ","
                value = value + "'" + re.sub(r"[','\"\]\[]","",str(info[data[i][0]])).strip() + "'"
            # 拼接入库语句
            sql = "insert into %s (%s) values(%s)" % (table_name[0][0], col, value)
            resultDb.write_sql(sql=sql)

    def tupleDataToDic(self,info):
        dic ={}
        for i in info:
            dic[i[0]]=i[1]
        return dic

    def main(self):
        print("")

if __name__ == '__main__':
    print("")