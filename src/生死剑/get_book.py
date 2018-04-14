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
@time: 2018/4/14 下午7:10

"""
import os
import re
import requests
import gzip

# requests.packages.urllib3.disable_warnings()

url_base = 'http://www.zhonghuawuxia.com/chapter/{}'
book_name = "生死剑"
pattern = r'.*</div>(.*)<br><br>.*'
start = 55230
total = 24


headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/63.0.3239.84 Safari/537.36'}
book_title = "第{}章"
url_book = 'https://github.com/xiaominghe2014/spider_book/blob/master/book/{}/{}.md'
git_root = 'https://github.com/xiaominghe2014/spider_book/blob/master'
git_book = 'https://github.com/xiaominghe2014/spider_book/blob/master/book/{}'.format(book_name)
current_dir = os.path.dirname(os.path.realpath(__file__))
book_path = '{}/../../book/{}/'.format(current_dir, book_name)
md_root = '{}/../../README.md'.format(current_dir)
md_book = '{}/../../book/{}/README.md'.format(current_dir, book_name)
session = requests.session()


def check_dir():
    if not os.path.exists(book_path):
        os.makedirs(book_path)


def write_txt(txt, file):
    with open(file, mode='w+', encoding='utf-8') as f:
        f.write(txt)


def get_link(txt, url):
    if '' == url:
        return ''
    url = url_book.format(book_name, url)
    return '[{}]({})'.format(txt, url)


def per_book_chat(url, save_title, pre_tag, next_tag):
    print(url, save_title)
    resp = session.get(url, headers=headers, stream=True, verify=False)
    try:
        text = resp.text
        g = re.match(pattern, text, re.S | re.X)
        txt = g.group(1)
        book = '{}/{}.md'.format(book_path, save_title)
        link = '\n{}&nbsp;&nbsp;&nbsp;&nbsp;{}&nbsp;&nbsp;&nbsp;&nbsp;{}\n'\
               .format(get_link('上一章', pre_tag), get_link('下一章', next_tag), get_link('返回目录', 'README'))
        txt = '{}{}{}'.format(link, txt, link)
        write_txt(txt, book)
    except Exception as e:
        print(e)


def add_md():
    with open(md_root, mode='a+', encoding='utf-8') as md:
        md.write('\n- [{}]({})'.format(book_name, url_book.format(book_name, 'README')))
    with open(md_book, mode='a+', encoding='utf-8') as md:
        txt = '# {}\n## 章节列表\n'.format(book_name)
        for unit in range(total):
            title = book_title.format(unit + 1)
            url = url_book.format(book_name, title)
            txt = '\n{}- [{}]({})\n'.format(txt, title, url)
        md.write(txt)


def main():
    check_dir()
    for unit in range(total):
        url = url_base.format(unit+start)
        title = book_title.format(unit+1)
        pre_tag = ''
        next_tag = ''
        if unit > 0:
            pre_tag = book_title.format(unit)
        if unit < total-1:
            next_tag = book_title.format(unit+2)
        per_book_chat(url, title, pre_tag, next_tag)
    add_md()


if __name__ == '__main__':
    main()

