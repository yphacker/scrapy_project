# coding=utf-8
# author=yphacker

import requests
from requests.adapters import HTTPAdapter

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
}


def check_baidu(item):
    session = requests.session()
    session.mount('http://', HTTPAdapter(max_retries=3))
    url = 'https://www.baidu.com/'
    proxy = {
        str(item['type']).lower(): str(item['ip']) + ':' + str(item['port'])
    }
    info = session.get(url, headers=headers, proxies=proxy, timeout=3)
    if info.status_code == 200:
        return True
    return False
