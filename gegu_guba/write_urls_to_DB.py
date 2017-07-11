#!usr/bin/env python3.6  
#-*- coding:utf-8 -*-  
""" 
@author:iBoy 
@file: write_urls_to_DB.py 
@time: 2017/07/05 
"""
import requests
import traceback
from lxml import etree
from mongodb_queue import MongoQueue

spider_queue = MongoQueue('guba', 'gegu_all_urls')

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

            for i in range(1, sumpage+1):
                newurl = url[:-5] + '_' + str(i) + '.html'
                spider_queue.guba_push(newurl, title)

        except Exception as e:
            print(e)
        tmp = f.readline()[:-1]