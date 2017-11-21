# -*- coding: utf-8 -*-
import sys
import os
import re
reload(sys)
import shutil
import codecs
sys.setdefaultencoding('utf-8')
sys.path.append("..\public")
from mylog import *
from explainExcel import *

LOG_PATH = "../log/test_log.txt"
set_file_path(LOG_PATH)

def generate_func(my_dict, index, file_name): # my_dict是一个case, 即从excel里面读出的每一行
    """
    此方法根据传入的参数自动生成../test/test_case_all.py, test_case_all.py就是测试脚本
    param:  my_dict   参数为字典
    """
    url_list = my_dict[u"访问地址"].split(":")[-1].split("/")
    temp_str = ""

    if not os.path.exists("../testcase/{}".format(file_name)):
        print "../testcase/{}.py".format(file_name)
        exit(-1)

    for index_me, i in enumerate(url_list):
        if index_me == 0:
            pass
        else:
            temp_str += "_" + i
    # 以excel里面的访问网址的最后一个单词构造test case的函数名字

    if not os.path.exists("../data/newfile.crt.pem") and not os.path.exists("../data/newfile.key.pem"): # http协议，不用带证书
        string = "def test_{0}{1}(data={2}):\n    '''{3}'''\n    call_API(data)\n".format(str(index), temp_str, my_dict, my_dict[u"用例名称"])
    else:
        string = "def test_{0}{1}(data={2}):\n    '''{3}'''\n    call_API(data, cert=('../data/newfile.crt.pem', '../data/newfile.key.pem'))\n".format(
                    str(index), temp_str, my_dict, my_dict[u"用例名称"])

    with codecs.open("../testcase/{}".format(file_name),"a+", "utf-8") as fd:
        fd.writelines(string) # 将string写到文件

def is_float(s):
    return sum([n.isdigit() for n in s.strip().split('.')]) == 2

def convert_values(value):
    if is_float(value):
        second = [int(n) for n in value.strip().split(".") if n.isdigit]
        if second[1] == 0:
            return second[0]
        else:
            return value
    else:
        return value

def generate_test_case():
    workbook, sheet_names = read_excel("../data/data_model.xlsx") # 解析excel的每一行到case_list列表

    for sheet_name in sheet_names:
        file_name = "test_{}.py".format(sheet_name)
        shutil.copyfile("./template.py", "../testcase/test_{}.py".format(sheet_name))  # 先拷模板文件
        case_list = read_sheet(workbook, sheet_name)
        case_dict = {}
        for case in case_list:
            try:
                if case[u"执行步骤"]:
                    case_dict[convert_values(case[u"执行步骤"])] = case
            except Exception:
                error(u"Excel数据源有问题，请核对".format(Exception))
                print Exception
                exit(-1)

        for index, case in case_dict.iteritems():
            generate_func(case, index, file_name)


if __name__ == "__main__":
    # info("case_list:\n{}\n".format(CASE_LIST))
    generate_test_case()
