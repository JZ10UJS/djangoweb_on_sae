#!/usr/bin/python
# coding:utf-8

"""
主要是当启动项目时，自动抓取一些新闻，
并通过RESTful API写入到数据库中
这个耗时5s内，但是tornado的Future obj不能被celery序列化，
就没采用
"""

import time, base64
from datetime import timedelta

from BeautifulSoup import BeautifulSoup as BS
from tornado import httpclient, gen, ioloop, queues

# 主要用于django的HTTP Basic Auth 登录
AUTH = ('root','zhangjie123')
b64s = base64.encodestring('%s:%s' % AUTH)[:-1]
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Authorization': 'Basic %s' % b64s,
    'Accept-Encoding':'gzip, deflate',
    'Accept': '*/*',
    'Connection':'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded',
}

URLS = {
    'HX':'http://www.huxiu.com/whatsnew.html?f=nav_article_whatsnew',
}


concurrency = 10


@gen.coroutine
def get_article_links(url, info_num):
    """用以获取虎嗅首页推荐文章的超链接"""
    s = time.time()
    try:
        response = yield httpclient.AsyncHTTPClient().fetch(url)
        print('fetched %s' % url)

        html = response.body if isinstance(response.body, str) \
            else response.body.decode()
        soup = BS(html)
        domain = 'http://www.huxiu.com'
        div_tags = soup.findAll('div', attrs={'class':'mob-ctt'}, limit=info_num)
        urls = [domain + div.a.get('href') for div in div_tags]
    except Exception as e:
        print('Exception: %s %s' % (e, url))
        raise gen.Return([])
    print 'handle base url using time: %.3f seconds' % (time.time()-s)
    raise gen.Return(urls)


@gen.coroutine
def main(website_name, info_num=10):
    q = queues.Queue()
    start = time.time()

    @gen.coroutine
    def handle_url():
        detail_url = yield q.get()
        try:
            response = yield httpclient.AsyncHTTPClient().fetch(detail_url)
            print 'handling detial url %s' % (detail_url,)
            html = response.body

            # 用以直接在http body中传参数, title=u'xxxx'&summary=u'82828之类的
            # 如果data中含有unicode， urlencode(data)会爆decode error
            # 所以直接自己构造
            data = []
            soup = BS(html)
            title_tag = soup.find('h1', attrs={'class':'t-h1'})
            data.extend(['title=', title_tag.text])
            content_tag = soup.find('div', attrs={'id':'article_content'})
            p_tags = content_tag.findAll('p')
            data.extend(['&summary=', p_tags[0].text])
            res = (p_tag.text for p_tag in p_tags)
            data.extend(['&content=', '\n'.join(res)])
            data.extend(['&category=', 'http://127.0.0.1:8000/api-info/categorys/3/'])
    

            post_url = 'http://localhost:8000/api-info/news.json'
            body = ''.join(data)
            rsp = yield httpclient.AsyncHTTPClient().fetch(
                post_url,
                method='POST',
                body=body,
                headers=HEADERS
                )
        except Exception as e:
            raise e
        else:
            print 'send to mydb success!'
        finally:
            q.task_done()

    @gen.coroutine
    def worker():
        while True:
            yield handle_url()

    detail_urls = yield get_article_links(URLS[website_name], info_num)
    map(q.put, detail_urls)

    for _ in range(concurrency):
        worker()

    yield q.join(timeout=timedelta(seconds=300))
    
    print 'Done in %.3f seconds' % (time.time() - start,)
    
if __name__ == '__main__':
    io_loop = ioloop.IOLoop.current()
    io_loop.run_sync(lambda:main('HX'))
    #io_loop.run_sync(post_test)
