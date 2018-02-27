#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 文件名：ReplaceTXT.py
import os
import xlwt
#1.创建一个excell文件
workbook = xlwt.Workbook() #注意Workbook的开头W要大写
#2.创建一个sheet
sheet1 = workbook.add_sheet('sheet1',cell_overwrite_ok=True)
#文件名
file_x = open('E:\\名人名单\\中国企业.txt'.decode('utf-8').encode('cp936'))#file_y = open('E:\\model_output_log\\y\\_iter_36000_yhand_output.txt')
# 临时变量，sheet的行
temp = 0
for line in file_x.readlines():
    line = line.strip('\n')
    try:
        #.出现的位置
        first = line.index('.')
        #空格出现的位置
        last = line.index(' ')
        #需要的字符串
        company = line[first + 1:last+1].decode('cp936')
        #将字符串写到sheet的第temp行0列
        sheet1.write(temp, 0, company)
    except:
        pass
    #行加一
    temp += 1
    #保存Excel文件到指定路径
workbook.save('C:\\work\\worklog\\log\\20180108\\Fortune500Companies.xlsx')
#释放资源
file_x.close()
