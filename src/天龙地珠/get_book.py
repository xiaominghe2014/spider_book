#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
@version: ??
@author: xiaoming
@license: MIT Licence 
@contact: xiaominghe2014@gmail.com
@site: 
@software: PyCharm
@file: get_book.py
@time: 2018/4/13 下午4:08

"""
import os
import re
import requests

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/63.0.3239.84 Safari/537.36'}
book_title = "天龙地珠(十二神拳)-第{}章"
url_base = "http://www.zhonghuawuxia.com/chapter/{}"
tag = "pre"
start = 65853
total = 10
current_dir = os.path.dirname(os.path.realpath(__file__))
book_path = '{}/../../book/天龙地珠/'.format(current_dir)
session = requests.session()


def check_dir():
    if not os.path.exists(book_path):
        os.makedirs(book_path)


def write_txt(txt, file):
    with open(file, mode='w+', encoding='utf-8') as f:
        f.write(txt)


def per_book_chat(url, save_title, txt_tag):
    print(url, save_title, txt_tag)
    resp = session.get(url, headers=headers, stream=True, verify=False)
    try:
        text = resp.text
        pattern = r'.*(<{0}>.*</{0}>).*'.format(tag)
        txt = re.match(pattern, text, re.S | re.X).group(1)
        book = '{}/{}.md'.format(book_path, save_title)
        write_txt(txt, book)
    except Exception as e:
        print(e)


def main():
    check_dir()
    for unit in range(total):
        url = url_base.format(unit+start)
        title = book_title.format(unit+1)
        per_book_chat(url, title, tag)


if __name__ == '__main__':
    main()

