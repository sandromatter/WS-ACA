# ---------------------------------------------------------------------------------------
#
# pinkbike_spider.py
# 
# ---------------------------------------------------------------------------------------
# Import packages
# ---------------------------------------------------------------------------------------

import scrapy
from ..items import PinkbikeScraperItem
from scrapy.loader import ItemLoader
import logging
from scrapy.utils.log import configure_logging 

# ---------------------------------------------------------------------------------------
# Program
# ---------------------------------------------------------------------------------------

class PinkbikeSpider(scrapy.Spider):
    name = 'pinkbike'
    allowed_domains = ['pinkbike.com']
    url_parameter_year = 2000
    url_parameter_month = 1
    start_urls = [
        'https://www.pinkbike.com/news/archive/?catid=0&year=2000&month=1'
    ]
    configure_logging(install_root_handler=False)
    logging.basicConfig(
        filename='pinkbike_log.txt',
        format='%(levelname)s: %(message)s',
        level=logging.INFO
    )


    def parse(self, response):

        self.logger.info('Parse function called on {}'.format(response.url))
        articles = response.xpath('//*[@class="news-box2"]')

        for article in articles:

            loader = ItemLoader(item = PinkbikeScraperItem(), selector = article)
                
            loader.add_xpath('article_title', './/a[@class="f22 fgrey4 bold"]')
            loader.add_xpath('article_url', './/*[@class="f22 fgrey4 bold"]/@href')
            loader.add_xpath('article_author_name', './/a[@class="fblack"]')

            article_item = loader.load_item()
            article_detail_url = article.xpath('.//*[@class="f22 fgrey4 bold"]/@href').get()
            yield response.follow(url=str(article_detail_url), callback=self.parse_article, meta={'article_item': article_item})

        next_page = 'https://www.pinkbike.com/news/archive/?catid=0&year=' + str(PinkbikeSpider.url_parameter_year) + '&month=' + str(PinkbikeSpider.url_parameter_month)

        if PinkbikeSpider.url_parameter_month <= 12:
            PinkbikeSpider.url_parameter_month += 1
            logging.info("############################################  We're currently at this page:  ############################################")
            logging.info(next_page)
            logging.info("#########################################################################################################################")
            yield response.follow(next_page, callback=self.parse)

        elif PinkbikeSpider.url_parameter_year <= 2021:
            PinkbikeSpider.url_parameter_year += 1
            PinkbikeSpider.url_parameter_month = 1
            yield response.follow(next_page, callback=self.parse)




    def parse_article(self, response):

        article_item = response.meta['article_item']

        article_selector = response.xpath('//*[@id="content-container"]')
        loader = ItemLoader(item = article_item, selector = article_selector)
    
        loader.add_xpath('article_meta_title', '/html/head/title')
        loader.add_xpath('article_meta_description', '//meta[@name="description"]/@content')
        loader.add_xpath('article_publishing_date', '//meta[@property="article:published_time"]/@content')
        loader.add_xpath('article_tag_name', './/*[@class="blog-section"]//a[contains(@class, "pb-tag")]')

        # comment_selector = response.xpath('//*[@id="comment_wrap"]')
        # loader = ItemLoader(item = article_item, selector = comment_selector)

        loader.add_xpath('comment_author_name', './/*[contains(@class, "cmcont")]/div[1]/a[1]')
        loader.add_xpath('comment_html_id', './/*[contains(@class, "ppcont")]/div[1][contains(@id, "cm")]/@id')
        loader.add_xpath('comment_publishing_date', './/*[contains(@class, "cmcont")]/div[1]/a[@class="time"]')
        loader.add_xpath('comment_upvotes', './/span[contains(@class, "pcu")]')
        loader.add_xpath('comment_downvotes', './/span[contains(@class, "pcd")]')
        loader.add_xpath('comment_content', './/*[contains(@class, "cmcont")]/div[@class="comtext"]')
        # loader.add_xpath('article_comment_flag_number', './/*[contains(@class, "cmcont")]/div[1]/a[2]')

        yield loader.load_item()


