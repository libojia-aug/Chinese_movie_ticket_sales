# -*- coding: UTF-8 -*- 
import random
import json
import urllib.request
import re
import json
import time
import logging
import os.path

import config

timeNow = int(time.time())

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logfile = config.rootDir + "Logs/" + \
    time.strftime('%Y%m%d%H', time.localtime(timeNow)) + '.log'
fh = logging.FileHandler(logfile, mode='w')
fh.setLevel(logging.DEBUG)  # 输出到file的log等级的开关
# 定义handler的输出格式
formatter = logging.Formatter(
    "%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
fh.setFormatter(formatter)
# 将logger添加到handler里面
logger.addHandler(fh)


def getText(url):
    # 在User-Agent列表中随机选择一个User-Agent
    user_agent = random.choice(config.ua_list)
    req = urllib.request.Request(url)

    # add_header()方法添加/修改一个HTTP报头
    req.add_header('User-Agent', user_agent)

    fails = 0
    while True:
        try:
            if fails >= config.tryTime:
                break
            res = urllib.request.urlopen(req, None, 3)
            textUrl = urllib.request.unquote(res.read().decode('utf8'))
        except Exception as e:
            fails += 1
            logger.error(
                "getText(): can not get respone: try again: " + str(fails))
            logger.error(str(e))
        else:
            break
    try:
        text = json.loads(textUrl)
        return text
    except Exception as e:
        logger.error("getText(): can not get url text: " + str(e))
        return


def getUrl(url):
    text = getText(url)
    try:
        data = text["data2"]
    except Exception as e:
        logger.error("getUrl(): can not get data2: " + str(e))
        return "err"
    for raw in data:
        Irank = raw["Irank"]
        mId = raw["mId"]
        MovieName = raw["MovieName"]
        BoxOffice = raw["BoxOffice"]
        sumBoxOffice = raw["sumBoxOffice"]
        movieDay = raw["movieDay"]
        boxPer = raw["boxPer"]

        path = config.rootDir + "data/"

        if not os.path.exists(path):
            os.makedirs(path)
        fo = open(path + time.strftime("%Y%m%d%H",
                                       time.localtime(timeNow)), "a")
        fo.write(Irank + config.Separator + mId + config.Separator + MovieName + config.Separator + BoxOffice +
                 config.Separator + sumBoxOffice + config.Separator + movieDay + config.Separator + boxPer + "\n")
        fo.close()

# {'Irank': '1', 'mId': '665526', 'MovieName': '海王', 'BoxOffice': '798.73', 'sumBoxOffice': '81885.55', 'movieDay': '6', 'boxPer': '80.38', 'MovieImg': '132277.jpg'}
# 排名，编号，名字，票房，总票房，上映时间，环比，图片
if __name__ == '__main__':
    logger.info("start")
    getUrl(config.url)
    logger.info("end")
