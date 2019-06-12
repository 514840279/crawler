# -*- coding: utf-8 -*-


import datetime
import re



nowTime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') # 现在

nowDate=datetime.datetime.now().strftime('%Y-%m-%d') # 今天
today=datetime.date.today() # 今天



print(nowTime,nowDate,today)



# 汉字转阿拉伯数字
class WordToNum():

    CN_NUM = {
        '〇': 0, '一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9,
        '零': 0, '壹': 1, '贰': 2, '叁': 3, '肆': 4, '伍': 5, '陆': 6, '柒': 7, '捌': 8, '玖': 9,
        '0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
        '₀': 0, '₁': 1, '₂': 2, '₃': 3, '₄': 4, '₅': 5, '₆': 6, '₇': 7, '₈': 8, '₉': 9,
        '⁰': 0, '¹': 1, '²': 2, '³': 3, '⁴': 4, '⁵': 5, '⁶': 6, '⁷': 7, '⁸': 8, '⁹': 9,
        '貮': 2, '两': 2, '俩': 2, "今": 0, "明": 1, "后": 2, "昨":-1, "前":-2, '这': 0, '上':-1,
        '下': 1, '半':0.5
    }

    CN_UNIT = {
        '十': 10,
        '拾': 10,
        '百': 100,
        '佰': 100,
        '千': 1000,
        '仟': 1000,
        '万': 10000,
        '萬': 10000,
        '亿': 100000000,
        '億': 100000000,
        '兆': 1000000000000,
    }

    def chinese_to_arabic(self,cn: str) -> int:
        unit = 0  # current
        ldig = []  # digest
        for cndig in reversed(cn):
            if cndig in self.CN_UNIT:
                unit = self.CN_UNIT.get(cndig)
                if unit == 10000 or unit == 100000000:
                    ldig.append(unit)
                    unit = 1
            else:
                dig = self.CN_NUM.get(cndig)
                if unit:
                    dig *= unit
                    unit = 0
                ldig.append(dig)
        if unit == 10:
            ldig.append(10)
        val, tmp = 0, 0
        for x in reversed(ldig):
            if x == 10000 or x == 100000000:
                val += tmp * x
                tmp = 0
            else:
                tmp += x
        val += tmp
        return val


# 日期计算
class DateTimeSub():

    def subStrDate(self,wordstr):
        wordToNum = WordToNum()
        # 天
        if wordstr.find("天"):
            pattern = re.compile(r'.*?([〇|一|二|三|四|五|六|七|八|九|零|壹|贰|叁|肆|伍|陆|柒|捌|玖|0|1|2|3|4|5|6|7|8|9|₀|₁|₂|₃|₄|₅|₆|₇|₈|₉|⁰|¹|²|³|⁴|⁵|⁶|⁷|⁸|⁹||两|俩|今|明|后|昨|前|十|拾|百|佰|千|仟"]+天)')  # 查找数字
            result1 = pattern.findall(wordstr)
            for substr in result1:
                substr = str.replace(substr,'天','')
                substrnum = wordToNum.chinese_to_arabic(substr)
                newwordstr = str.replace(wordstr, substr, '%d' % substrnum)
                print(newwordstr)
                print(wordstr[wordstr.find("天")+1])
                if wordstr[wordstr.find("天")+1] == '前':
                    newdatetime = today- datetime.timedelta(days=substrnum)
                    print(newdatetime)
                if wordstr[wordstr.find("天") + 1] == '后':
                    newdatetime = today + datetime.timedelta(days=substrnum)
                    print(newdatetime)
                return newwordstr
        # 礼拜/周/星期
        if wordstr.find("周"):
            pattern = re.compile(r'.*?([〇|一|二|三|四|五|六|七|八|九|零|壹|贰|叁|肆|伍|陆|柒|捌|玖|0|1|2|3|4|5|6|7|8|9|₀|₁|₂|₃|₄|₅|₆|₇|₈|₉|⁰|¹|²|³|⁴|⁵|⁶|⁷|⁸|⁹||两|俩|十|拾|百|佰|上|下|个]+[礼拜|周|星期]+)')  # 查找数字
            result1 = pattern.findall(wordstr)
            print(result1)

        # 个月/
        if wordstr.find("个月"):
            pattern = re.compile(r'.*?([〇|一|二|三|四|五|六|七|八|九|零|壹|贰|叁|肆|伍|陆|柒|捌|玖|0|1|2|3|4|5|6|7|8|9|₀|₁|₂|₃|₄|₅|₆|₇|₈|₉|⁰|¹|²|³|⁴|⁵|⁶|⁷|⁸|⁹||两|俩|十|拾|上|下|个]+月)')  # 查找数字
            result1 = pattern.findall(wordstr)
            print(result1)
            for substr in result1:
                substr = str.replace(substr, '个月', '')
                substrnum = wordToNum.chinese_to_arabic(substr)
                newwordstr = str.replace(wordstr, substr, '%d' % substrnum)
                print(newwordstr)
                print(wordstr[wordstr.find("个月") + 2])
                if wordstr[wordstr.find("个月") + 2] == '前':
                    newdatetime = today - datetime.timedelta(days=substrnum*7)
                    print(newdatetime)
                if wordstr[wordstr.find("个月") + 2] == '后':
                    newdatetime = today + datetime.timedelta(days=substrnum*7)
                    print(newdatetime)
                return newwordstr



if __name__ == '__main__':
    wordToNum = WordToNum()
    print(wordToNum.chinese_to_arabic(cn='两万七千五百二十一'))
    print("-------------------------")
    print(wordToNum.chinese_to_arabic(cn='十八'))
    print("-------------------------")
    print(wordToNum.chinese_to_arabic(cn='一亿零一'))
    dateTimeSub = DateTimeSub()
    dateTimeSub.subStrDate('我在两天后出差')
    dateTimeSub.subStrDate('你半个月后是生日吧？')
    dateTimeSub.subStrDate('下个月十号？')
    dateTimeSub.subStrDate('下个礼拜日逛街')
    dateTimeSub.subStrDate('二百一十三天前我买了。。。')
    dateTimeSub.subStrDate('这周末签到？')