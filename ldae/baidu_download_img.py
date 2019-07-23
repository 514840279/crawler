# -- coding: UTF-8 --

from common.inc_csv import Csv_base
from common.inc_file import File_floder
import requests
if __name__ == '__main__':
    file_path = '../data/百科候选关键词.csv'
    folder_path ="../data/百科候选关键词/img"
    floder = File_floder()
    floder.add(folder_path)

    file = Csv_base()
    list = file.read_csv_file(file_path)
    for row in list:
        try:
            img_url = str(row[4]).replace('`','')
            if(img_url!=''):
                img_name=img_url.split("/")[-1]
                if(img_name.find("?")>-1):
                    img_name = img_name[0:img_name.find("?")]
                #img_content = requests.get(img_url).content
                #with open('../data/百科候选关键词/img/%s.jpg' % img_name, 'wb') as f:
                #    f.write(img_content)
                rw_str=[img_url,img_name,row[11].replace('`','')]
                file.write_csv_file_line(file_path="../data/百科候选关键词_img.csv",str=rw_str)
        except Exception as e:
            print(e)
