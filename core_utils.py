import errno
import json
import logging
import os
import re
from time import sleep

import requests
from bs4 import BeautifulSoup
import random

from banned_exception import BannedException

OUTPUT_DIR = 'comments'


def get_reviews_filename(product_id):
    filename = os.path.join(OUTPUT_DIR, '{}.json'.format(product_id))
    exist = os.path.isfile(filename)
    return filename, exist


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def persist_comment_to_disk(reviews):
    if len(reviews) == 0:
        return False
    product_id_set = set([r['product_id'] for r in reviews])
    assert len(product_id_set) == 1, 'all product ids should be the same in the reviews list.'
    product_id = next(iter(product_id_set))
    output_filename, exist = get_reviews_filename(product_id)
    if exist:
        return False
    mkdir_p(OUTPUT_DIR)
    with open(output_filename, 'w') as fp:
        json.dump(reviews, fp, sort_keys=True, indent=4, ensure_ascii=False)
    return True


def extract_product_id(link_from_main_page):
    # e.g. B01H8A7Q42
    p_id = -1
    tags = ['/dp/', '/gp/product/']
    for tag in tags:
        try:
            p_id = link_from_main_page[link_from_main_page.index(tag) + len(tag):].split('/')[0]
        except:
            pass
    m = re.match('[A-Z0-9]{10}', p_id)
    if m:
        return m.group()
    else:
        return None


def get_soup(url):
    if 'amazon.com' not in url:
        url = 'https://www.amazon.com' + url
    nap_time_sec = 0.05
    logging.debug('Script is going to sleep for {} (Amazon throttling). ZZZzzzZZZzz.'.format(nap_time_sec))
    sleep(nap_time_sec)
    header = randHeader()

    # header = {
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36'
    # }
    logging.debug('-> to Amazon : {}'.format(url))
    out = requests.get(url, headers=header)
    assert out.status_code == 200
    soup = BeautifulSoup(out.content, 'html.parser')
    if 'captcha' in str(soup):
        print('Your bot has been detected. Please wait a while.')
        #raise BannedException('Your bot has been detected. Please wait a while.')
    return soup


def randHeader():
    head_connection = ['Keep-Alive', 'close']
    head_accept = ['text/html, application/xhtml+xml, */*']
    head_accept_language = ['zh-CN,fr-FR;q=0.5', 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3']
    head_user_agent = ['Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
                       'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.95 Safari/537.36',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; rv:11.0) like Gecko)',
                       'Mozilla/5.0 (Windows; U; Windows NT 5.2) Gecko/2008070208 Firefox/3.0.1',
                       'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070309 Firefox/2.0.0.3',
                       'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070803 Firefox/1.5.0.12',
                       'Opera/9.27 (Windows NT 5.2; U; zh-cn)',
                       'Mozilla/5.0 (Macintosh; PPC Mac OS X; U; en) Opera 8.0',
                       'Opera/8.0 (Macintosh; PPC Mac OS X; U; en)',
                       'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.12) Gecko/20080219 Firefox/2.0.0.12 Navigator/9.0.0.6',
                       'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Win64; x64; Trident/4.0)',
                       'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0)',
                       'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; .NET4.0C; .NET4.0E)',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Maxthon/4.0.6.2000 Chrome/26.0.1410.43 Safari/537.1 ',
                       'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; .NET4.0C; .NET4.0E; QQBrowser/7.3.9825.400)',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0 ',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.92 Safari/537.1 LBBROWSER',
                       'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; BIDUBrowser 2.x)',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/3.0 Safari/536.11']

    header = {
        'Connection': head_connection[0],
        'Accept': head_accept[0],
        'Accept-Language': head_accept_language[1],
        'User-Agent': head_user_agent[random.randrange(0, len(head_user_agent))]
    }
    return header
