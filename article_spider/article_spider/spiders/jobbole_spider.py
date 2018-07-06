# -*- coding: utf-8 -*-
import re

import scrapy


class JobboleSpiderSpider(scrapy.Spider):
    name = 'jobbole_spider'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://web.jobbole.com/94889/']

    def parse(self, response):
        # 文章标题
        title = ''.join(response.xpath("//div[@class='entry-header']/h1/text()").extract())
        title = re.sub('\s', '', title)
        print('title:' + title)

        # 发表时间
        createTime = ''.join(response.xpath('//p[@class="entry-meta-hide-on-mobile"]/text()').extract())
        createTime = re.sub('\s|\·', '', createTime)
        print('create_time:' + createTime)

        # 点赞数
        praiseNums = ''.join(response.xpath('//span[@class=" btn-bluet-bigger href-style vote-post-up   register-user-only "]/h10/text()').extract())
        praiseNums = re.sub('\s', '', praiseNums)
        if praiseNums:
            praiseNums = int(praiseNums)
        else:
            praiseNums = 0
        print('praiseNums:' + str(praiseNums))

        # 收藏数
        favNums = ''.join(response.xpath('//span[@class=" btn-bluet-bigger href-style bookmark-btn  register-user-only "]/text()').extract())
        favNums = re.sub('\s|(收藏)', '', favNums)
        if favNums:
            favNums = int(favNums)
        else:
            favNums = 0
        print('favNums:' + str(favNums))

        # 评论数
        commentNums = ''.join(response.xpath('//span[@class="btn-bluet-bigger href-style hide-on-480"]/text()').extract())
        commentNums = re.sub('\s|评论', '', commentNums)
        if commentNums:
            commentNums = int(commentNums)
        else:
            commentNums = 0
        print('commentNums:' + str(commentNums))

        # 文章标签
        tag = response.xpath('//p[@class="entry-meta-hide-on-mobile"]/a/text()').extract()
        tag = ','.join(tag) if len(tag) > 1 else ''.join(tag)
        tag = re.sub('\s', '', tag)
        print('tag:' + tag)

        # 文章内容
        content = ''.join(response.xpath('//div[@class="entry"]').extract())
        content = re.sub('\s', '', content)
        print('content:' + content)
        
