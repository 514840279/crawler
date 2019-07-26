#!/usr/bin/env python
# -*- coding: UTF-8 -*-  

'''
{
"版权":"LDAE工作室",
"author":{
"1":"腾辉",
"2":"吉庚"
}
"初创时间:"2017年3月",
}
'''

#--------- 外部模块处理<<开始>> ---------#

#-----系统自带必备模块引用-----

import sys # 操作系统模块1
import os # 操作系统模块2
import time # 时间模块
import psutil
import platform
import shutil # 删除文件
import zipfile # 压缩文件

#-----系统外部需安装库模块引用-----


#-----DIY自定义库模块引用-----
sys.path.append("..")
import csv #CSV组件
import common.inc_sys as inc_sys #自定义基础组件

#--------- 外部模块处理<<结束>> ---------#


#--------- 内部模块处理<<开始>> ---------#

# ---外部参变量处理

# ---全局变量处理


# ---本模块内部类或函数定义区

#继承字符扩展对象
class File_base(inc_sys.String_what):

    # 获取参数的当前路径
    def cur_file_dir(self,path):
        # 判断为脚本文件还是py2exe编译后的文件，如果是脚本文件，则返回的是脚本的目录，如果是py2exe编译后的文件，则返回的是编译后的文件路径
        if os.path.isdir(path):
            return path
        elif os.path.isfile(path):
            return os.path.dirname(path)

    # 遍历指定目录，显示目录下的所有文件名
    def eachFile(self,filepath):
        pathDir = os.listdir(filepath)
        for allDir in pathDir:
            child = os.path.join('%s%s' % (filepath, allDir))
            print(child)  # .decode('gbk')是解决中文显示乱码问题

    # 获取window 盘符
    def drives(self):
        sysstr = platform.system()
        dirve = []
        if (sysstr == "Windows"):
            dirves = psutil.disk_partitions()
            for item in dirves:
                dirve.append(item[1])
            print("Call Windows tasks")
        elif (sysstr == "Linux"):
            dirves = psutil.disk_partitions()
            for item in dirves:
                dirve.append(item[1])
            print("Call Linux tasks")
        else:
            dirves = psutil.disk_partitions()
            for item in dirves:
                dirve.append(item[1])
            print("Other System tasks")
        return dirve
        
    # 字节bytes转化kb\m\g
    def formatSize(self,bytes):
    
        try:
            bytes = float(bytes)
            kb = bytes / 1024
        except:
            print("传入的字节格式不对")
            return False

        if kb >= 1024:
            M = kb / 1024
            if M >= 1024:
                G = M / 1024
                return "%f G" % (G)
            else:
                return "%f M" % (M)
        else:
            return "%f K" % (kb)
            
    # 获取文件大小
    def getDocSize(self,path):
        
        try:
            size = os.path.getsize(path)
            return self.formatSize(size)
        except Exception as err:
            print(err)
            return False
    
    # 隐含链接提交
    def link_form(self,i_p=0,to_link_p="disk",api_is_p="script",dic_p={},path_name_p="c:~@~"):
        txt = ""
        # 分区链接
        
        txt +="<form name=\"" + to_link_p + str(i_p) + "\" method=\"post\" action=\"" + api_is_p + "\" id=\"" + to_link_p + str(i_p) + "\" accept-charset=\"utf-8\" onsubmit=\"document.charset='utf-8';\"  >\n"
        txt +=self.page_args_hide(dic_p,"page,submit,username,action,path_name,") #form参数隐式传递
        txt +="<input name=\"path_name\" type=\"hidden\" value=\"" + path_name_p + "\" />"
        txt +="<input name=\"action\" type=\"hidden\" value=\"partition\" />"
        txt +="<input type=\"Submit\" name=\"argsubmit\" id=\"s\" style=\"display:none\" />\n"
        txt +="</form>\n"
        
        return txt

    # form参数隐式传递
    def page_args_hide(self,dic_p,args_not_p):
    
        txt = ""
        for x in dic_p:
        
            if (x + "," in args_not_p):
                pass
            else:
                #print (x + "-" + y) #调试用
                txt += "<input name=\"" + x + "\" type=\"hidden\" value=\"" + dic_p[x] +"\" />\n"
            
        return txt
        
