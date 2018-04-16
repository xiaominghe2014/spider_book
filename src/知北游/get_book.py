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
from lxml import etree

requests.packages.urllib3.disable_warnings()
url_base = 'https://www.88dus.com/xiaoshuo/1/1394/{}'
url_end = '/xiaoshuo/1/1394/'
book_name = "知北游"
pattern_title = r'<h1>(.*)</h1>'
pattern_content = r'<div class=\"yd_text2\">(.*)</div>'
pattern_next = r'var next_page = \"(.*)\"'
start = '446438.html'
char_set = 'gbk'
title_list = []

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
index = 1


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


def per_book_chat(url):
    resp = session.get(url, headers=headers, stream=True, verify=False)
    resp.encoding = char_set
    try:
        text = resp.text
        list_n = re.findall(pattern_next, text)
        next_page = list_n[0]
        list_t = re.findall(pattern_title, text)
        title = list_t[0]
        # list_c = re.findall(pattern_content, text)
        # txt = list_c[0]
        sel = etree.HTML(text)
        list_c = sel.xpath('//div[starts-with(@class,"yd_text2")]/text()')
        txt = ''.join(list_c)
        title_list.append(title)
        print(url, title)
        global index
        save_title = book_title.format(index)
        book = '{}/{}.md'.format(book_path, save_title)
        pre_tag = book_title.format(index-1)
        next_tag = book_title.format(index+1)
        if 1 == index:
            pre_tag = ''
        if next_page == url_end:
            next_tag = ''
        link = '\n{}&nbsp;&nbsp;&nbsp;&nbsp;{}&nbsp;&nbsp;&nbsp;&nbsp;{}\n'\
               .format(get_link('上一章', pre_tag), get_link('下一章', next_tag), get_link('返回目录', 'README'))
        txt = '{}<br />{}<br />{}<br />{}'.format(link, title, txt, link)
        write_txt(txt, book)
        index += 1
        if next_page == url_end:
            return
        per_book_chat(url_base.format(next_page))
    except Exception as e:
        print(e)


def add_md():
    with open(md_root, mode='a+', encoding='utf-8') as md:
        md.write('\n- [{}]({})'.format(book_name, url_book.format(book_name, 'README')))
    with open(md_book, mode='w+', encoding='utf-8') as md:
        txt = '# {}\n## 章节列表\n'.format(book_name)
        for unit in range(len(title_list)):
            title = book_title.format(unit + 1)
            url = url_book.format(book_name, title)
            txt = '\n{}- [{}]({})\n'.format(txt, title_list[unit], url)
        md.write(txt)


def main():
    check_dir()
    per_book_chat(url_base.format(start))
    add_md()


if __name__ == '__main__':
    main()

