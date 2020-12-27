"""
专家杀号：https://zx.500.com/dlt/zhuanjiashahao.php
彩票数据：https://datachart.500.com/dlt/
没有媒体预测页面
"""
import requests
import bs4
import xlwt
import sys
import re

class daletou():
    '''
    大乐透类
    获取双色球的各种数据，并进行简单的处理
    '''
    _start_period = "03001" #从03年开始出售第一期双色球

    def __init__(self):
        self.current_issue = self.getCurrentPeriod()

    def getCurrentPeriod(self):
        '''
        :return: 获取双色球最新期次,数据来自"https://kaijiang.500.com/"
        '''
        url = "https://kaijiang.500.com/"
        html = requests.get(url)
        html = bs4.BeautifulSoup(html.text, 'lxml')
        current_issue = html.find_all('tr', id="dlt")[0].find("td", align="center")
        i, j = re.search("\d{5}", current_issue.string).span()
        #print("当前双色球最新期数是->", current_issue.string[i:j])
        return current_issue.string[i:j]

if __name__ == "__main__":
    caipiao = daletou()
    print("当前双色球最新期数是->",caipiao.current_issue)