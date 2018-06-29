#!/usr/bin/python3

"""
@file: begin.py
@brief: 
@author: feihu1996.cn
@date: 18-06-29
@version: 1.0
"""


from scrapy import cmdline


spider = 'jobbole_spider'
cmdline.execute(["scrapy", "crawl", spider])
