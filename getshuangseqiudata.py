"""
专家杀号：https://zx.500.com/ssq/zhuanjiashahao.php
彩票数据：https://datachart.500.com/ssq/
媒体预测：https://zx.500.com/ssq/mediayc.php
"""
import requests
import bs4
import xlwt
import sys
import re
import os

class shuangseqiu():
    '''
    双色球类
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
        current_issue = html.find_all('tr', id="ssq")[0].find("td", align="center")
        i, j = re.search("\d{5}", current_issue.string).span()
        print("当前双色球最新期数是->", current_issue.string[i:j])
        return current_issue.string[i:j]

    def crawlingData(self, end_period = None, start_period = None):
        '''
        :param end_period: 截止获取数据的期次
        :param start_period: 开始获取数据的期次,从03年开始出售第一期双色球,默认从第一期开始爬取数据
        :return: 服务器响应，包含我们想要的数据，需要去解析
        '''
        url = 'http://datachart.500.com/ssq/history/newinc/history.php?start=%s&end=%s&sort=1' \
              % ( start_period, end_period)  # 可以提取到期号、中奖号码、奖金、开奖日期等信息
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0'
        }
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
        except Exception:
            print("爬取失败!")
            sys.exit()
        else:
            return response.text

    def extractData(self, response_text):
        '''
        :param response_text: 爬取到的网页文本内容
        :return: 提取到的彩票数据
        '''
        html = bs4.BeautifulSoup(response_text, 'lxml')
        cai_piao_info = html.find_all('tr', class_='t_tr1')
        current_row_index = 0
        all_data = {}
        all_cai_piao_info = []
        for index_cai_piao, one_cai_piao in enumerate(cai_piao_info):
            one_cai_piao = one_cai_piao.find_all('td')
            one_cai_piao = [i.text for index, i in enumerate(one_cai_piao) if index != 8]
            all_cai_piao_info.append([int(i) for i in one_cai_piao[1:8]])
            all_data[index_cai_piao] = one_cai_piao
            current_row_index += 1
        print("一共爬取到%d期彩票数据" % (current_row_index))
        return all_cai_piao_info, all_data

    def saveData(self, all_data, file_save_name, current_row_index = 0, worksheet = None):
        '''
        :param all_data: 爬取到的所有彩票数据
        :param file_save_name: 要保存的文件路径，xls文件
        :param current_row_index: 当前保存到多少行了
        :param worksheet:
        :return:
        '''
        workbook = None
        if not worksheet:
            # 创建一个workbook 设置编码
            workbook = xlwt.Workbook(encoding='utf-8')
            # 创建一个worksheet
            worksheet = workbook.add_sheet("双色球")
        if current_row_index == 0:
            # 将列标题写入excel
            current_row_index = 0
            for i, str_col in enumerate(
                    ['期号', '红球', '红球', '红球', '红球', '红球', '红球', '篮球', '奖池奖金', '一等奖注数', '奖金', '二等奖注数', '奖金', '总投注额', '开奖日期']):
                worksheet.write(current_row_index, i, str_col)  # 参数对应 行, 列, 值
            current_row_index += 1

        for _, one_cai_piao in all_data.items():
            for index, i in enumerate(one_cai_piao):
                worksheet.write(current_row_index, index, i)
            current_row_index += 1
        # 保存
        workbook.save('./data/%s.xls' % (file_save_name))

    def getAllData(self, file_save_name):
        #如果之前爬取过数据，则更新数据，否则开始爬取所有数据
        if os.path.exists(file_save_name) and os.path.isfile(file_save_name):
            pass
        else:
            response_text = self.crawlingData()
            all_cai_piao_info, all_data = self.extractData(response_text)
            self.saveData(all_data, "双色球数据")

if __name__ == "__main__":
    import json
    import numpy as np

    start_period = '03001'#从03年开始出售第一期双色球
    end_period = '20128'#要爬取的最后一期双色球
    all_cai_piao_info, all_data = shuangseqiu().extractData(end_period, start_period)

    all_cai_piao_info = np.array(all_cai_piao_info)
    np.save("./data/shuangseqiu", all_cai_piao_info)

    with open("./data/shuangseqiu.json", "w+") as f:
        json.dump(all_data, f)

