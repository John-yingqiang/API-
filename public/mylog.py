# -*- coding: utf-8 -*-
# mylog.py
import logging
import subprocess
import os.path
import time
import sys
reload(sys)
sys.setdefaultencoding('utf8')

FILE_PATH = "C:/log.txt"

def set_file_path(fname=None, formater = "%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s %(message)s"):
    #eg: fname = "c:/Users/Administrator/log/build_0001.txt"
    if (fname == None):
        fname = FILE_PATH
    if not os.path.exists(os.path.dirname(fname)): os.mkdir(os.path.dirname(fname))
    '''
    logging.basicConfig(level=logging.DEBUG,
                        format=formater,
                        datefmt='%m-%d %H:%M',
                        filename=fname,
                        filemode='w+')
    # 定义一个Handler打印INFO及以上级别的日志到sys.stderr
    
    console = logging.StreamHandler()
    console.setLevel(logging.ERROR)
    # 设置日志打印格式
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    console.setFormatter(formatter)
    # 将定义好的console日志handler添加到root logger
    logging.getLogger('').addHandler(console)

    '''
    dir_path = os.path.dirname(fname)
    logger = logging.getLogger("Automation")
    logger.setLevel(logging.DEBUG)
    # log_stream = logging.StreamHandler()

    try:
        log_file = logging.FileHandler(fname, "a+")
        forma = logging.Formatter(formater)
        # log_stream.setFormatter(forma)
        # log_stream.setLevel(logging.DEBUG)
        log_file.setFormatter(forma)
        logger.addHandler(log_file)
        # logger.addHandler(log_stream)
    except Exception:
        print "current exception in mylog.py:{}".format(Exception)


def screenshot(browser, picture_dir):
    now_time = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
    my_pic = picture_dir + "/" + now_time + "_pic"
    browser.get_screenshot_as_png(my_pic)
    if not os.path.exists(picture_dir):
        os.mkdir(picture_dir)
    info(u"截图为：" + my_pic)
    # PICS.append(my_pic + ".png")
    # PICPATH.append(my_pic + ".png")

def debug(msg, *args, **kwargs):
    logger = logging.getLogger("Automation")
    logger.debug(msg, *args, **kwargs)

def info(msg, *args, **kwargs):
    logger = logging.getLogger("Automation")
    logger.info(msg, *args, **kwargs)

def error(msg, *args, **kwargs):
    logger = logging.getLogger("Automation")
    logger.error(msg, *args, **kwargs)

def do_system(cmd):
    try:
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)
    except subprocess.CalledProcessError as error:
        output = error.output
    return output
