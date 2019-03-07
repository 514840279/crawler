#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from common.HtmlSource import HtmlSource
from common.Rule import Rule
from common.inc_conn import Conn_mysql
from common.inc_file import File_file,File_floder
from common.inc_csv import  Csv_base
import time
import uuid
import math
from lxml import html
import json
htmlSource = HtmlSource()
rule = Rule()
meituan_mysql = Conn_mysql( host='localhost', user='root', passwd='514840279@qq.com', db='app', port=3306,) # 生成MYSQL数据库索引数据实例


path = 'D:/app/meituan/'
# 多页
def main():
    sql ="""
    SELECT * FROM `meituan_city_url`
        WHERE ci_name = '美食'
        AND state=1
        ORDER BY city ASC
    """
    files = File_file()
    url = "https://meishi.meituan.com/i/api/channel/deal/list"

    headers ={"Origin": "https://meishi.meituan.com",
              "Host":"meishi.meituan.com"
              ,"Accept": "application/json"
              ,"Accept-Encoding": "gzip, deflate, br"
              ,"Accept-Language":"zh-CN,zh;q=0.9,en;q=0.8"
              ,'Referer': 'https://meishi.meituan.com/i/?ci=30&stid_b=1&cevent=imt%2Fhomepage%2Fcategory1%2F1'
              ,"Accept": "application/json"
              ,"User-Agent": "Mozilla/5.0 (Linux; U; Android 4.3; en-us; SM-N900T Build/JSS15J) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30"
              ,"Cookie":"__mta=209108909.1551529005971.1551955777272.1551955822655.37; _lxsdk_cuid=1693db239066c-0f343fb245dbaa-5d1f3b1c-1fa400-1693db23907c8; Hm_lvt_f66b37722f586a240d4621318a5a6ebe=1551518386; iuuid=2E3BF9E2CEBD41E4785995038C75AA1E9E0166E7BB22578436E1E9F7BCB42F70; _lxsdk=2E3BF9E2CEBD41E4785995038C75AA1E9E0166E7BB22578436E1E9F7BCB42F70; webp=1; wm_order_channel=mtib; _hc.v=71c2388f-3625-2203-629a-6a09a4e6d99c.1551518481; mtcdn=K; rvct=1010%2C197%2C1205%2C1068%2C151; a2h=4; isid=3A92B13CC95E59257FB53A0E692A592E; oops=b2nzRcwFi-gBaYFLXpJAO1uap4gAAAAA_QcAAE_Ef4UCUfjvEF-dnhF5aP_fPZ7kvLnrgEA976BqeFXwB53i3AtyH3LgYywIhXjzKw; logintype=fast; _lx_utm=utm_source%3D60030; userId=118752261; token=tqkQeweocQDlsoqgH5RyDrAUiKUAAAAA_QcAACGJxNZ4foDfWlBdRggXIHS4NEh5bAkvHHgPaLzdp1xAav1j4mfzUE9Epdoem3aFSQ; IJSESSIONID=frlmw1uga39011t9bgfu1yymf; u=118752261; __utmc=74597006; ci3=1; client-id=61e259b3-ec8f-4651-aaec-c366452d2749; uuid=af38a34d-cb68-4ef1-bc37-e96c3e2aa817; p_token=b2nzRcwFi-gBaYFLXpJAO1uap4gAAAAA_QcAAE_Ef4UCUfjvEF-dnhF5aP_fPZ7kvLnrgEA976BqeFXwB53i3AtyH3LgYywIhXjzKw; __utma=74597006.1186670783.1551518414.1551955447.1551961475.7; __utmz=74597006.1551961475.7.4.utmcsr=meishi.meituan.com|utmccn=(referral)|utmcmd=referral|utmcct=/i/; latlng=38.890466,121.520372,1551961474979; ci=527; cityname=%E6%98%8C%E9%82%91; __utmb=74597006.7.9.1551961480398; i_extend=C_b1Gimthomepagecategory11H__a; _lxsdk_s=169581cc0ff-0a1-bd9-bf%7C%7C8"}

    res,data = meituan_mysql.read_sql(sql)
    files = File_file()
    for row in data:
        file_name = row['pinyin']+".json"

        with open(path+file_name, 'r',encoding='utf-8') as f:
            print(f)
            json_data = json.load(f)
            crawler_data = json_data['crawlerMeta']
            crawler_data['deal_attr_23'] = ""
            crawler_data['deal_attr_24'] = ""
            crawler_data['deal_attr_25'] = ""
            crawler_data['poi_attr_20033'] = ""
            crawler_data['poi_attr_20043'] = ""
            crawler_data['sort'] = "default"
            crawler_data['stationId'] = 0

            crawler_data['lineId'] = 0
            crawler_data['cateId'] = 1

            areaObj = json_data['navBarData']['areaObj']
            #print(crawler_data,areaObj)
            for areas in areaObj:
                for area in areaObj[areas]:
                    print(area)
                    crawler_data['areaId']=area['id']
                    crawler_data['limit'] = 15
                    crawler_data['originUrl'] =  crawler_data['originUrl']+'&stid_b=1&cevent=imt%2Fhomepage%2Fcategory1%2F1'
                    headers['Referer'] = crawler_data['originUrl']

                    page = math.ceil(area['count'] / 15)

                    for a in range(0,page+1):
                        crawler_data['offset'] = a*15
                        print(crawler_data)
                        result_data = htmlSource.get_html(url_p=url,type_p='rp',post_data=crawler_data,headers_p=headers)
                        files.save_source(path=path+"data",file= area['name']+str(a)+".json",all_the_text=result_data)
                        #print(result_data)





if __name__ == '__main__': # 判断文件入口
    main()
