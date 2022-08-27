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
secretKey= os.environ.get("secretKey")
keywords=os.environ.get("keywords")
CleanKeywords=os.environ.get("CleanKeywords")

github_headers = {
    'Authorization': "token {}".format(github_token)
}

def init():
    logging.info("init application")
    dingding("test", "测试链接", webhook, secretKey)
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
                    print("[+] keyword: {} ,{} ,{} ,{} ,{}".format(keyword, keyword_name,keyword_url,pushed_at,description))
                else:
                    print("[-] keyword: {} ,{}的更新时间为{}, 不属于今天".format(keyword, keyword_name, pushed_at))
            except Exception as e:
                pass
    except Exception as e:
        logging.error(e, "github链接不通")
    return today_keyword_info_tmp

def dingding(text, msg,webhook,secretKey):
    ding = cb.DingtalkChatbot(webhook, secret=secretKey)
    ding.send_text(msg='{}\r\n{}'.format(text, msg), is_at_all=False)

def sendmsg():
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
    sendmsg()
    flashCleanData()
    return

def test():
    getKeywordNews("漏洞")


if __name__ == '__main__':
    test()
