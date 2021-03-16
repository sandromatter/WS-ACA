# ---------------------------------------------------------------------------------------
#
# pinkbike.py
# 
# ---------------------------------------------------------------------------------------
# Import packages
# ---------------------------------------------------------------------------------------

import scrapy
from scrapy import loader
from ..items import PinkbikeScraperItem
from scrapy.loader import ItemLoader

# ---------------------------------------------------------------------------------------
# Variables
# ---------------------------------------------------------------------------------------



# ---------------------------------------------------------------------------------------
# Program
# ---------------------------------------------------------------------------------------

class PinkbikeSpider(scrapy.Spider):
    name = 'pinkbike'
    allowed_domains = ['pinkbike.com']
    # url_parameter_month = 2
    # url_parameter_year = 2020
    # start_urls = ['https://www.pinkbike.com/news/archive/?catid=0&year=2020&month=%s' % page for page in range(1,12)]
    start_urls = ['https://www.pinkbike.com/news/archive/?catid=0&year=2020&month=1']


    def parse(self, response):

        self.logger.info('Parse function called on {}'.format(response.url))
        articles = response.xpath('//*[@class="news-box2"]')
        for article in articles:
            loader = ItemLoader(item = PinkbikeScraperItem(), selector = article)
            
            loader.add_xpath('article_title', './/a[@class="f22 fgrey4 bold"]')
            loader.add_xpath('article_url', './/*[@class="f22 fgrey4 bold"]/@href')
            loader.add_xpath('article_author', './/a[@class="fblack"]')
            loader.add_xpath('article_tags', './/div[@class="floatleft"]/div/a')

            article_item = loader.load_item()
            article_detail_url = article.xpath('.//*[@class="f22 fgrey4 bold"]/@href').get()
            yield response.follow(url=str(article_detail_url), callback=self.parse_article, meta={'article_item': article_item})

        # next_page = 'https://www.pinkbike.com/news/archive/?catid=0&year=2020&month=1'

    def parse_article(self, response):
        article_item = response.meta['article_item']
        loader = ItemLoader(item = article_item, response = response)

        loader.add_xpath('article_meta_title', '/html/head/title')
        loader.add_xpath('article_meta_keywords', '//meta[@name="keywords"]/@content')
        loader.add_xpath('article_meta_description', '//meta[@name="description"]/@content')
        loader.add_xpath('article_published_time', '//meta[@property="article:published_time"]/@content')
        loader.add_xpath('article_number_of_comments', '//*[@id="commenttop"]')
        loader.add_xpath('article_comment_username', '//*[contains(@class, "cmcont")]/div[1]/a[1]')
        loader.add_xpath('article_comment_date', '//*[contains(@class, "cmcont")]/div[1]/a[@class="time"]')
        loader.add_xpath('article_comment_upvotes', '//span[@class="pcu "]')
        loader.add_xpath('article_comment_downvotes', '//span[@class="pcd "]')
        loader.add_xpath('article_comment_content', '//*[contains(@class, "cmcont")]/div[@class="comtext"]')
        # loader.add_xpath('article_comment_flag_number', '//*[contains(@class, "cmcont")]/div[1]/a[2]')
        yield loader.load_item()
