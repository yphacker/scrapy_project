# coding=utf-8
# author=yphacker

import scrapy
from douban_tenement.items import DoubanTenementItem


class DouBanSpider(scrapy.Spider):
    name = "douban"
    allowed_domains = ["douban.com"]
    # 苏州街
    start_urls = (
        'https://www.douban.com/group/search?cat=1013&group=35417&sort=time&q=%E8%8B%8F%E5%B7%9E%E8%A1%97',
    )

    rules = (
        # Rule(LinkExtractor(allow=('*',)), callback='parse_content'),
    )

    def parse(self, response):
        reqs = []
        for url in self.start_urls:
            req = scrapy.Request(url, callback=self.parse_list)
            reqs.append(req)
        i = 0
        # 此url_list拿不到首页
        url_list = response.xpath('//*[@id="content"]/div/div[1]/div[3]//@href').extract()
        for url in url_list:
            i += 1
            if i >= 2:
                break
            req = scrapy.Request(url, callback=self.parse_list)
            reqs.append(req)
        return reqs

    def parse_list(self, response):
        url_list = response.xpath('//*[@id="content"]/div/div[1]/div[2]/table/tbody//@href').extract()
        for url in url_list:
            yield scrapy.Request(str(url), callback=self.parse_content)

    def parse_content(self, response):
        item = DoubanTenementItem()
        item['subject'] = response.xpath('//*[@id="content"]/h1/text()').extract()[0]
        item['release_time'] = \
        response.xpath('//*[@id="content"]/div/div[1]/div[1]/div[2]/h3/span[2]/text()').extract()[0]
        item['content'] = response.xpath("//*[@id='link-report']/div[@class='topic-content']//text()").extract()
        image_urls = response.xpath(
            "//*[@id='link-report']/div[@class='topic-content']//div[@class='image-container image-float-center']//img/@src").extract()
        item['image_urls'] = image_urls
        return item
