#-*- coding:utf-8 -*-
import os
import requests
#打开文件夹
def open_file(file_name, size=0):
    for root, dirs, files in os.walk(file_name):
        for file in files:
            my_file = os.path.join(root, file)
            size = os.path.getsize(my_file)
            print root+'===size=='+str(size)
            if size == 0:
                os.remove(my_file)
                os.removedirs(root)
                print('success delete')
                continue
            log_txt = open(my_file)
            i = 0
            for line in log_txt:
                dowm_pic(line, root+'/'+'_'+str(i)+'.jpg')
                i+=1
            log_txt.close()
            os.remove(my_file)
#下载图片
def dowm_pic(url,save_file):
   try:
    pic = requests.get(url, timeout=20)
    fp = open(save_file.decode('utf-8').encode('cp936'),'wb')
    fp.write(pic.content)
    fp.close()
   except requests.exceptions.ConnectionError:
    pass
if __name__ == '__main__':
    file_name = 'F:/qq_friend_down_pic/qq_f_0222'
    open_file(file_name)