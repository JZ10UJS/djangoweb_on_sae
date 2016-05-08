#!/usr/bin/python
# coding: utf-8

"""
主要是当启动项目时，自动抓取一些新闻，
并通过RESTful API写入到数据库中
这多线程还没有从头到尾直接写来得快。。
耗时24s左右，所以要用celery redis 异步调用
"""

import time
import requests
import threading
from Queue import Queue
from BeautifulSoup import BeautifulSoup as BS

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    
}
URLS = {
    'HX':'http://www.huxiu.com/whatsnew.html?f=nav_article_whatsnew',
}

# 调用RESTful API的用户名和密码
AUTH = ('root', 'zhangjie123')


class HomePageHandler(object):
    def __init__(self, base_url, num=10):
        self.url = base_url
        # 用以存放详细页面的链接
        self.a_link_queue = Queue()
        # 抓取的篇数
        self.num = num
        # 用以存放发送到DB中的合格数据
        self.data_queue = Queue()

    def go(self):
        print 'running...'
        ss = requests.session()
        ss.headers.update(HEADERS)
        rsp = ss.get(self.url)
        rsp.encoding = rsp.apparent_encoding

        # 'http://www.huxiu.com'
        domain = self.url.rsplit('/', 1)[0]

        if rsp.ok:
            print'get home page success!'
            soup = BS(rsp.text)
            # 首页推荐文章div tag
            div_tags = soup.findAll('div', attrs={'class':'mob-ctt'}, limit=self.num)
            # 依次取出链接放入self.a_link_queue中
            map(self.a_link_queue.put, (domain + div.a.get('href') for div in div_tags))

            for i in range(10):
                a = DetailHandler(self.a_link_queue, self.data_queue)
                a.setDaemon(True)
                a.start()
                
            for i in range(3):
                b = PostHandler(self.data_queue)
                b.setDaemon(True)
                b.start()
            
            
            
        self.a_link_queue.join()
        self.data_queue.join()
        print 'DONE!'


class DetailHandler(threading.Thread):
    def __init__(self, a_link_queue, data_queue):
        super(DetailHandler, self).__init__()
        self.a_link_queue = a_link_queue
        self.data_queue = data_queue
        self.ss = requests.session()
        self.ss.headers.update(HEADERS)

    def parse_detail_url(self, url):
        """处理文章详情页，并将所需数据put到data_queue中，用以发送到db"""
        
        rsp = self.ss.get(url)
        rsp.encoding = rsp.apparent_encoding

        data = {}
        
        soup = BS(rsp.text)
        title_tag = soup.find('h1', attrs={'class':'t-h1'})
        data['title'] = title_tag.text
        content_tag = soup.find('div', attrs={'id':'article_content'})
        p_tags = content_tag.findAll('p')
        data['summary'] = p_tags[0].text
        res = (p_tag.text for p_tag in p_tags)
        data['content'] = '\n'.join(res)
        data['category'] = 'http://127.0.0.1:8000/api-info/categorys/3/'

        self.data_queue.put(data)
        
    def run(self):
        while not self.a_link_queue.empty():
            link = self.a_link_queue.get()
            print 'handling with `%s` by <%s>\n' % (link, self.name)
            self.parse_detail_url(link)
            
            self.a_link_queue.task_done()


class PostHandler(threading.Thread):
    """
    将queue中的数据通过RESTful API发送到DB中
    """
    def __init__(self, queue):
        super(PostHandler, self).__init__()
        self.post_data_queue = queue
        self.ss = requests.session()
        self.ss.auth = AUTH

    def run(self):
        # 这个地方不用 empty是因为初始化的时候，detailhander 没来得及
        # 将data放入data_queue中，导致其为空。线程直接就结束了.
        # data_queue.join()却无法完成。
        while True:
            data = self.post_data_queue.get()            
            url = 'http://127.0.0.1:8000/api-info/news.json/'
            print 'send to my db..'
            rsp = self.ss.post(url, data=data)
            if rsp.ok:
                print 'success'
            else:
                print rsp.content
            self.post_data_queue.task_done()
            
    


def main(website_name, info_num=10):
    a = HomePageHandler(URLS[website_name], info_num)
    a.go()


if __name__ == '__main__':
    s = time.time()
    main('HX')
    e = time.time()
    print 'using ', e-s
    
        
