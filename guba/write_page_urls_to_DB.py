#!usr/bin/env python3.6  
#-*- coding:utf-8 -*-  
""" 
@author:iBoy 
@file: write_page_urls_to_DB.py 
@time: 2017/07/03 
"""
from mongodb_queue import MongoQueue

spider_queue = MongoQueue('guba', 'page_urls')


for i in range(1, 743416):
    url = 'http://guba.eastmoney.com/default_' + str(i) + '.html'
    spider_queue.push(url)

