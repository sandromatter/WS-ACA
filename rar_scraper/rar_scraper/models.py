# ---------------------------------------------------------------------------------------
#
# models.py
#
# Set up the db structure with sqlalchemy
# 
# ---------------------------------------------------------------------------------------
# Import packages
# ---------------------------------------------------------------------------------------

from sqlalchemy import create_engine, Column, Table, ForeignKey
from sqlalchemy import Integer, Text 
from sqlalchemy.ext.declarative import declarative_base
from scrapy.utils.project import get_project_settings
from sqlalchemy.orm import relationship
from sqlalchemy.sql.elements import Null


# ---------------------------------------------------------------------------------------
# Database model > Tables
# ---------------------------------------------------------------------------------------

# result
    # result_bib
    # result_beat
    # result_position
    # result_cat_participants

# rider
    # rider_meta_title
    # rider_meta_url     
    # rider_name

# sponsor_name

# event
    # event_date
    # event_name
    # event_venue

# category
    # category_name


# ---------------------------------------------------------------------------------------
# Program
# ---------------------------------------------------------------------------------------

Base = declarative_base()


def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    return create_engine(get_project_settings().get("CONNECTION_STRING"))

def create_table(engine):
    Base.metadata.create_all(engine)


# Rider table

class Rider(Base):
    __tablename__ = "rider"

    id = Column(Integer, primary_key=True)

    rider_meta_url = Column('rider_meta_url', Text())
    rider_name = Column('rider_name', Text())

    results = relationship('Result', backref="rider") # O-to-M for rider and result


# Event table

class Event(Base):
    __tablename__ = "event"

    id = Column(Integer, primary_key=True)

    event_name = Column('event_name', Text())
    event_date = Column('event_date', Integer())
    event_venue = Column('event_venue', Text())
 
    results = relationship('Result', backref="event") # O-to-M for event and result


# Category table

class Category(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True)

    category_name = Column('category_name', Text())
 
    results = relationship('Result', backref="category") # O-to-M for category and result


# Result table

class Result(Base):
    __tablename__ = "result"

    id = Column(Integer, primary_key=True)
    event_id = Column(Integer, ForeignKey('event.id'))  # Many riders to one event
    category_id = Column(Integer, ForeignKey('category.id'))  # Many riders to one category
    rider_id = Column(Integer, ForeignKey('rider.id'))  # Many results to one rider

    result_bib = Column('result_bib', Integer())
    result_beat = Column('result_beat', Integer())
    result_position = Column('result_position', Integer())
    result_cat_participants = Column('result_cat_participants', Integer())