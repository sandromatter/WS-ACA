# ---------------------------------------------------------------------------------------
#
# pipelines.py
#
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# 
# useful for handling different item types with a single interface
# 
# ---------------------------------------------------------------------------------------
# Import packages
# ---------------------------------------------------------------------------------------

from sqlalchemy.orm import sessionmaker
from .models import Result, Rider, Event, Category, db_connect, create_table
import logging


# ---------------------------------------------------------------------------------------
# Program
# ---------------------------------------------------------------------------------------

class StoreToDatabasePipeline(object):


    def __init__(self):
        """
        Initializes database connection and sessionmaker
        Creates tables
        """
        engine = db_connect()
        create_table(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()


    def store_db(self, item):

        # Check if the Rider already exists
        rider = (
            self.session.query(Rider)
            .filter_by(rider_name = item["rider_name"], rider_meta_url = item["rider_meta_url"])
            .first()
        )

        if rider is None:
            rider = Rider(rider_name = item["rider_name"], rider_meta_url = item["rider_meta_url"])

        self.session.add(rider)
        self.session.commit()

        # Check if the Category already exists
        if "category_name" in item:
            for i in item["category_name"]:

                category = self.session.query(Category).filter_by(category_name = i).first()

                # check whether the current category_name already exists in the database
                if category is None:  # the current category_name exists
                    category = Category(category_name = i)

                self.session.add(category)
        
        self.session.commit()

        # Check if the Event already exists
        if "event_name" in item:
            for k in range(len(item["event_name"])):

                event = self.session.query(Event).filter_by(event_name = item["event_name"][k]).first()

                # check whether the current event_name already exists in the database
                if event is None:  # the current event_name exists
                    event = Event(event_name = item["event_name"][k])

                event.event_date = item["event_date"][k]
                event.event_venue = item["event_venue"][k]

                self.session.add(event)
        
        self.session.commit()

        # Check if the Result already exists
        if "result_position" in item:
            for j in range(len(item["result_position"])):

                current_event = self.session.query(Event).filter_by(event_name = item["event_name"][j]).first()
                current_category = self.session.query(Category).filter_by(category_name = item["category_name"][j]).first()
                current_rider = self.session.query(Rider).filter_by(rider_name = item["rider_name"]).first()

                result = self.session.query(Result).filter_by(event_id = current_event.id, category_id = current_category.id, rider_id = current_rider.id, result_position = item["result_position"][j], result_bib = item["result_bib"][j], result_beat = item["result_beat"][j], result_cat_participants = item["result_cat_participants"][j]).first()

                # check whether the current result already exists in the database
                if result is None:  # the current result doesn't exist
                    result = Result(event_id = current_event.id, category_id = current_category.id, rider_id = current_rider.id, result_position = item["result_position"][j], result_bib = item["result_bib"][j], result_beat = item["result_beat"][j], result_cat_participants = item["result_cat_participants"][j])

                self.session.add(result)
        
        self.session.commit()

        return item
        

    def process_item(self, item, spider):
        self.store_db(item)
        # logging.info("@@@@  ↓  @@@@  ↓  @@@@  ↓  @@@@  ↓  @@@@  ↓  Item stored in database  ↓  @@@@  ↓  @@@@  ↓  @@@@  ↓  @@@@  ↓  @@@@")
        # logging.info(item)
        # logging.info("@@@@  ↑  @@@@  ↑  @@@@  ↑  @@@@  ↑  @@@@  ↑  @@@@  ↑  @@@@  ↑  @@@@  ↑  @@@@  ↑  @@@@  ↑  @@@@  ↑  @@@@  ↑  @@@@  ↑  @@@@")
        # logging.info("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        return item