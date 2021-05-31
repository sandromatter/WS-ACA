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
            try: 
                loader = ItemLoader(item = RarScraperItem(), selector = result)
                    
                loader.add_xpath('result_rider_name', '//*[@id="h1-title"]')
                loader.add_xpath('result_data_date', '//*[@id="T1"]/tbody/tr/td[2]/time/@datetime')
                loader.add_xpath('result_data_event', '//*[@id="T1"]/tbody/tr/td[3]')
                loader.add_xpath('result_data_venue', '//*[@id="T1"]/tbody/tr/td[5]')
                loader.add_xpath('result_data_category', '//*[@id="T1"]/tbody/tr/td[6]')
                loader.add_xpath('result_data_license_age', '//*[@id="T1"]/tbody/tr/td[7]')
                loader.add_xpath('result_data_bib', '//*[@id="T1"]/tbody/tr/td[8]')
                loader.add_xpath('result_data_sponsors', '//*[@id="T1"]/tbody/tr/td[9]')
                loader.add_xpath('result_data_position', '//*[@id="T1"]/tbody/tr/td[10]')
                loader.add_xpath('result_data_participants', '//*[@id="T1"]/tbody/tr/td[10]/span')
                # loader.add_xpath('result_data_fastest_time_rider', '//*[@id="T1"]/tbody/tr/td[12]/@data-sb')
                # loader.add_xpath('result_data_fastest_time_category', '//*[@id="T1"]/tbody/tr/td[13]/@data-sb')
                # loader.add_xpath('result_data_fastest_time_day', '//*[@id="T1"]/tbody/tr/td[15]/@data-sb')

                yield loader.load_item()

            except:
                next_page = 'https://www.rootsandrain.com/rider' + str(RarSpider.url_parameter_rider)

            next_page = 'https://www.rootsandrain.com/rider' + str(RarSpider.url_parameter_rider)

        if RarSpider.url_parameter_rider <= 999999:
            RarSpider.url_parameter_rider += 1
            logging.info("############################################  We're currently at this page:  ############################################")
            logging.info(next_page)
            logging.info("#########################################################################################################################")
            yield response.follow(next_page, callback=self.parse)


