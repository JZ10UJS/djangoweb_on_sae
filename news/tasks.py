from celery.decorators import task
from celery.utils.log import get_task_logger

from news.news_spider import main as spider_main

#from feedback.emails import send_feedback_email

logger = get_task_logger(__name__)

@task(name='crawl_news_task')
def crawl_news_task(website_name, info_nums):
    logger.info('Star crawling')
    return spider_main(website_name, info_nums)