# 分区的 重命名 格式化
class File_driver(File_base):

    # 重命名
    def rename(self,driver,new_driver_name):
        print("分区重命名【"+driver+"】开始！")
        try:
            os.system("label "+ driver+" " + new_driver_name)
        except:
            print("分区重命名【" + driver + "】失败！")
        print("分区重命名【" + driver + "】结束！")
        return True

    # 格式化
    def format(self,driver,type="type"):
        print("分区格式化【"+driver+"】开始！")
        try:
            # /q 快速格式化， /y 没有确认直接执行 ，/fs 分区格式类型
            os.system("format "+ driver+" /Q /fs:" + type + " /y")
        except:
            print("分区格式化【" + driver + "】失败！")
        print("分区格式化【" + driver + "】结束！")
        return True

# 文件夹的 复制剪切粘贴更名 解压缩 加解密 统计（大小，文件数量，时间等）
class File_floder(File_base):
    
    # 添加 目录或文件 type = [dir|file]
    def add(self,path_p,type="dir"):
        
        try:
            if type == "dir":
                os.makedirs(path_p)
            elif type == "file":
                open(path_p,"w")

        except(FileExistsError):
            print("文件已存在！")
            
        return True

    # 修改文件（路径）名称
    def upd(self,path,file_name,new_file_name):
        os.rename(path+file_name, path+new_file_name)
        return True

    # 删除文件
    def remove(self,path,type="dir"):
        print("删除文件开始！")
        try:
            if type=="dir":
                # 清空文件夹
                for root, dirs, files in os.walk(path, topdown=False):
                    for name in files:
                        os.remove(os.path.join(root, name))
                    for name in dirs:
                        os.rmdir(os.path.join(root, name))
                # 删除文件夹
                os.rmdir(path)
            else:
                # 删除文件
                os.remove(path)
        except:
            print("删除文件失败！")
            return False
        print("删除文件成功！")
        return True

    # 复制文件文件夹
    def copy(self,path,new_path):
        print("复制文件开始！")
        for file in os.listdir(path):
            sourceFile = os.path.join(path, file)
            targetFile = os.path.join(new_path, file)
            if os.path.isfile(sourceFile):
                if not os.path.exists(new_path):
                    os.makedirs(new_path)
                if not os.path.exists(targetFile) or (
                    os.path.exists(targetFile) and (os.path.getsize(targetFile) != os.path.getsize(sourceFile))):
                    open(targetFile, "wb").write(open(sourceFile, "rb").read())
            if os.path.isdir(sourceFile):
                self.copy(sourceFile, targetFile)
        print("复制文件完成！")
        return True

    # 移动文件
    def move(self,path,new_path):
        shutil.move(path, new_path)
        return True

    # 压缩文件
    def compress(self,path,compress_file_name):
        print("压缩开始！")
        zipf = zipfile.ZipFile(compress_file_name, 'w')
        pre_len = len(os.path.dirname(path))
        for parent, dirnames, filenames in os.walk(path):
            for filename in filenames:
                pathfile = os.path.join(parent, filename)
                arcname = pathfile[pre_len:].strip(os.path.sep)  # 相对路径
                zipf.write(pathfile, arcname)
        zipf.close()
        print("压缩完成！")
        return True

    # 解压缩文件
    def uncompress(self,path,compress_file_name):
        print("解压缩开始！")
        if not os.path.exists(path):
            os.makedirs(path)
        zfobj = zipfile.ZipFile(compress_file_name)
        for name in zfobj.namelist():
            name = name.replace('\\', '/')

            if name.endswith('/'):
                os.mkdir(os.path.join(path, name))
            else:
                ext_filename = os.path.join(path, name)
                ext_dir = os.path.dirname(ext_filename)
                if not os.path.exists(ext_dir):
                    os.mkdir(ext_dir)
                outfile = open(ext_filename, 'wb')
                outfile.write(zfobj.read(name))
                outfile.close()
        print("解压缩完成！")
        return True

    # 加密
    def encrypt(self,path,file_name,script):

        return True

    # 解密
    def unencrypt(self, path, file_name, script):
        return True

    # 读取文件或文件夹（大小，文件数量，时间等）
    def read_list_info(self, path):
        print("读取目录信息开始！")
        dir_list=[]
        pathDir = os.listdir(path)
        for item in pathDir:
            dir=()
            t = os.stat(path=path+"//"+item)
            ctime =self.format_datetime(t.st_ctime) # 创建时间
            mtime = self.format_datetime(t.st_mtime)  # 创建时间
            atime = self.format_datetime(t.st_atime)  # 访问时间
            type = "dir"  # 目录、文件标识
            size = 0
            if os.path.isfile(path+"//"+item ):
                size = t.st_size
                type = "file"
            else:
                #size = self.getFileSize(filePath=path+"//"+item)  # 目录的大小 拖慢速度，不建议使用
                pass
            dir=(item,ctime,mtime,atime,size,type)
            dir_list.append(dir)
        print("读取目录信息完成！")
        return dir_list

    # 格式化 时间 格式 2017年5月31 11:28:56
    def format_datetime(self,date_time):
        date = ""
        date= time.localtime(date_time)
        date = str(date[0]) + "年" + str(date[1]) + "月" + str(date[2]) + " " + str(date[3]) + ":" + str(date[4]) + ":" + str(date[5])
        return date

    # 文件夹大小
    # 这里没有直接的函数接口,但可以通过计算所有文件的大小和算出文件夹大小用os.walk函数遍历文件夹
    def getFileSize(self,filePath, size=0):
        if (os.path.isfile(filePath)):
            size = os.path.getsize(filePath)
        else:
            for root, dirs, files in os.walk(filePath):
                for f in files:
                    size += os.path.getsize(os.path.join(root, f))
                    #print(f)
                for d in dirs:
                    self.getFileSize(d, size)
        return size

