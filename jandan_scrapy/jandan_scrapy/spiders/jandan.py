# coding=utf-8
# author=yphacker

import scrapy

from jandan_scrapy.utils import tools
from jandan_scrapy.items import JandanScrapyItem


class DouBanSpider(scrapy.Spider):
    name = "jandan"
    allowed_domains = ["jandan.net"]
    # 这个start_urls貌似并没有起作用
    start_urls = (
        'http://jandan.net/ooxx',
    )

    def start_requests(self):
        reqs = []
        reqs.append(scrapy.Request('http://jandan.net/ooxx/MjAxOTEyMTItMT{}#comments'.format('TQ')))
        # num_choose = list(map(chr, range(ord('a'), ord('z') + 1))) + list(map(chr, range(ord('A'), ord('Z') + 1)))
        # for i in num_choose:
        #     for j in num_choose:
        #         num = i + j
        #         req = scrapy.Request('http://jandan.net/ooxx/MjAxOTEyMTItMT{}#comments'.format(num))
        #         reqs.append(req)
        return reqs

    def parse(self, response):
        comment_list = response.xpath("//*[@class='commentlist']/li")
        items = []
        for comment in comment_list:
            item = JandanScrapyItem()
            item['author'] = comment.xpath(".//div[@class='author']/strong/text()").extract()
            # 可能出现为空的情况
            if len(item['author']) <= 0:
                continue
            item['author'] = item['author'][0]
            item['image_urls'] = []
            img_urls = comment.xpath('.//div[@class="text"]//p/img/@src').extract()
            for img_url in img_urls:
                # 切换大图
                # img_url = img_url.replace('mw600', 'large')
                item['image_urls'].append('http:' + img_url)
            items.append(item)
        return items
