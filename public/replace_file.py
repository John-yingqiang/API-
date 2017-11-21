# -*- coding: utf-8 -*-
import os
import sys
import datetime
reload(sys)
sys.setdefaultencoding('utf8')

def modify_file(file):
    fd = open(file, "r+")
    time = os.path.getctime(file)
    date = datetime.datetime.fromtimestamp(time)
    create_time = date.strftime('%Y-%m-%d %H:%M:%S')
    time = os.path.getmtime(file)
    date = datetime.datetime.fromtimestamp(time)
    modify_time = date.strftime('%Y-%m-%d %H:%M:%S')

    lines = fd.readlines()
    for i, line in enumerate(lines):
        if line.find(u"开始时间") > 0:
            line += create_time
            lines[i] = line
        elif line.find(u"结束时间") > 0:
            line += modify_time
            lines[i] = line
            break
    fd.seek(os.SEEK_SET)
    fd.writelines(lines)
    fd.flush()
    fd.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print u"参数错误，请输入正确的文件名"
        exit(-1)
    else:
        modify_file(sys.argv[-1])
