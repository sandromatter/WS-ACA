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
from itemloaders.processors import TakeFirst, MapCompose, Identity
from sqlalchemy.sql.elements import Null
from sqlalchemy.sql.expression import null
from w3lib.html import remove_tags
from datetime import datetime
import re

# ---------------------------------------------------------------------------------------
# Program
# ---------------------------------------------------------------------------------------

def convert_race_date(text):
    # convert string "2020-01-31" to Python date
    return int(datetime.strptime(text, "%Y-%m-%d").timestamp())

def convert_integer(text):
    # strip the string comments and return int
    try:
        text = int(text)
    except:
        text = str("")
    return text

def convert_beat_integer(text):
    # strip the percent sign and return int
    beat_string = text
    beat_integer = beat_string[:-1]
    try:
        text = int(beat_integer)
    except:
        text = str("")
    return text

def convert_position_integer(text):
    # Split into "position" and "participants"
    position_string = text
    split_string = position_string.split("/", 1)
    substring_position = split_string[0]
    try:
        text = int(substring_position)
    except:
        text = str("")
    return text

def convert_participants_integer(text):
    # Split into "position" and "participants"
    position_string = text
    split_string = position_string.split("/", 1)
    substring_participants = split_string[1]
    try:
        text = int(substring_participants)
    except:
        text = str("")
    return text

class RarScraperItem(scrapy.Item):

    rider_meta_url = scrapy.Field(
        input_processor = MapCompose(remove_tags),
        output_processor = TakeFirst()
    )

    rider_name = scrapy.Field(
        input_processor = MapCompose(remove_tags, str.lower),
        output_processor = TakeFirst()
    )

    result_bib = scrapy.Field(
        input_processor = MapCompose(remove_tags, convert_integer),
        output_processor = Identity()
    )

    result_beat = scrapy.Field(
        input_processor = MapCompose(remove_tags, convert_beat_integer),
        output_processor = Identity()
    )

    result_position = scrapy.Field(
        input_processor = MapCompose(remove_tags, convert_position_integer),
        output_processor = Identity()
    )

    result_cat_participants = scrapy.Field(
        input_processor = MapCompose(remove_tags, convert_participants_integer),
        output_processor = Identity()
    )

    event_date = scrapy.Field(
        input_processor = MapCompose(remove_tags, convert_race_date),
        output_processor = Identity()
    )

    event_name = scrapy.Field(
        input_processor = MapCompose(remove_tags),
        output_processor = Identity()
    )

    event_venue = scrapy.Field(
        input_processor = MapCompose(remove_tags),
        output_processor = Identity()
    )

    category_name = scrapy.Field(
        input_processor = MapCompose(remove_tags),
        output_processor = Identity()
    )
