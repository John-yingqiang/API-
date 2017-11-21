#-*- coding:utf-8 -*-
import xlrd
import os
import copy
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from mylog import *

def read_excel(file_path):
    if not os.path.exists(file_path):
        info("文件不存在：{}".format(file_path))
        exit(-1)

    workbook = xlrd.open_workbook(file_path)  # 打开文件
    sheet_names = workbook.sheet_names()
    return workbook, sheet_names

def read_sheet(workbook, sheet_name):
    '''
    此方法用于读取excel，把excel每一行作为一个列表元素，返回一个列表
    param:   file_path  excel 文件的路径
    return:  list
    '''
    case_list = []
    row_dict = {}
    sheet1 = workbook.sheet_by_name(sheet_name)

    for row in range(2, sheet1.nrows):
        for col in range(sheet1.ncols):
            row_dict[sheet1.cell(1, col).value] = unicode(sheet1.cell(row, col).value).replace("\n", "") # 读取excel每一行，{"调用方法":"post", "访问网址":""}
        case_list.append(copy.deepcopy(row_dict))
        row_dict.clear()
    return case_list

if __name__ == '__main__':
    path = "C:/Users/Administrator/Desktop/data.xlsx"
    print read_excel(path)
