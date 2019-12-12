# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
import re
import requests
from jandan_scrapy import settings


class JandanScrapyPipeline(object):
    def process_item(self, item, spider):
        return item


class ImageDownloadPipeline(object):
    def process_item(self, item, spider):
        if 'image_urls' in item.keys():
            dir_path = '%s/%s' % (settings.IMAGES_STORE, item['author'])
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
            for image_url in item['image_urls']:
                is_gif = re.match(r'.*\.sinaimg\.cn\/\w+\/(.*?\.(jpg|gif))', image_url)
                if not is_gif:
                    continue
                image_file_name = is_gif.group(1)
                file_path = '%s/%s' % (dir_path, image_file_name)
                if os.path.exists(file_path):
                    continue
                # 此处下载图片没用代理，后续把这个位置补上
                with open(file_path, 'wb') as handle:
                    response = requests.get('http://' + image_url, stream=True)
                    for block in response.iter_content(1024):
                        if not block:
                            break
                        handle.write(block)
        return item
