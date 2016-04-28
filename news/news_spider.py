#!/usr/bin/python
# coding: utf-8

"""
主要是当启动项目时，自动抓取一些新闻，
并通过RESTful API写入到数据库中
"""

import requests
import threading
import json
from Queue import Queue
from BeautifulSoup import BeautifulSoup as BS

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    
}
urls = [
    'http://www.huxiu.com/whatsnew.html?f=nav_article_whatsnew',
]

# 调用RESTful API的用户名和密码
AUTH = ('root', 'zhangjie123')


class HomePageHander(object):
    def __init__(self, base_url, queue):
        self.url = base_url
        self.queue = queue

    def get_data(self):
        print 'start run'
        ss = requests.session()
        ss.headers.update(HEADERS)
        rsp = ss.get(self.url)
        rsp.encoding = rsp.apparent_encoding
        datas = []

        if rsp.ok:
            print'get home page success!'
            soup = BS(rsp.text)
            div_tags = soup.findAll('div', attrs={'class': 'mob-ctt'})
            map(self.queue.put, div_tags[:10])
            
            for i in range(5):
                a = DetailHander(self.queue, datas)
                a.setDaemon(True)
                a.start()
            
        self.queue.join()
        return datas


class DetailHander(threading.Thread):
    def __init__(self, tag_queue, datas):
        super(DetailHander, self).__init__()
        self.queue = tag_queue
        self.datas = datas

    def parse_detail_url(self, url):
        ss = requests.session()
        ss.headers.update(HEADERS)
        rsp = ss.get(url)
        rsp.encoding = rsp.apparent_encoding

        soup = BS(rsp.text)
        content_tag = soup.find('div', attrs={'id':'article_content'})
        p_tags = content_tag.findAll('p')
        res = [p_tag.text for p_tag in p_tags]
        return '\n\n'.join(res)
        
    def run(self):
        while not self.queue.empty():
            self.tag = self.queue.get()
            content_tag = self.tag.h3
            title = content_tag.text
            detail_url = content_tag.a.get('href')
            summary = self.tag.find('div', attrs={'class':'mob-sub'})
            print'get detail page %s by %s' % (detail_url, self.name)
            content = self.parse_detail_url('http://www.huxiu.com'+ detail_url)
            self.datas.append({'title': title, 
                          'summary': summary,
                          'content': content})
            self.queue.task_done()


def main():
    queue = Queue()
    t = HomePageHander(urls[0], queue)
    datas = t.get_data()
    print 'datas get success!'

    ss = requests.session()
    ss.auth = AUTH

    # 先判定是已经有categorys, 若没有就新建，主要是数据库初始化的时候。
    url = 'http://127.0.0.1:8000/api-info/categorys.json/'
    rsp = ss.get(url)
    category_datas = json.loads(rsp.text)

    if category_datas['count'] == 0:
        for category in ['Politics','Gossip','Novelty','Python','Django','HTML','CSS']:
            rsp == ss.post(url, data={'name':category})

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
    
        
