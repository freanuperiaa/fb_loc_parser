from scrapy.crawler import CrawlerProcess, Crawler
from celery import shared_task

from .scraper import FriendsLocSpider


@shared_task
def scrape(email, password):
    crawler = Crawler(FriendsLocSpider, {
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
        'ROBOTSTXT_OBEY': False,
        'LOG_LEVEL': 'ERROR',
    })
    process = CrawlerProcess()

    process.crawl(crawler, email=email, password=password)
    process.start()
