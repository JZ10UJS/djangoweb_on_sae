#!/usr/bin/python
# coding: utf-8

"""
主要是当启动项目是，自动抓取一些新闻，
并通过RESTful API写入到数据库中
"""

import requests
from BeautifulSoup import BeautifulSoup as BS

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    
}
urls = (
    'http://internet.baidu.com',
)

# 调用RESTful API的用户名和密码
AUTH = ('root', 'zhangjie123')


def parse_base_url(url):
    ss = requests.session()
    ss.headers.update(HEADERS)
    rsp = ss.get(url)
    rsp.encoding = rsp.apparent_encoding
    datas = []

    if rsp.ok:
        print'get home page success!'
        soup = BS(rsp.text)
        div_tags = soup.findAll('div', attrs={'class': 'mod-column'})
        for div_tag in div_tags:
            content_tag = div_tag.h2
            title = content_tag.text
            detail_url = content_tag.a.get('href')
            summary = div_tag.p.text
            print'get detail page %s' % detail_url
            content = parse_detail_url(detail_url)
            datas.append({'title': title, 
                          'summary': summary,
                          'content': content})

    return datas


def parse_detail_url(url):
    ss = requests.session()
    ss.headers.update(HEADERS)
    rsp = ss.get(url)
    rsp.encoding = rsp.apparent_encoding

    soup = BS(rsp.text)
    content_tag = soup.find('div', attrs={'class':'article-detail'})
    p_tags = content_tag.findAll('p', attrs={'class':'text'})
    res = [p_tag.text for p_tag in p_tags]
    return '\n\n'.join(res)



def main():
    datas = parse_base_url(urls[0])
    print 'datas get success!'

    ss = requests.session()
    ss.auth = AUTH
    url = 'http://127.0.0.1:8000/api-info/news.json/'

    for data in datas:
        # category现在就加载一个栏目里面，后期如果爬不同的网站信息，再改
        data['category'] = 'http://127.0.0.1:8000/api-info/categorys/3/'
        print 'send to my db..'
        rsp = ss.post(url, data=data)
        if rsp.ok:
            print 'success'
        else:
            print rsp.content



if __name__ == '__main__':
    main()