# 文件的  复制剪切粘贴更名 解压缩 加解密 统计（大小，文件数量，时间等） +++ 打开 与 编辑源码 上传下载
class File_file(File_floder):

    # 打开编辑源码
    def open_source1(self,path,file,encoding_='utf-8'):
        return self.open_source2(file_path=path+"/"+file,encoding=encoding_)

    # 打开编辑源码
    def open_source2(self,file_path,encoding_='utf-8'):
        file_object = open(file_path  ,"r",encoding=encoding_)
        try:
            all_the_text = file_object.read()
        finally:
            file_object.close()
        return all_the_text

    # 保存源码
    def save_source(self,path,file,all_the_text,encoding_='utf-8',mode='a+'):
        with open(path + "/" + file,mode=mode,encoding=encoding_) as file_object:
            file_object.write(all_the_text)
            file_object.close()
            return True




    # 上传
    def upload(self,path,file,file_name):

        pass

    # 下载
    def download(self,path,file_name):
    
        pass
        
    # 进行文件分割处理
    def split(self,fromfile,todir,chunksize=500*1024*1024):
        if not os.path.exists(todir):#check whether todir exists or not
            os.mkdir(todir)
        else:
            for fname in os.listdir(todir):
                os.remove(os.path.join(todir,fname))
        partnum = 0
        inputfile = open(fromfile,'rb')#open the fromfile
        while True:
            chunk = inputfile.read(chunksize)
            if not chunk:             #check the chunk is empty
                break
            partnum += 1
            filename = os.path.join(todir,('part%04d'%partnum))
            fileobj = open(filename,'wb')#make partfile
            fileobj.write(chunk)         #write data into partfile
            fileobj.close()
        return partnum

    # 进行文件合并处理
    def joinfile(self,fromdir, filename, todir):
        if not os.path.exists(todir):
            os.mkdir(todir)
        if not os.path.exists(fromdir):
            print('Wrong directory')
        outfile = open(os.path.join(todir, filename), 'wb')
        files = os.listdir(fromdir)  # list all the part files in the directory
        files.sort()  # sort part files to read in order
        for file in files:
            filepath = os.path.join(fromdir, file)
            infile = open(filepath, 'rb')
            data = infile.read()
            outfile.write(data)
            infile.close()
        outfile.close()
#--------- 内部模块处理<<结束>> ---------#

#---------- 主过程<<开始>> -----------#

def main():

    print ("") #调试用
    
if __name__ == '__main__':
    
    main()
    
#---------- 主过程<<结束>> -----------#