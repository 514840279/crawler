# -- coding: UTF-8 --

# 导入测试实例文件数据用，
from common.inc_csv import Csv_base

# DateUtils用日期计算工具
from datetime import datetime,  timedelta, date, timezone
from time import time, ctime, localtime, strftime, strptime, mktime
import re

csv = Csv_base();

class DateUtils:
    cn_num = {
    '〇': '0', '一': '1', '二': '2', '三': '3', '四': '4', '五': '5', '六': '6', '七': '7', '八': '8', '九': '9', '零': '0',
    '壹': '1', '贰': '2', '叁': '3', '肆': '4', '伍': '5', '陆': '6', '柒': '7', '捌': '8', '玖': '9', '貮': '2', '两': '2','俩': '2','十': '',
    }
    cn_date_day={
        "大前天": -3,
        "大后天": 3,
        "明天": 1,
        "后天": 2,
        "昨天":-1,
        "今天": 0,
        "前天":-2,
    }
    en_date_mon={
        "Jan.": '01',
        "January":'01',
        "Feb.": '02',
        "February": '02',
        "Mar.": '03',
        "March": '03',
        "Apr.": '04',
        "April": '04',
        "May.": '05',
        "May": '05',
        "Jun.": '06',
        "June": '06',
        "Jul.": '07',
        "July": '07',
        "Aug.": '08',
        "August": '08',
        "Sept.": '09',
        "September": '09',
        "Sept.": '09',
        "September": '09',
        "Oct.": '10',
        "October": '10',
        "Nov.": '11',
        "November": '11',
        "Dec.": '12',
        "December": '12',
    }
    cn_date_mon={
        "本月": 0,
        "这个月":0,
        "上个月":-1,
        "下个月":1
    }
    cn_date_year={
        "今年":0,
        "去年":-1,
        "大前年":-3,
        "前年":-2,
        "明年":1,
        "来年":1,
        "下一年":1,
        "大后年":3,
        "后年":2
    }

    #resultDate=[]
    # 获取日期时间
    def getDate(self,datestr=""):
        if datestr == "":
            return ""
        # 转数字
        datestr = self.zh_cn_to_num(datestr)
        # 特殊转日期
        datestr = self.zh_cn_to_date(datestr)
        # 节气，节假日（端午，中秋），朔望月 此法转换主要使用阴历计算法 TODO
        #datestr = self.zh_cn_to_ccdate(datestr)
        # 获取准确的日期，并统一格式，返回
        resultDate= self.getAccurateDate(datestr)
        return resultDate

    # 使用替换特殊标点，正则匹配等替换日期
    def getAccurateDate(self,datestr):
        flag = True
        # 正常顺序的 Y%M%D%
        regex_str_sort_ymd = ".*?(\d{4}[年、/.-]?)(\d{1,2}([月、/.-]*))(\d{1,2}[日号、/.]?)"
        sort_ymd = re.match(regex_str_sort_ymd, datestr)
        if sort_ymd and len(sort_ymd.groups())>3 and flag:
            monthstr = sort_ymd[2][0:2].replace("月",'').replace("、",'').replace("/",'').replace(".",'').replace("-",'')
            newdatestr = date(int(sort_ymd[1][0:4]), int(monthstr),int( sort_ymd[4][0:2])).strftime('%Y-%m-%d')
            datestr = datestr.replace(sort_ymd[0],newdatestr)
            flag=False

        # 错乱顺序的 M%D%Y%  D%M%Y%  M%Y%D% TODO
        regex_str_sort_no_ymd = ".*?((\d{1,4}[年月日号、/.-]*){3})"
        sort_no_ymd = re.match(regex_str_sort_no_ymd, datestr)
        print("sort_no_ymd", sort_no_ymd)
        if sort_no_ymd and flag:
            print("sort_no_ymd", sort_no_ymd[0])
            flag = False

        # 日期不全的 Y%M% M%D%  默认补全 今年 这个月 TODO
        regex_str_sort_ymormd = ".*?(\d{1,4}([年月、/.-]*){2})"
        sort_ymormd = re.match(regex_str_sort_ymormd, datestr)
        if sort_ymormd and flag:
            print("sort_ymormd",datestr)
            flag = False


        return datestr

    # 特殊转、替换日期
    def zh_cn_to_date(self,datestr=""):
        # 中文准确日期 替换
        for cndate in self.cn_date_day.keys():
            if datestr.find(cndate) > -1:
                nowdate = datetime.now()
                newdate = nowdate + timedelta(self.cn_date_day[cndate])
                datestr = datestr.replace(cndate, newdate.strftime('%Y-%m-%d'))
        # 英文替换月份
        for enmonth in self.en_date_mon.keys():
            if datestr.find(enmonth) > -1:
                datestr = datestr.replace(enmonth, self.en_date_mon[enmonth]+"月")
        # 中文替换月份
        for cnmon in self.cn_date_mon.keys():
            if datestr.find(cnmon) > -1:
                nowmon = datetime.now().month
                newmon = nowmon + self.cn_date_mon[cnmon]
                datestr = datestr.replace(cnmon, str(newmon)+"月")
        # 中文替换年份
        for cnyear in self.cn_date_year.keys():
            if datestr.find(cnyear) > -1:
                nowyear = datetime.now().year
                newyear = nowyear + self.cn_date_year[cnyear]
                datestr = datestr.replace(cnyear, str(newyear)+"年")
        # 中文星期计算替换 指定星期几的可以计算准确日期，未指定为模糊时间 TODO

        return datestr

    # 汉字转阿拉伯数字
    def zh_cn_to_num(self,datestr):
        str_tem=""
        for i in datestr:
            if i in self.cn_num:
                str_tem += self.cn_num[i]
            else:
                str_tem+=i
        return str_tem

    if __name__ == '__main__':
        pass


# 测试实例
def main():
    datetools = DateUtils()

    strlines = csv.read_csv_file_line(file_path='2_测试实例文档.txt')
    for strline in strlines:
        resultDate = datetools.getDate(datestr= strline[0])
        print(strline[0],resultDate)

# 单实例测试
def run():
    datetools = DateUtils()
    resultDate = datetools.getDate(datestr="9月27")
    print(resultDate)

if __name__ == '__main__':

    # 字符串短语转化日期格式化
    #main()
    #run()

    tes =  re.search(r".*?((\d{1,4}([年月、/.-]*)))", "9月27",re.M|re.I)
    print(tes.groups())