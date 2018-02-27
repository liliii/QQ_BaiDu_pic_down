#coding=utf-8
#######################################################
#filename:test_xlutils.py
#author:defias
#date:xxxx-xx-xx
#function：向excel文件中写入数据
#######################################################
import xlrd
import xlutils.copy
#打开一个workbook
rb = xlrd.open_workbook('C:\\work\\worklog\\log\\20180108\\Fortune500Companies.xlsx')
wb = xlutils.copy.copy(rb)
#获取sheet对象，通过sheet_by_index()获取的sheet对象没有write()方法
ws = wb.get_sheet(0)
#写入数据
ws.write(1, 1, 'changed!')
#添加sheet页
wb.add_sheet('sheetnnn2',cell_overwrite_ok=True)
#利用保存时同名覆盖达到修改excel文件的目的,注意未被修改的内容保持不变
wb.save('C:\\work\\worklog\\log\\20180108\\Fortune500Companies.xlsx')