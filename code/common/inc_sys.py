#!/usr/bin/env python
# -*- coding: UTF-8 -*-  

#--------- 外部模块处理<<开始>> ---------#

#-----系统自带必备模块引用-----
import os # 操作系统模块
import sys # 系统模块
import time # 获得系统时间
import datetime # 获得日期
import re #正则处理
import linecache # 引用缓存读取文件模块

#-----系统外部需安装库模块引用-----
#-----DIY自定义库模块引用-----

#--------- 外部模块处理<<结束>> ---------#


#--------- 内部模块处理<<开始>> ---------#

# ---外部参变量处理

# ---全局变量处理

# 说明字典
dic_note = {
"版权":["LQAB工作室"],
"作者":["集体","吉更"],
"初创时间":["2018年10月"],
"功能":["自定义系统模块 1.0"],
}

# ---本模块内部类或函数定义区

#0 版本说明
def version(dic_p={}):
    print ("\n")
    print ("-----------------------------")
    [print("\n",x," --- ",re.sub("[\[,\],\',\,]", "", str(dic_p[x])),"\n") for x in dic_p] # 调试用
    print ("-----------------------------")

#1 简单的调试中断
def e(note_p):
    print (note_p) #显示标记信息
    exit()  # 终止执行
    
#2 参数处理 web框架可能不支持exec 需重新定制化处理 注意2 返回的一元参数字典键值一律为字符型
def args_get(args_p=""):

    dic_args ={}
    
    args_p = args_p.replace(":b'",":['")
    args_p = args_p.replace("',}","'],}")
    args_p = args_p.replace("', '",",")
    
    arr_t1 = re.findall('{(.*)}',args_p)
    #print (arr_t1) #调试用
    for x in arr_t1:
    
        str_t = str(x)
        str_t = str_t.strip()
        str_t = str_t.replace("'],","|~|")
        str_t = str_t.replace(":['","@#@")
        str_t = str_t.replace("']","")
        #print (str_t)
        arr_t2 = str_t.split("|~|")
        
        
        for y in arr_t2:
        
            #print (y) #调试用
            str_t2 = str(y)
            str_t2 = str_t2.strip()
            arr_t3 = str_t2.split("@#@")
            
            if (len(arr_t3) == 2):
                dic_args[arr_t3[0]] = arr_t3[1]
    
    return dic_args # 返回参数字典

#3 字符串截取 
def str_split(time_p,dot_p="."):
    time_p = str(time_p)
    arr_t = time_p.split(dot_p)
    return arr_t[0]

#4 过滤单双引号引号
def transfer_quotes(content):
    if content is None:
        return None
    else:
        string = ""
        for c in content:
            if c == "\"":
                string += "\\\""
            elif c == "'":
                string += "\\\'"
            elif c == "\\":
                string += "\\\\"
            else:
                string += c
        return string

#5 判断是否是数字 支持正负号
def is_num_by_except(num):
    try:
        int(num)
        return True
    except ValueError:
        print ("%s is not a number !" % num)
        return False

#6 获取脚本路径
def cur_file_dir():
    
     path = sys.path[0]
     #判断为脚本文件还是py2exe编译后的文件，如果是脚本文件，则返回的是脚本的目录，如果是py2exe编译后的文件，则返回的是编译后的文件路径
     if os.path.isdir(path):
         return path
     elif os.path.isfile(path):
         return os.path.dirname(path)
         
#7 编码硬补丁
def gbk_bug(txt_p):
    txt_p = txt_p.replace(u"\u2022","") #编码补丁1
    txt_p = txt_p.replace(u"\ufffd","") #编码补丁2
    txt_p = txt_p.replace(u"\ufeff","") #编码补丁3
    txt_p = txt_p.replace(u"\xa0","") #编码补丁4
    txt_p = txt_p.replace(u"\u264f","") #编码补丁5
    txt_p = txt_p.replace(u"\u30fb","") #编码补丁6
    txt_p = txt_p.replace(u"\0xac","") #编码补丁7
    txt_p = txt_p.replace(u"\u271a","") #编码补丁8
    txt_p = txt_p.replace(u"\xa1","") #编码补丁9
    return txt_p

#8 计算耗时函数
def time_cost(start_time_c):
    end_time_c = datetime.datetime.now() #赋值结束时间
    end_time_c = str(end_time_c-start_time_c)
    arr_1 = end_time_c.split(":")
    try:
        all_time = 3600*float(arr_1[0]) + 60*float(arr_1[1]) + float(arr_1[2])
    except:
        all_time = 0
        
    return all_time
    
