# ---------------------------------------------------------------------------------------
#
# items.py
#
# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
# 
# ---------------------------------------------------------------------------------------
# Import packages
# ---------------------------------------------------------------------------------------

import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, MapCompose, Identity
from w3lib.html import remove_tags
from datetime import datetime


# ---------------------------------------------------------------------------------------
# Variables
# ---------------------------------------------------------------------------------------



# ---------------------------------------------------------------------------------------
# Program
# ---------------------------------------------------------------------------------------

def split_keywords(text):
    text = [x.strip() for x in text.split(',')]
    return text


def convert_date(text):
    # convert string "2020-01-31T07:00:00-08:00" to Python date
    return datetime.strptime(text, "%Y-%m-%dT%H:%M:%S%z")


def remove_comment_string(text):
    # strip the string comments and return int
    text = text.strip(" Comments")
    return int(text)


class PinkbikeScraperItem(scrapy.Item):

    # Fields scraped from article list

    article_title = scrapy.Field(
        input_processor = MapCompose(remove_tags, str.strip),
        output_processor = TakeFirst()
    )

    article_url = scrapy.Field(        
        input_processor = MapCompose(),
        output_processor = TakeFirst()
    )

    article_author = scrapy.Field(
        input_processor = MapCompose(remove_tags),
        output_processor = TakeFirst()
    )

    article_tags = scrapy.Field(
        input_processor = MapCompose(remove_tags),
        output_processor = Identity()
    )
    article_meta_title = scrapy.Field(
        input_processor = MapCompose(remove_tags),
        output_processor = TakeFirst()
    )

    # Fields scraped from detail page

    article_meta_keywords = scrapy.Field(        
        input_processor = MapCompose(remove_tags, split_keywords),
        output_processor = Identity()
    )

    article_meta_description = scrapy.Field(
        input_processor = MapCompose(remove_tags),
        output_processor = TakeFirst()
    )

    article_number_of_comments = scrapy.Field(
        input_processor = MapCompose(remove_tags, remove_comment_string),
        output_processor = TakeFirst()
    )

    article_published_time = scrapy.Field(
        input_processor = MapCompose(remove_tags, convert_date),
        output_processor = TakeFirst()
    )
    
    article_comment_username = scrapy.Field(
        input_processor = MapCompose(remove_tags),
        output_processor = TakeFirst()
    )

