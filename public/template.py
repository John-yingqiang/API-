# -*- coding: utf-8 -*-
import requests
import json
import sys
import hashlib
import time
import os.path
from copy import deepcopy
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append("..\public")
from mylog import *

SHEET_NAME = "sheet_gl"
info("sheet_name:{}".format(SHEET_NAME))
LOG_PATH = "../log/test_log.txt"
set_file_path(LOG_PATH)
HEADER = {}
HEADER = {'Content-type': 'application/json; charset=utf-8'}
GLOBAL_VAR = {}
false = False
null = None

# 遍历一个字典结构
def check_dict(mydict, parent_list):
    global GLOBAL_VAR
    for key, value in mydict.iteritems():
        parent_list.append(key)
        if isinstance(value, dict):
            check_dict(value, parent_list)
        elif isinstance(value, list):
            for index, it in enumerate(value):
                parent_list.append(index)
                if isinstance(it, dict):
                    check_dict(it, parent_list)
                elif isinstance(it, basestring):
                    if it.startswith("kechuang"):
                        GLOBAL_VAR[it] = deepcopy(parent_list)
                parent_list.pop()
        else:
            if isinstance(value, basestring):
                if value.startswith("kechuang"):
                    GLOBAL_VAR[value] = deepcopy(parent_list)
        parent_list.pop()

def encode_password(password):
    tpass = hashlib.sha1(password.strip()).hexdigest().upper()
    info("encode:{}".format(tpass))
    return tpass

def makesure(func):
    def wrapper(para1):
        print u"测试开始"
        assert func(para1) == True
        print u"测试通过"
    return wrapper

@makesure
def call_API(test_dict, cert=None):
    """
    接口测试公共模板
    param:  test_dict  字典，格式：test_dict = {"访问地址":"www.baidu.com", "数据内容":"data", "调用方法":"post", "返回代码"：200, "返回结果":""}
    """
    global HEADER
    content_data = None

    # sheet_gl.json 保存变量的真实值
    try:
        with open("{}.json".format(SHEET_NAME)) as fg:
            key_dict = json.load(fg)
            if key_dict:
                for key, value in key_dict.items():
                    locals()[key] = value
                    eval(key)
    except Exception:
        key_dict = {} #第一次字典为空

    if test_dict[u"数据内容"]:
        info("test_dict___data:{}".format(test_dict[u"数据内容"]))
        content_data = eval((test_dict[u"数据内容"])) # 将变量用真实值替换过来
        info("content_data:{}".format(content_data))

    # 登录账户需要取出密码
    if "login" in test_dict[u"访问地址"]:
        if isinstance(content_data, dict):
            for i, k in content_data.items():
                if "pass" in i.lower():
                    content_data[i] = encode_password(k)

    content_data = json.dumps(content_data)
    info("address:{}, data:{}, header:{}".format(test_dict[u"访问地址"], content_data, HEADER))
    print u"开始发送数据"

    # verify=False 是调用http协议，verify=True 是调用https协议，其中带cert的是https的双向认证，不带cert是https单项认证
    if test_dict[u"调用方法"].lower() in u"post":
        r = requests.post(test_dict[u"访问地址"], data=content_data, verify=False, cert=cert, headers=HEADER)
    elif test_dict[u"调用方法"].lower() in u"get":
        if test_dict[u"数据内容"]:
            # get 请求时，带参数的需要传字典
            content_data = json.loads(content_data)
            r = requests.get(test_dict[u"访问地址"], params= content_data, verify=False, cert=cert,  headers=HEADER)
        else:
            r = requests.get(test_dict[u"访问地址"], verify=False, cert=cert, headers=HEADER)
    elif test_dict[u"调用方法"].lower() in u"put":
        r = requests.put(test_dict[u"访问地址"], data=content_data, verify=False, cert=cert,  headers=HEADER)
    elif test_dict[u"调用方法"].lower() in u"delete":
        r = requests.delete(test_dict[u"访问地址"], data=content_data, verify=False, cert=cert,  headers=HEADER)

    if r.status_code != 200:
        info("请求结果:\n{}\n".format(r.text))
        error(r.status_code)
        assert False == True

    data_in_file = r.json()
    if test_dict[u"返回结果"]:
        result = json.loads(test_dict[u"返回结果"])
    info("response result:{}".format(data_in_file))

    # 找出excel表中用户列出的变量的位置， 保存在GLOBAL_VAR字典中 GLOBAL_VAR:{u'kechuang_weiwen_1': [u'data', u'sympathy', u'reason']}
    if test_dict[u"变量对应关系表"]:
        temp_data = json.loads(test_dict[u"变量对应关系表"])
        parent_key = []
        if isinstance(temp_data, dict):
            check_dict(temp_data, parent_key)

    info("GLOBAL_VAR:{}".format(GLOBAL_VAR))
    if not test_dict[u"获取授权字段"]:
        if result["message"] == data_in_file["message"] and result["code"] == data_in_file["code"]:
            if not test_dict[u"是否比较返回结果"]:
                # 将GLOBAL_VAR中的变量替换成真实的值
                for key, value in GLOBAL_VAR.iteritems():
                    my_result = generate(value)
                    info("my_result:{}".format(my_result))
                    temp = eval(my_result)
                    info("temp:{}".format(temp))
                    key_dict[key] = temp.encode("utf-8")
                info("key_dict:{}".format(key_dict))
                # 将字典保存的变量回写到文件中
                with open("{}.json".format(SHEET_NAME), "w+") as fd:
                    json.dump(key_dict, fd, indent=4)
                    time.sleep(1)
                GLOBAL_VAR.clear()
                return True
            else:
                # 将返回结果和期望值进行比较
                return result==data_in_file
        else:
            error("excel期待结果:\n{}\n".format(result))
            error("实际请求结果:\n{}\n".format(data_in_file))
            print u"实际结果的message或者code与期望值不匹配\n实际message:{}, 实际code:{} \n期望message:{}, 期望code:{}".format(
                data_in_file["message"], data_in_file["code"], result["message"], result["code"]
            )

            return False
    else:
        # 登录接口返回access-token
        info("result:{}".format(data_in_file))
        HEADER["x-access-token"] = data_in_file["data"][test_dict[u"获取授权字段"]]
        return True
    info("\r\n")

# 将list_all的值组合起来，在返回结果中取值
def generate(list_all):
    y=""
    for i in list_all:
        if isinstance(i, basestring):
            y +='["{}"]'.format(i)
        else:
            y += '[{}]'.format(i)
    return "data_in_file" + y


