# ---------------------------------------------------------------------------------------
#
# rar_spider.py
# 
# ---------------------------------------------------------------------------------------
# Import packages
# ---------------------------------------------------------------------------------------

import scrapy
from ..items import RarScraperItem
from scrapy.loader import ItemLoader
import logging
from scrapy.utils.log import configure_logging 

# ---------------------------------------------------------------------------------------
# Program
# ---------------------------------------------------------------------------------------

class RarSpider(scrapy.Spider):
    name = 'rar'
    allowed_domains = ['rootsandrain.com']
    url_parameter_rider = 2
    start_urls = [
        'https://www.rootsandrain.com/rider1'
    ]
    configure_logging(install_root_handler=False)
    logging.basicConfig(
        filename='rar_log.txt',
        format='%(levelname)s: %(message)s',
        level=logging.INFO
    )


    def parse(self, response):

        self.logger.info('Parse function called on {}'.format(response.url))
        results = response.xpath('//*[@id="container"]')

        for result in results:
            loader = ItemLoader(item = RarScraperItem(), selector = result)
                
            loader.add_xpath('rider_meta_url', '//meta[@property="og:url"]/@content')
            loader.add_xpath('rider_name', '//*[@id="h1-title"]')
            loader.add_xpath('category_name', '//*[@id="T1"]/tbody/tr/td[6]')
            loader.add_xpath('event_name', '//*[@id="T1"]/tbody/tr/td[3]')
            loader.add_xpath('event_date', '//*[@id="T1"]/tbody/tr/td[2]/time/@datetime')
            loader.add_xpath('event_venue', '//*[@id="T1"]/tbody/tr/td[5]')
            loader.add_xpath('event_participants', '//*[@id="T1"]/tbody/tr/td[10]/span')
            loader.add_xpath('result_bib', '//*[@id="T1"]/tbody/tr/td[8]')
            loader.add_xpath('result_position', '//*[@id="T1"]/tbody/tr/td[10]')

            yield loader.load_item()

            next_page = 'https://www.rootsandrain.com/rider' + str(RarSpider.url_parameter_rider)

        if RarSpider.url_parameter_rider <= 200000:
            RarSpider.url_parameter_rider += 1
            logging.info("    ")
            logging.info("############################################  We're currently at this page:  ############################################")
            logging.info(next_page)
            logging.info("#########################################################################################################################")
            logging.info("    ")
            yield response.follow(next_page, callback=self.parse)


