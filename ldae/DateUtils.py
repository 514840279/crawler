# -- coding: UTF-8 --

# 导入测试实例文件数据用，
from common.inc_csv import Csv_base

# DateUtils用日期计算工具
from datetime import datetime,  timedelta, date, timezone
from time import time, ctime, localtime, strftime, strptime, mktime
import re
# 寿星天文历 农历转公历 公历转农历
import sxtwl

csv = Csv_base();


class DateUtils:

    cn_num = {
        '〇': '0', '一': '1', '二': '2', '三': '3', '四': '4', '五': '5', '六': '6', '七': '7', '八': '8', '九': '9',
        '零': '0', '壹': '1', '贰': '2', '叁': '3', '肆': '4', '伍': '5', '陆': '6', '柒': '7', '捌': '8', '玖': '9',
        '貮': '2', '两': '2', '俩': '2', '十': '',
    }
    cn_date_day ={
        "大前天": -3,
        "大后天": 3,
        "明天": 1,
        "后天": 2,
        "昨天": -1,
        "今天": 0,
        "前天": -2,
    }
    en_date_mon ={
        "Jan.": '01', "January": '01',
        "Feb.": '02', "February": '02',
        "Mar.": '03', "March": '03',
        "Apr.": '04', "April": '04',
        "May.": '05', "May": '05',
        "Jun.": '06', "June": '06',
        "Jul.": '07', "July": '07',
        "Aug.": '08', "August": '08',
        "Sept.": '09', "September": '09',
        "Sept.": '09', "September": '09',
        "Oct.": '10', "October": '10',
        "Nov.": '11', "November": '11',
        "Dec.": '12', "December": '12',
    }
    cn_date_mon={
        "本月": 0, "这个月": 0,
        "上个月": -1,
        "下个月": 1
    }
    cn_date_year={
        "今年": 0,
        "去年": -1,
        "大前年": -3,
        "前年": -2,
        "明年": 1,
        "来年": 1,
        "下一年": 1,
        "大后年": 3,
        "后年": 2
    }
    cn_date_week ={
        "这周": 0, "这礼拜": 0, "这个礼拜": 0, "这星期": 0, "这个星期": 0,
        "大上周": -2, "大上个礼拜": -2, "大上个星期": -2,
        "上周": -1, "上个礼拜": -1, "上礼拜": -1, "上个星期": -1, "上星期": -1,
        "大下周": 2, "大下个星期": 2, "大下个礼拜": 2,
        "下周": 1, "下星期": 1, "下个星期": 1, "下礼拜": 1, "下个礼拜": 2,
    }

    cn_date_jqmc = [
        "冬至", "小寒", "大寒", "立春", "雨水", "惊蛰", "春分", "清明", "谷雨", "立夏", "小满", "芒种",
        "夏至", "小暑", "大暑", "立秋", "处暑", "白露", "秋分", "寒露", "霜降", "立冬", "小雪", "大雪"
    ]

    #resultDate=[]
    # 获取日期时间
    def getDate(self,datestr=""):
        if datestr == "":
            return ""
        # 转数字
        datestr = self.zh_cn_to_num(datestr)
        # 特殊转日期
        datestr = self.zh_cn_to_date(datestr)
        # 节气转换日期，取值必须包含年 节气计算每年，每个节气参数不同
        datestr = self.zh_cn_solar_terms(datestr)

        # 节假日 新年，五一，国庆，十一（春节，端午，中秋）， TODO
        # 朔望月 转换日期 TODO
        #datestr = self.zh_cn_to_ccdate(datestr)
        # 获取准确的日期，并统一格式，返回
        resultDate = self.getAccurateDate(datestr)
        return resultDate

    # 使用替换特殊标点，正则匹配等替换日期
    def getAccurateDate(self,datestr):
        flag = True
        # 正常顺序的 Y%M%D%
        regex_str_sort_ymd = ".*?(\d{4}[年、/\.-]?)(\d{1,2}([月、/\.-]*))(\d{1,2}([日号、/\.]?))"
        sort_ymd = re.match(regex_str_sort_ymd, datestr)
        if sort_ymd and flag and len(sort_ymd[0]) >= 8:
            monthstr = sort_ymd[2][0:2].replace("月",'').replace("、",'').replace("/",'').replace(".",'').replace("-",'')
            newdatestr = date(int(sort_ymd[1][0:4]), int(monthstr),int(sort_ymd[4][0:2])).strftime('%Y-%m-%d')
            datestr = datestr.replace(sort_ymd[0],newdatestr)
            flag=False

        # 错乱顺序的 M%D%Y%  D%M%Y%  M%Y%D%  TODO
        # 考虑话术中不应有乱序，只有文档中会乱，文档中一般如何区分年月日的
        regex_str_sort_no_ymd = ".*?((\d{1,4}([年月日号、/\.-]*)){3})"
        sort_no_ymd = re.match(regex_str_sort_no_ymd, datestr)
        if sort_no_ymd and flag and len(sort_no_ymd[0]) >= 8:
            print("sort_no_ymd", sort_no_ymd[0])
            # 如何拆解年月日
            flag = False

        # 日期不全的 Y%M% M%D% 19/9/9 默认补全 今年 这个月   TODO
        regex_str_sort_ymormd = ".*?(\d{1,4}([年月、/\.-]*){2})"
        sort_ymormd = re.match(regex_str_sort_ymormd, datestr)
        if sort_ymormd and flag:
            print("sort_ymormd",datestr)
            flag = False

        return datestr

    # 二十四节气查询
    def zh_cn_solar_terms(self,datestr):
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
                nowyear = datetime.now().year
                nowmon = datetime.now().month
                newmon = nowmon + self.cn_date_mon[cnmon]
                datestr = datestr.replace(cnmon, str(nowyear)+"年"+str(newmon)+"月")

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
        str_tem = ""
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
    strlines = csv.read_csv_file_line(file_path='2_测试实例文档.txt')
    for strline in strlines:
        resultDate = DateUtils().getDate(datestr= strline[0])
        print(strline[0],resultDate)

# 单实例测试
def run():
    print(DateUtils().getDate(datestr="25号6月今年"))

if __name__ == '__main__':

    # 字符串短语转化日期格式化
    main()
    #run()
