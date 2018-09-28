#coding=utf-8
import scrapy
from scrapy.http import Request
from biliob_spider.items import VideoOnline
import time
import json
import logging
from pymongo import MongoClient
import datetime

class OnlineSpider(scrapy.spiders.Spider):
    name = "online"
    allowed_domains = ["bilibili.com"]
    start_urls = ['https://www.bilibili.com/video/online.html']
    custom_settings = {
        'ITEM_PIPELINES': {
            'biliob_spider.pipelines.OnlinePipeline': 300
        }
    }

    def parse(self, response):
        try:
            video_list = response.xpath('//*[@id="app"]/div[2]/div[2]/div')

            # 为了爬取分区、粉丝数等数据，需要进入每一个视频的详情页面进行抓取
            title_list = video_list.xpath('./a/p/text()').extract()
            watch_list = video_list.xpath('./p/b/text()').extract()
            author_list = video_list.xpath('./div[1]/a/text()').extract()
            for i in range(len(title_list)):
                item = VideoOnline()
                item['title'] = title_list[i]
                item['author'] = author_list[i]
                item['data'] = [{'datetime':datetime.datetime.now(),'number':watch_list[i]}]
                yield item

        except Exception as error:
            # 出现错误时打印错误日志
            logging.error("视频爬虫在解析时发生错误")
            logging.error(response.url)
            logging.error(error)