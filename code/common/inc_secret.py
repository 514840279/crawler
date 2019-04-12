#!/usr/bin/env python
# -*- coding: UTF-8 -*- 

'''
{
"版权":"LDAE工作室",
"author":{
"1":"power",
"2":"吉更",
}
"初创时间:"2017年3月",
}
'''
#--------- 外部模块处理<<开始>> ---------#

#-----系统自带必备模块引用-----

import sys # 操作系统模块1
import os # 系统模块
import base64 # base64加密模块
import pickle # 存取结构化数据模块
import hashlib # hashlib加密模块

#-----系统外部需安装库模块引用-----

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

#-----DIY自定义库模块引用-----
sys.path.append("..")

#--------- 外部模块处理<<结束>> ---------#


#--------- 内部模块处理<<开始>> ---------#

# ---外部参变量处理

# ---全局变量处理


# ---本模块内部类或函数定义区

# 加密的基础类
class Secret_base(object):

    def secret_do(self,file_p,key_p="ldae_is_good", secret_if=1):

        password=bytes(key_p, encoding="utf-8")
        salt = b"llddaaeeiissookk"
        kdf = PBKDF2HMAC(algorithm=hashes.SHA256(),length=32,salt=salt,iterations=100000,backend=default_backend())
        #kdf = PBKDF2HMAC(algorithm=hashes.SHA224,length=32,salt=b"123",iterations=100000,backend=default_backend())
        jey = base64.urlsafe_b64encode(kdf.derive(password))
        key = Fernet(jey)
    
        if secret_if == 1:
            
            try:
                
                t = open(file_p, 'r', encoding="utf-8")
                text = t.read()
                text = text.encode("utf-8")
                t.close()
            
            except:
            
                t = open(file_p, 'r')
                text = t.read()
                text = text.encode("utf-8")
                t.close()
        
            try:
            
                token = key.encrypt(text) # 加密
                #print(token) # 调试用
        
                f = open(file_p, 'wb')
                f.write(token)
                f.close()
                return True
    
            except:
            
                print ("\nThe running is bad!Try it again,please!\n")
                return False
                
        if secret_if == 2:
        
            text = open(file_p, 'rb').read()
            if (text[0:5] != b"gAAAA"):
                    print ("\nThe file is not a Secret file!Try it again,please!\n")
                    return False
            try:
            
                source_str = key.decrypt(text)
                source_str = source_str.decode("utf-8") # 解密
            
            except:
            
                print ("\nThe key is wrong!Try it again,please!\n")
                return False
            
            try:
        
                f = open(file_p, 'w', encoding="utf-8")
                f.write(source_str)
                f.close()
                return True
        
            except:

                f = open(file_p, 'w')
                f.write(source_str)
                f.close()
                return True
                
           