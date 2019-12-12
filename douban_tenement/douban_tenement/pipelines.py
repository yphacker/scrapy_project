# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
import re
import time


class DoubanTenementPipeline(object):
    def process_item(self, item, spider):
        return item


class FilePipeline(object):

    def process_item(self, item, spider):
        release_time = item['release_time']
        time_str = time.strptime(release_time, "%Y-%m-%d %H:%M:%S")
        time_str = time.strftime("%Y-%m-%d-%H", time_str)
        # fa_path = os.path.dirname(__file__)
        pattern = re.compile(r'[<>/\\\|:""\*\? \n]')
        file_name = re.sub(pattern, '_', item['subject'].strip()) + time_str + '.md'
        print(file_name)
        dir_path = '../data/'
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        abs_file_name = dir_path + file_name
        if not os.path.exists(abs_file_name):
            os.system(r'touch %s' % abs_file_name)
        f = open(abs_file_name, 'w')
        for image_url in item['image_urls']:
            f.write('![](%s)\n' % image_url)
        for line in item['content']:
            f.write("%s" % line)
        f.close()
        return item
