# -- coding: UTF-8 --

# 导入测试实例文件数据用，
from common.inc_csv import Csv_base

# DateUtils用日期计算工具
from datetime import datetime,  timedelta, date,timezone
from time import time, ctime, localtime, strftime, strptime, mktime
import re,json,calendar
# 寿星天文历 农历转公历 公历转农历
#import sxtwl
from common.inc_file import File_file

csv = Csv_base()
file = File_file()

class DateUtils:

    cn_num = {
        '〇': '0', '一': '1', '二': '2', '三': '3', '四': '4', '五': '5', '六': '6', '七': '7', '八': '8', '九': '9',
        '零': '0', '壹': '1', '贰': '2', '叁': '3', '肆': '4', '伍': '5', '陆': '6', '柒': '7', '捌': '8', '玖': '9',
        '貮': '2', '两': '2', '俩': '2', '十': '',
    }
    cn_date_day = {
        "大前天": -3,
        "大后天": 3,
        "明天": 1,
        "后天": 2,
        "昨天": -1,
        "今天": 0,
        "前天": -2,
    }
    en_date_mon = {
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
    cn_date_mon = {
        "本月": 0, "这个月": 0,
        "上个月": -1,
        "下个月": 1
    }
    cn_date_year = {
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
    cn_date_week = {
        "这周": 0, "这礼拜": 0, "这个礼拜": 0, "这星期": 0, "这个星期": 0,"本周": 0,"本星期": 0,"本礼拜": 0,
        "大上周": -2, "大上个礼拜": -2, "大上个星期": -2,
        "上周": -1, "上个礼拜": -1, "上礼拜": -1, "上个星期": -1, "上星期": -1,
        "大下周": 2, "大下个星期": 2, "大下个礼拜": 2,
        "下周": 1, "下星期": 1, "下个星期": 1, "下礼拜": 1, "下个礼拜": 2,
    }

    cn_date_jqmc = [
        "冬至", "小寒", "大寒", "立春", "雨水", "惊蛰", "春分", "清明", "谷雨", "立夏", "小满", "芒种",
        "夏至", "小暑", "大暑", "立秋", "处暑", "白露", "秋分", "寒露", "霜降", "立冬", "小雪", "大雪"
    ]

    # https://baike.baidu.com/item/世界动物日/1073877
    _jieri_ = {
        "元旦":"01月01日","New Year's Day":"01月01日",
        "国际大屠杀纪念日":"01月27日","The Holocaust and the United Nations Outreach Programme":"01月27日",

        "世界湿地日":"02月02日","World Wetlands Day":"02月02日","湿地日":"02月02日",
        "情人节":"02月14日","Valentine's Day":"02月14日",
        "国际母语日":"02月21日","International Mother Language Day":"02月21日",
        "反对殖民主义斗争日":"02月21日","The struggle against colonialism day":"02月21日",
        # 世界居住条件调查日(2月的最后一天)

        "国际海豹日": "03月01日","International Day of the Seal": "03月01日",
        "全国爱耳日": "03月03日","爱耳日": "03月03日","Ear Care Day": "03月03日",
        "青年志愿者服务日": "03月05日",
        "世界青光眼日": "03月06日","World Glaucoma Day": "03月06日",
        "国际劳动妇女节": "03月08日","国际妇女节": "03月08日","妇女节": "03月08日","International Women's Day": "03月08日",
        "保护母亲河日": "03月09日","Mother River Protection Day":"03月09日",
        "植树节": "03月12日",     "中国植树节": "03月12日","China Arbor Day": "03月12日",
        "白色情人节": "03月14日", "White Day": "03月14日",
        "国际警察日": "03月14日","International Policemen' Day": "03月14日",
        "世界消费者权益日": "03月15日","World Consumer Right Day": "03月15日","打假日": "03月15日","消费者权益日": "03月15日",
        "国际航海日": "03月17日","世界海事日": "03月17日",
        "世界森林日": "3月21日","World Forest Day": "03月21日", "森林日": "03月21日",
        "世界睡眠日": "03月21日","World Sleep Day":"03月21日","睡眠日":"03月21日",
        "国际消除种族歧视日": "03月21日","International Day for the Elimination of Racial Discrimination": "03月21日",
        "世界儿歌日": "03月21日",
        "世界水日":"03月22日","World Water Day":"03月22日",
        "世界气象日":"03月23日","World Meteorological Day":"03月23日","气象日":"03月23日",
        "世界防治结核病日":"03月24日","World Tuberculosis Day":"03月24日",
        "世界戏剧日": "03月27日","World Theatre Day":"03月27日",

        "愚人节":"04月01日","April Fools' Day":"04月01日",
        "国际儿童图书日": "04月02日","International Children's Book Day": "04月02日",
        "世界自闭症日": "04月02日",
        "巴勒斯坦儿童日": "04月05日",
        "世界卫生日":"04月07日","World Health Day":"04月07日",
        "世界高血压日":"04月07日",
        "反思卢旺达大屠杀国际日":"04月07日",
        "非洲环境保护日":"04月10日",
        "世界帕金森病日": "04月11日",
        "非洲自由日": "04月15日",
        "世界社会工作日": "04月15日",
        "世界血友病日": "04月17日",
        "国际古迹遗址日": "04月18日",
        "世界地球日":"04月22日","World Earth Day":"04月22日","地球日":"04月22日",
        "世界读书日":"04月23日",
        "世界防治疟疾日": "04月25日",
        "世界知识产权日":"04月26日","World Intellectual Property Day":"04月26日",
        "世界安全生产与健康日": "04月28日",
        "化学战受害者纪念日": "04月29日",
        "全国交通安全反思日": "04月30日",
        # ▪ 全球青年服务日(4月的第2或第3个周末)
        #▪ 世界儿童日(4月的第4个星期日)

        "国际劳动节":"05月01日","劳动节":"05月01日","International Labour Day":"05月01日","五一国际劳动节":"05月01日","国际劳动节":"05月01日",
        #"世界哮喘日":"05月03日","World Asthma Day":"05月03日","哮喘日":"05月03日",
        "世界新闻自由日":"05月03日",
        "中国青年节":"05月04日","青年节":"05月04日","Chinese Youth Day":"05月04日","五四青年节":"05月04日",
        "世界红十字日":"05月08日","World Red-Cross Day":"05月08日","红十字日":"05月08日",
        "战胜德国法西斯纪念日":"05月09日",
        "国际护士节":"05月12日","International Nurse Day":"05月12日","护士节":"05月12日",
        "国际家庭日":"05月15日","International Family Day":"05月15日","家庭日":"05月15日",
        "碘缺乏病防治日":"05月15日",
        "世界电信日":"05月17日","World Telecommunications Day":"05月17日","电信日":"05月17日",
        "国际博物馆日":"05月17日",
        "全国学生营养日":"05月20日",
        "世界计量日":"05月20日",
        "世界文化发展日": "05月21日",
        "国际生物多样性日": "05月22日",
        "国际牛奶日":"05月23日","International Milk Day":"05月23日",
        "非洲解放日": "05月25日",
        "世界向人体条件挑战日": "05月26日",
        "国际维和人员日": "05月29日",
        "世界无烟日":"05月31日","World No-Smoking Day":"05月31日","无烟日":"05月31日",
        # ▪ 世界防治哮喘日(5月的第1个周二)
        # ▪ 母亲节(5月的第2个星期日)

        "国际儿童节":"06月01日", "儿童节":"06月01日","International Children's Day":"06月01日",
        "世界牛奶日":"06月01日",
        "受侵略戕害的无辜儿童国际日":"06月04日",
        "世界环境日":"06月05日","International Environment Day":"06月05日","环境日":"06月05日",
        "全国爱眼日":"06月06日","爱眼日":"06月06日",
        "世界海洋日":"06月08日",
        "世界无童工日": "06月12日",
        "世界献血者日": "06月14日",
        "世界防治荒漠化和干旱日":"06月17日","World Day to combat desertification":"06月17日",
        "世界难民日": "06月20日",
        "国际奥林匹克日":"06月23日","International Olympic Day":"06月23日","奥林匹克日":"06月23日",
        "全国土地日":"06月25日","土地日":"06月25日",
        "国际禁毒日":"06月26日","International Day Against Drug Abuse and Illicit Trafficking":"06月26日","禁毒日":"06月26日",
        "联合国宪章日":"06月26日",
        #▪ 父亲节(6月的第3个星期日)


        "中国共产党诞生日":"07月01日", "建党节":"07月01日","Anniversary of the Founding of the Chinese Communist Party":"07月01日",
        "国际建筑日":"07月01日", "International Architecture Day":"07月01日","建筑日":"07月01日",
        "国际体育记者日":"07月02日",
        "中国人民抗日战争纪念日":"07月07日","抗日战争纪念日":"07月07日",
        "世界过敏性疾病日": "07月08日",
        "世界人口日":"07月11日","World Population Day":"07月11日",
        "曼德拉国际日": "07月18日",
        "人类月球日": "07月20日",
        "世界肝炎日": "07月28日",
        #  ▪ 国际合作节(7月的第1个星期六)


        "中国人民解放军建军节":"08月01日","建军节":"08月01日","Army Day":"08月01日",
        "国际土著人日": "08月09日", "世界土著人民国际日": "08月09日",
        "国际青年节":"08月12日","International Youth Day":"08月12日",
        "纳米比亚日": "08月26日",

        "国际扫盲日":"09月08日","International Anti-illiteracy Day":"09月08日","扫盲日":"09月08日",
        "世界教师日": "10月05日", "World Teachers' Day": "10月05日",
        "中国教师节":"09月10日","Teacher's Day":"09月10日","教师节":"09月10日",
        "世界预防自杀日":"09月10日",
        "国际民主日":"09月15日",
        "中国脑健康日":"09月16日",
        "国际臭氧层保护日":"09月16日","International Day for the Preservation of the Ozone Layer":"09月16日",
        "全国爱牙日":"09月20日","爱牙日":"09月20日",
        "世界停火日":"09月21日","World Cease-fire Day":"09月21日",
        "国际和平日":"09月21日","国际失智症日":"09月21日",
        "世界无车日": "09月22日",
        "世界旅游日":"09月27日","World Tourism Day":"09月27日",
        "国际翻译日": "09月30日",
        #▪ 世界急救日(9月的第2个星期六)
        #▪ 世界清洁地球日(9月的第3个周末)
        #▪ 国际聋人日(9月的第4个星期日)
        #▪ 世界海事日(9月的最后1周)

        "中华人民共和国国庆节":"10月01日", "国庆节":"10月01日","国庆":"10月01日","National Day":"10月01日",
        "国际音乐日":"10月01日","International Music Day":"10月01日",
        "国际老年人日":"10月01日","International Day of Older Persons":"10月01日",
        "国际和平与民主自由斗争日":"10月02日",
        "世界动物日":"10月04日","World Animal Day":"10月04日",
        "全国高血压日":"10月08日",
        "世界邮政日":"10月09日","World Post Day":"10月09日","邮政日":"10月09日",
        "世界精神卫生日":"10月10日","World Mental Health Day":"10月10日",
        "世界镇痛日": "10月11日",
        "世界关节炎日": "10月12日","世界60亿人口日": "10月12日",
        "世界保健日": "10月13日", "国际标准时间日": "10月13日",
        "世界标准日":"10月14日","World Standards Day":"10月14日",
        "国际盲人节":"10月15日","International Day of the Blind":"10月15日","盲人节":"10月15日",
        "世界农村妇女日":"10月15日","World Rural Women's Day":"10月15日","农村妇女日":"10月15日",
        "全球洗手日":"10月15日",
        "世界粮食日":"10月16日", "World Food Day":"10月16日","粮食日":"10月16日",
        "国际消除贫困日":"10月17日", "International Day for the Eradication of Poverty":"10月17日",
        "世界厨师日": "10月20日","世界骨质疏松日": "10月20日",
        "世界传统医药日": "10月22日",
        "联合国日":"10月24日", "United Nations Day":"10月24日",
        "世界发展新闻日": "10月24日",  "World Development Information Day": "10月24日",
        "世界发展信息日": "10月24日",
        "中国男性健康日":"10月28日","男性健康日":"10月28日",
        "万圣节":"10月31日",    "Halloween":"10月31日", "世界勤俭日":"10月31日",
        # ▪ 世界住房日(10月的第1个星期一)
        # ▪ 国际减轻自然灾害日(10月第2个星期三)

        "十月社会主义革命纪念日": "11月07日",
        "中国记者节":"11月08日",
        "消防宣传日":"11月09日",
        "吉尼斯世界纪录日":"11月09日",
        "世界青年节": "11月10日",
        "世界糖尿病日":"11月14日",    "World Diabetes Day":"11月14日",
        "国际宽容日": "11月16日",
        "国际大学生节":"11月17日","大学生节":"11月17日",
        "世界厕所日": "11月19日",
        "非洲工业化日": "11月20日",
        "世界问候日": "11月21日","世界电视日": "11月21日",
        "消除对妇女的暴力日": "11月25日",
        "国际消除对妇女的暴力日":"11月25日",    "International Day For the elimination of Violence against Women":"11月25日",
        "国际声援巴勒斯坦人民日": "11月20日",


        "世界爱滋病日":"12月01日",    "World AIDS Day":"12月01日","爱滋病日":"12月01日",
        "废除奴隶制国际日": "12月02日",
        "世界残疾人日":"12月03日",     "World Disabled Day":"12月03日","残疾人日":"12月03日", "国际残疾人日":"12月03日",
        "全国法制宣传日":"12月04日","法制宣传日":"12月04日",
        "国际志愿人员日": "12月05日",
        "世界足球日":"12月09日",    "World Football Day":"12月09日","足球日":"12月09日",
        "国际反腐败日": "12月09日",
        "国际民航日": "12月07日",
        "世界人权日": "12月10日",
        "世界强化免疫日": "12月15日",
        "国际移徙者日": "12月18日",
        "南南合作日": "12月19日",
        "国际篮球日": "12月21日",
        "圣诞节":"12月25日",    "Christmas Day":"12月25日",
        # ▪ 国际儿童电视广播日(12月的第2个星期日)

        # 1月最后一个星期日国际麻风节
        # 3月最后一个完整周的星期一中小学生安全教育日
        # 春分月圆后的第一个星期日复活节(Easter Monday)(有可能是3月22-4月25日间的任一天)
        # 5月第二个星期日母亲节(Mother's Day)
        # 5月第三个星期日全国助残日
        # 6月第三个星期日父亲节(Father's Day)
        # 9月第三个星期二国际和平日(International Peace Day)
        # 9月第三个星期六全国国防教育日
        # 9月第四个星期日国际聋人节(International Day of the Deaf)
        # 10月的第一个星期一世界住房日(World Habitat Day)
        # 10月的第二个星斯一加拿大感恩节(Thanksgiving Day)
        # 10月第二个星期三国际减轻自然灾害日(International Day for Natural Disaster Reduction)
        # 10月第二个星期四世界爱眼日(World Sight Day)
        # 11月最后一个完整周的星期一中小学生安全教育日星期四美国感恩节(Thanksgiving Day)

        "双十一": "11月11日", "双11": "11月11日",
        "淘宝购物节": "11月11日",
        "京东购物节": "06月18日",
    }


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

        # 阳历节假日 元旦，五一，国庆/十一
        datestr = self.zh_cn_en_jieri(datestr)

        # 阴历节日（新年/春节/大年初一/正月初一，端午，中秋/月饼节/八月十五，上元/正月十五/元宵节/灯节,鬼节/七月十五/中元节、下元节/十月十五）， TODO

        # 朔望月 转换日期 TODO
        #datestr = self.monday_to_date(datestr)

        # 获取准确的日期，并统一格式，返回
        resultDate = self.getAccurateDate(datestr)

        return resultDate

    # 使用替换特殊标点，正则匹配等替换日期
    def getAccurateDate(self,datestr):
        flag = True
        # 正常顺序的 Y%M%D%
        regex_str_sort_ymd = ".*?(\d{4}[年、/\.-]?)(\d{1,2}([月、/\.-]*))(\d{1,2}([日号、/\.]?))"
        sort_ymd = re.match(regex_str_sort_ymd, datestr)
        if sort_ymd is not None and flag and len(sort_ymd[0]) >= 8:
            monthstr = sort_ymd[2][0:2].replace("月",'').replace("、",'').replace("/",'').replace(".",'').replace("-",'')
            dayhstr = sort_ymd[4][0:2].replace("日", '').replace("号", '').replace("、", '').replace("/", '').replace(".", '').replace("-",'')
            newdatestr = date(int(sort_ymd[1][0:4]), int(monthstr),int(dayhstr)).strftime('%Y-%m-%d')
            datestr = datestr.replace(sort_ymd[0],newdatestr)
            flag=False

        # 错乱顺序的 M%D%Y%  D%M%Y%  M%Y%D%  TODO
        # 考虑话术中不应有乱序，只有文档中会乱，文档中一般如何区分年月日的
        regex_str_sort_no_ymd = ".*?((\d{1,4}([年月日号、/\.-]*)))"
        sort_no_ymd = re.match(regex_str_sort_no_ymd, datestr)
        if sort_no_ymd is not None and flag is True and len(sort_no_ymd[0]) >= 8:
            #print("sort_no_ymd", sort_no_ymd[0])
            # 如何拆解年月日
            flag = False

        # 日期不全的 M%D% 默认补全   一般处理 “MM月DD日” 类型的
        regex_str_sort_ymormd = ".*?((\d{1,2}([月、/\.-]+))(\d{1,2}([日号、/\.]?)))"
        sort_ymormd = re.match(regex_str_sort_ymormd, datestr)
        if sort_ymormd is not None and flag is True:
            #print(sort_ymormd[0], sort_ymormd[1], sort_ymormd[2], sort_ymormd[3], sort_ymormd[4])
            #print("sort_ymormd", datestr)
            monthstr = sort_ymormd[2][0:2].replace("月", '').replace("、", '').replace("/", '').replace(".",'').replace("-", '')
            if (int(monthstr) > 12):
                return datestr  # 区分不了月日的
            laststr = datestr[datestr.find(sort_ymormd[0]) + len(sort_ymormd[0]):datestr.find(sort_ymormd[0]) + len(sort_ymormd[0]) + 4]
            if re.match(r"\d*", laststr).span(0)[1] is not 0:
                return datestr  # 区分不了年月日的
            dayhstr = sort_ymormd[4][0:2].replace("日", '').replace("号", '').replace("、", '').replace("/",'').replace(".", '').replace("-", '')
            nowyear = datetime.now().year
            newdatestr = date(nowyear, int(monthstr), int(dayhstr)).strftime('%Y-%m-%d')
            datestr = datestr.replace(sort_ymormd[0], newdatestr)
            flag = False

        return datestr

    # 二十四节气查询 格式必须是 YYYY年节气
    def zh_cn_solar_terms(self,datestr):
        yearstr = re.findall(r'.*?(\d{4})年',datestr)
        if len(yearstr)>0:
            jsonstr = file.open_source_fullpath_read_line(file_path='jieqi.json',end=int(yearstr[0]),start=int(yearstr[0])-1)
            jsondic = json.loads(jsonstr[0].replace("'","\""))
            for jieqi in self.cn_date_jqmc:
                if datestr.find(jieqi) >= 0:
                    jieqidate = jsondic[yearstr[0]][jieqi]
                    datestr =datestr.replace(jieqi,jieqidate)
        return datestr

    # 阳历节假日 元旦，五一，国庆/十一
    def zh_cn_en_jieri(self,datestr):
        for cndate in self._jieri_.keys():
            if datestr.find(cndate) > -1:
                datestr = datestr.replace(cndate, self._jieri_[cndate])
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
                if newmon > 12:
                    newmon = 1
                    nowyear = nowyear + 1
                elif newmon < 1:
                    newmon = 12
                    nowyear = nowyear - 1
                datestr = datestr.replace(cnmon, str(nowyear)+"年"+str(newmon)+"月")

        # 中文替换年份
        for cnyear in self.cn_date_year.keys():
            if datestr.find(cnyear) > -1:
                nowyear = datetime.now().year
                newyear = nowyear + self.cn_date_year[cnyear]
                datestr = datestr.replace(cnyear, str(newyear)+"年")

        # 中文星期计算替换 指定星期几的可以计算准确日期，未指定为模糊时间,给定默认周一为日期
        if datestr.find("周") > -1 or datestr.find("礼拜") > -1 or datestr.find("星期") > -1:
            reg_week = r".*?((周|礼拜|星期)((\d)+|天|日)?)"
            sort_week = re.match(reg_week, datestr)

            if sort_week is not None:
                add_week = sort_week[3] if sort_week[3] is not None else 1
                if add_week == "天" or add_week == "日":
                    add_week = 7
                else:
                    add_week = int(add_week)
            else:
                add_week = calendar.MONDAY + 1

            for cndate in self.cn_date_week.keys():
                if datestr.find(cndate) > -1:
                    nowdate = datetime.now()
                    week = datetime.now().weekday()
                    newdate = nowdate + timedelta(weeks=(self.cn_date_week[cndate]), days=(add_week - week - 1))
                    datestr = datestr.replace(sort_week[0], newdate.strftime('%Y-%m-%d'))

        # 阴历转阳历 须文本标识 阴历、农历的字样 TODO


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
    print(DateUtils().getDate(datestr="上周六"))
    print(DateUtils().getDate(datestr="下礼拜天"))
    print(DateUtils().getDate(datestr="这周二"))
    print(DateUtils().getDate(datestr="下星期"))
    print(DateUtils().getDate(datestr="下周"))
    print(DateUtils().getDate(datestr="本周"))
    print(DateUtils().getDate(datestr="这周"))
    print(DateUtils().getDate(datestr="上周"))
    print(DateUtils().getDate(datestr="下星期"))
    print(DateUtils().getDate(datestr="上星期"))
    print(DateUtils().getDate(datestr="上礼拜"))
    print(DateUtils().getDate(datestr="下礼拜"))





if __name__ == '__main__':

    # 字符串短语转化日期格式化
    main()
    #run()
