
from common.Mysql_Utils import MyPymysqlPool
dbpool = MyPymysqlPool("default")

#cr = "create table sys_dic_utf8_code(code int primary key,info varchar(3),delete_flag int); "
#dbpool.update(cr);
for i in range(1,55296):
    print(i,chr(i) )
    sql ="insert into sys_dic_utf8_code(code,info,delete_flag) values(%d,'%s',0)" %(i,chr(i).replace("\\","\\\\").replace("'","\\'"))
    dbpool.insert(sql)

dbpool.dispose()