#9 web下的javascript计时跳转
def skip_js(note_s,time_s,url_s,s_name="s0"):
    
    str_t = "\n"
    str_t += "<br><br><center>&nbsp;<font color='ff0000'><span id='" + s_name + "' color='ff0000'></span></font>&nbsp;秒" + note_s + "</center>"
    str_t += "<SCRIPT LANGUAGE='JavaScript'>"
    str_t += "function timer1(n,shower){"
    str_t += "this.time=n;"
    str_t += "this.url='';"
    str_t += "   this.shower=shower;"
    str_t += "}"
    str_t += "timer1.prototype.go=function(url){"
    str_t += "   this.url=url;"
    str_t += "   this.printinfo();"
    str_t += "};"
    str_t += "timer1.prototype.printinfo=function(){"
    str_t += "   var n=this.time;"
    str_t += "   var url=this.url;"
    str_t += "   var shower=this.shower;"
    str_t += "   var timer1;"
    str_t += "   (function(n){"
    str_t += "   print();"  
    str_t += "   function print(){"
    str_t += "     if(typeof(shower)=='string'){"
    str_t += "     document.getElementById(shower).innerHTML=n;"
    str_t += "     }else{"
    str_t += "     shower.innerHTML=n;"
    str_t += "     }"
    str_t += "    n--;"
    str_t += "    if(n<0){"
    str_t += "     clearInterval(timer1);"
    str_t += "     location.href=url;"
    str_t += "    }"
    str_t += "   }"
    str_t += "   timer1=setInterval(print,1000); " 
    str_t += "})(n)" 
    str_t += "};"
    str_t += "var timer1=new timer1(" + str(time_s) + ",'" + s_name + "');"
    str_t += "timer1.go('" + url_s + "');"
    str_t += "</SCRIPT>"

    return str_t

#10 字符串扩展类
class String_what(object):

    #判断是否是数字 支持正负号
    def is_num_by_except(self,str_p):
        try:
            int(str_p)
            return True
        except ValueError:
            return False
#11 随机生成n位的纯验证码 
def code_numb_rand(long_p=6):
    import random
    import math

    code_list = []
    numb_for = int(math.ceil(long_p/10))
    for j in range(numb_for):
        for i in range(10): # 0-9数字
            code_list.append(str(i))
            
    myslice = random.sample(code_list,long_p)  # 从list中随机获取6个元素，作为一个片断返回
    verification_code = ''.join(myslice) # list to string
    # print code_list
    # print type(myslice)
    return verification_code
    
#12 随机生成6位的验证码 
def code_char_rand():

    import random
    code_list = []
    for i in range(2):
        random_num = random.randint(0, 9) # 随机生成0-9的数字
        # 利用random.randint()函数生成一个随机整数a，使得65<=a<=90
        # 对应从“A”到“Z”的ASCII码
        a = random.randint(65, 90)
        b = random.randint(97, 122)
        random_uppercase_letter = chr(a)
        random_lowercase_letter = chr(b)

        code_list.append(str(random_num))
        code_list.append(random_uppercase_letter)
        code_list.append(random_lowercase_letter)
    verification_code = ''.join(code_list)
    return verification_code
    
#13 命令行格式下，参数字典的生成。
def args2dic(args_list_p=[]):
    
    dic_p = {}
    
    if args_list_p:
        
        i = 0
        
        for x in args_list_p:

            if (i > 0):
                if (x.split("=")):
                    dic_p[x.split("=")[0]] = x.split("=")[1]
                    #print (i,x,type(x)) # 调试用
            i += 1
        
    return dic_p
    
#14 web模式下的回退代码
def back_link(msg_p="请返回重新处理"):
    code_p = "[ <a href=\"javascript:history.go(-1)\">" + msg_p + "</a> ]"
    return code_p
    
#15 加解密
def secret_lqab(text_p,secret_if="yes",key_p="lqabisgood",salt_p = b'llddaaeeiissookk'):

    import base64 # base64加密模块
    import hashlib # hashlib加密模块
    import psutil # 系统库
    from cryptography.fernet import Fernet
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    #预处理
    password=bytes(key_p, encoding="utf-8")
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(),length=32,salt=salt_p,iterations=100000,backend=default_backend())
    jey = base64.urlsafe_b64encode(kdf.derive(password))
    key = Fernet(jey)
    result = text_p
    
    #加密
    if (secret_if == "yes"):
        
        try:
            result = result.encode("utf-8")
            result = str(key.encrypt(result)) # 加密
            result = result.replace("b'","")
            result = result.replace("'","")
        except:
            pass
    #解密
    if (secret_if == "no"):
        
        try:
            result = result.encode("utf-8")
            result = key.decrypt(result)
            result = result.decode("utf-8")

        except:
            pass
    
    return result

