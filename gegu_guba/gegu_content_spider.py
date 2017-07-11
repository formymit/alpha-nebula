#!usr/bin/env python3.6  
#-*- coding:utf-8 -*-  
""" 
@author:iBoy 
@file: gubaSpider.py
@time: 2017/07/03
"""
import requests
from lxml import etree
import time
from mongodb_queue import MongoQueue
import multiprocessing
import traceback


headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:53.0) Gecko/20100101 Firefox/53.0',
}


def get_sumpage(url):
    try:
        response = requests.get(url, headers=headers)
        response.encoding = 'utf-8'

        selector = etree.HTML(response.text)

        # sumpage = selector.xpath('//span[@class="sumpage"]//text()')# js加载 此方案不可行
        sumpage_tmp = selector.xpath('//span[@class="pagernums"]/@data-pager')[0]
        sum_num = sumpage_tmp.split('|')[1]
        each_page_num = sumpage_tmp.split('|')[2]
        sumpage = int(int(sum_num)/int(each_page_num))

    except Exception as e:
        print(e)
        traceback.print_exc()
    return sumpage

# def getdata(url):
#     try:
#         response = requests.get(url, headers=headers)
#         response.encoding = 'utf-8'
#
#         selector = etree.HTML(response.text)
#
#         all_title_hrefs = selector.xpath('//div[@id="mainbody"]//span[@class="l3"]/a/@href')
#
#         for each in all_title_hrefs:
#             if each[:4] != 'http' and each[0] != '/':
#                 each = 'http://guba.eastmoney.com/' + each
#                 print(each)
#             elif each[:4] != 'http':
#                 each = 'http://guba.eastmoney.com' + each
#                 print(each)
#
#     except Exception as e:
#         print(e)
#         traceback.print_exc()
#     return response.status_code


if __name__ == '__main__':

    # url = 'http://guba.eastmoney.com/list,300104.html'
    print('start...')
    with open('gegu_list.txt') as f:
        tmp = f.readline()[:-1]
        while tmp:
            try:
                title = tmp.split('\t')[0]
                url = tmp.split('\t')[1]
                print(title)
                print(url)

                sumpage = get_sumpage(url)
                print(sumpage)
            except Exception as e:
                print(e)
            tmp = f.readline()[:-1]


                # for i in range(1, sumpage + 1):
    #     newurl = url[:-5] + '_' + str(i) + '.html'
    #     print('爬取页面：'+newurl)
    #     getdata(newurl)

