# -*- coding: utf-8 -*-


import scrapy
from proxy.items import ProxyItem
from proxy.check_url import check_baidu


class XiciSpider(scrapy.Spider):
    name = "xici"
    allowed_domains = ["xicidaili.com"]
    start_urls = (
        'http://www.xicidaili.com',
    )

    def start_requests(self):
        reqs = []
        for i in range(1, 3):
            req = scrapy.Request("http://www.xicidaili.com/nn/%s" % i)
            reqs.append(req)
        return reqs

    def parse(self, response):
        ip_list = response.xpath("//table[@id='ip_list']")
        trs = ip_list[0].xpath('tr')
        items = []
        for ip in trs[2:]:
            item = ProxyItem()
            item['ip'] = ip.xpath('td[2]/text()')[0].extract()
            item['port'] = ip.xpath('td[3]/text()')[0].extract()
            item['position'] = ip.xpath('string(td[4])')[0].extract().strip()
            item['type'] = ip.xpath('td[6]/text()')[0].extract()
            item['speed'] = ip.xpath('td[7]/div[@class="bar"]/@title')[0].re('\d{0,2}\.\d{0,}')
            item['life'] = ip.xpath('td[9]/text()')[0].extract()
            item['last_check_time'] = ip.xpath('td[10]/text()')[0].extract()
            print (item)
            if check_baidu(item):
                items.append(item)
        return items
