#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2022/8/25 23:28
# @Author  : Cl0udG0d
# @File    : main.py
# @Github: https://github.com/Cl0udG0d
import datetime
import logging
import os
import dingtalkchatbot.chatbot as cb
import requests
import re



github_token = os.environ.get("github_token")
webhook= os.environ.get("webhook")
# webhook= "https://oapi.dingtalk.com/robot/send?access_token=d8c16a1142ae1e3077d05234b73826b1b65ec56c38b9ff83564e8b317f372d04"
secretKey= os.environ.get("secretKey")
# secretKey= "SEC33f24a184e46aecd0b2e2cad1df0457d6820cc1d75430880420aca97d54c24f6"
keywords=os.environ.get("keywords")
CleanKeywords=os.environ.get("CleanKeywords")

github_headers = {
    'Authorization': "token {}".format(github_token)
}

def checkEnvData():
    if not github_token:
        logging.error("github_token 获取失败")
        exit(0)
    elif not webhook:
        logging.error("钉钉 webhook 获取失败")
        exit(0)
    elif not secretKey:
        logging.error("钉钉 secretKey 获取失败")
        exit(0)
    else:
        logging.info("环境变量加载成功")


def init():
    logging.basicConfig(level=logging.INFO)
    logging.info("init application")
    checkEnvData()
    dingding("测试链接", "钉钉链接成功", webhook, secretKey)
    logging.info("start send test msg")
    return



def splitKeywordList():
    return keywords.split()

def splitCleanKeywords():
    return CleanKeywords.split()

def getKeywordNews(keyword):
    today_keyword_info_tmp=[]
    try:
        # 抓取本年的
        api = "https://api.github.com/search/repositories?q={}&sort=updated".format(keyword)
        json_str = requests.get(api, headers=github_headers, timeout=10).json()
        today_date = datetime.date.today()
        n=20 if len(json_str['items'])>20 else len(json_str['items'])
        for i in range(0, n):
            keyword_url = json_str['items'][i]['html_url']
            try:
                keyword_name = json_str['items'][i]['name']
                description=json_str['items'][i]['description']
                pushed_at_tmp = json_str['items'][i]['pushed_at']
                pushed_at = re.findall('\d{4}-\d{2}-\d{2}', pushed_at_tmp)[0]
                if pushed_at == str(today_date):
                    today_keyword_info_tmp.append({"keyword_name": keyword_name, "keyword_url": keyword_url, "pushed_at": pushed_at,"description":description})
                    logging.info("[+] keyword: {} ,{} ,{} ,{} ,{}".format(keyword, keyword_name,keyword_url,pushed_at,description))
                else:
                    logging.info("[-] keyword: {} ,{}的更新时间为{}, 不属于今天".format(keyword, keyword_name, pushed_at))
            except Exception as e:
                pass
    except Exception as e:
        logging.error(e, "github链接不通")
    return today_keyword_info_tmp

def dingding(text, msg,webhook,secretKey):
    ding = cb.DingtalkChatbot(webhook, secret=secretKey)
    ding.send_text(msg='{}\r\n{}'.format(text, msg), is_at_all=False)
    logging.info("发送消息 title:{} msg:{}".format(text,msg))

def sendmsg(pushdata):
    text=""
    for data in pushdata:
        text+="工具名称:{}\n工具网址:{}\n详情:{}\n\n\n ".format(data.get("keyword_name"),data.get("keyword_url"),data.get("description"))
    return

def flashCleanData():
    return


def yunp4n_main():
    init()
    keywords=splitKeywordList()
    cleanKeywords=set(splitCleanKeywords())
    pushdata=list()

    for keyword in keywords:
        templist=getKeywordNews(keyword)
        for tempdata in templist:
            if tempdata.get("keyword_name") in cleanKeywords:
                pass
            else:
                pushdata.append(tempdata)
                cleanKeywords.add(tempdata.get("keyword_name"))
    sendmsg(pushdata)
    flashCleanData()
    return

def test():
    # getKeywordNews("漏洞")
    init()

if __name__ == '__main__':
    test()