#16 无显示跳转js码
def skip_js_unshow(time_s,url_s,s_name):
    
    str_t = "\n"
    str_t += "<center><font id='" + s_name + "' color='ffffff'></font></center>"
    str_t += "<SCRIPT LANGUAGE='JavaScript'>"
    str_t += "function timer1(n,shower){"
    str_t += "this.time=n;"
    str_t += "this.url='';"
    str_t += "   this.shower=shower;"
    str_t += "}"
    str_t += "timer1.prototype.go=function(url){"
    str_t += "   this.url=url;"
    str_t += "   this.printinfo();"
    str_t += "};"
    str_t += "timer1.prototype.printinfo=function(){"
    str_t += "   var n=this.time;"
    str_t += "   var url=this.url;"
    str_t += "   var shower=this.shower;"
    str_t += "   var timer1;"
    str_t += "   (function(n){"
    str_t += "   print();"  
    str_t += "   function print(){"
    str_t += "     if(typeof(shower)=='string'){"
    str_t += "     document.getElementById(shower).innerHTML=n;"
    str_t += "     }else{"
    str_t += "     shower.innerHTML=n;"
    str_t += "     }"
    str_t += "    n--;"
    str_t += "    if(n<0){"
    str_t += "     clearInterval(timer1);"
    str_t += "     location.href=url;"
    str_t += "    }"
    str_t += "   }"
    str_t += "   timer1=setInterval(print,1000); " 
    str_t += "})(n)" 
    str_t += "};"
    str_t += "var timer1=new timer1(" + str(time_s) + ",'" + s_name + "');"
    str_t += "timer1.go('" + url_s + "');"
    str_t += "</SCRIPT>"
    
    return str_t
    
#17 模块内的多线程执行
def thread_it(func, *args):
    import threading # 线程模块
    t = threading.Thread(target=func, args=args) 
    t.setDaemon(True)   # 守护--就算主界面关闭，线程也会留守后台运行
    t.start()           # 启动
    # t.join()          # 阻塞--会卡死界面！
    
#18 秒与时分秒制式转化
def time_h_m_s(time_p="00-00-00",do_p=1):
    
    # 时间转秒
    if (do_p == 1):
    
        arr_t = time_p.split("-")
        
        if (len(arr_t) >=3):
            time_all_p = 3600*(int(arr_t[0])) + 60*(int(arr_t[1])) + (int(arr_t[2]))
        else:
            time_all_p = 0
            
        return time_all_p
            
    # 秒转时间
    if (do_p == 2):
        m, s = divmod(time_p, 60)
        h, m = divmod(m, 60)
        time_start_p = str(h) + "时" + str(m) + "分" + str(s) + "秒"
        return time_start_p
        
#19 延迟启动
def sleep_start(dic_p,after_p="00-00-00"):
    """
    cmd或shell模式下的延时启动
    """
    if (dic_p):
            
        time_all_p = time_h_m_s(time_p=after_p,do_p=1)
            
        if (time_all_p > 0):
            
            time_wait = time_all_p
            
            for i in range(time_all_p):
                time_start_p = time_h_m_s(time_p=time_wait,do_p=2)
                os.system( 'cls' )
                print ("主程序将在 " + str(time_start_p)+ " 后启动")
                time_wait = time_wait - 1
                
                time.sleep(1) #延迟一秒显示
        
        os.system( 'cls' )

#20 获得文本型字典 what_is 1 列表 2 元组 3 字典
def dic_txt_make(path_p="",what_is=3,part_p="\n",cache_if=1):
    
    list_p =[]
    tuple_p = ()
    dic_p = {}
    txt = ""
    if (cache_if == 1):
        
        cache_data = linecache.getlines(path_p)
        for line in range(len(cache_data)):
            txt += cache_data[line]
            
    else:
    
        with open(path_p, 'r', encoding="utf-8") as f:
            txt= f.read()

    if (txt):
    
        if (what_is == 3):
        
            try:
                list_p = txt.split(part_p)
            except:
                pass
            if (list_p):
                i=1
                for x in list_p:
                    if (len(x) > 0):
                        dic_p[x] = i
                        i += 1
                    
            return dic_p
            
        if (what_is == 2):
        
            try:
                tuple_p = txt.split(part_p)
            except:
                pass
            return tuple_p
            
        if (what_is == 1):
        
            try:
                list_p = txt.split(part_p)
            except:
                pass
            return list_p
    else:
    
        return txt
        
#21 base64编码解码
def base64_code(txt_p="",secret_if="yes"):
                
    result = "" # 结果文本
    import base64
    #转成bytes string
    bytesString = txt_p.encode(encoding="utf-8")
    # print(bytesString) #调试用
 
    #base64 编码
    
    if (secret_if == "yes"):
        result = base64.b64encode(bytesString)
        
        
    if (secret_if == "no"):
        result = base64.b64decode(bytesString)
    
    result = result.decode()
    return result

#--------- 内部模块处理<<结束>> ---------#

#---------- 主过程<<开始>> -----------#

def main():
    
    version(dic_p=dic_note) # 打印版本
    print ("hello world!")

if __name__ == '__main__':
    main()

#---------- 主过程<<结束>> -----------#