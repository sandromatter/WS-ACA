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


# ---------------------------------------------------------------------------------------
# Program
# ---------------------------------------------------------------------------------------


def convert_race_date(text):
    # convert string "2020-01-31" to Python date
    return int(datetime.strptime(text, "%Y-%m-%d").timestamp())

def convert_integer(text):
    # strip the string comments and return int
    return int(text)

# def convert_position_integer(text):
#     # strip the string comments and return int
#     text = text.strip("-")
#     return int(text)

# def convert_participants_integer(text):
#     # strip the string comments and return int
#     text = text.strip("-")
#     return int(text)


class RarScraperItem(scrapy.Item):

    result_rider_name = scrapy.Field(
        input_processor = MapCompose(remove_tags),
        output_processor = TakeFirst()
    )

    result_data_date = scrapy.Field(
        input_processor = MapCompose(remove_tags, convert_race_date),
        output_processor = TakeFirst()
    )

    result_data_event = scrapy.Field(
        input_processor = MapCompose(remove_tags),
        output_processor = TakeFirst()
    )

    result_data_venue = scrapy.Field(
        input_processor = MapCompose(remove_tags),
        output_processor = TakeFirst()
    )

    result_data_category = scrapy.Field(
        input_processor = MapCompose(remove_tags),
        output_processor = TakeFirst()
    )

    result_data_license_age = scrapy.Field(
        input_processor = MapCompose(remove_tags),
        output_processor = TakeFirst()
    )

    result_data_bib = scrapy.Field(
        input_processor = MapCompose(remove_tags, convert_integer),
        output_processor = TakeFirst()
    )

    result_data_sponsors = scrapy.Field(
        input_processor = MapCompose(remove_tags),
        output_processor = TakeFirst()
    )

    result_data_position = scrapy.Field(
        input_processor = MapCompose(remove_tags),
        output_processor = TakeFirst()
    )

    result_data_participants = scrapy.Field(
        input_processor = MapCompose(remove_tags),
        output_processor = TakeFirst()
    )

    result_data_fastest_time_rider = scrapy.Field(
        input_processor = MapCompose(remove_tags, convert_integer),
        output_processor = TakeFirst()
    )

    result_data_fastest_time_category = scrapy.Field(
        input_processor = MapCompose(remove_tags, convert_integer),
        output_processor = TakeFirst()
    )

    result_data_fastest_time_day = scrapy.Field(
        input_processor = MapCompose(remove_tags, convert_integer),
        output_processor = TakeFirst()
    )
