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

# article_to_tag

# article
    # article_title
    # article_url     
    # article_meta_title
    # article_meta_description
    # article_publishing_date

# article_tag

# article_author

# comment
    # comment_date
    # comment_upvotes
    # comment_downvotes
    # comment_content

# comment_author

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


# article_to_tag table

# Association Table for Many-to-Many relationship between Article and Tag
# https://docs.sqlalchemy.org/en/13/orm/basic_relationships.html#many-to-many
article_to_tag = Table('article_to_tag', Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('article_id', Integer, ForeignKey('article.id')),
    Column('article_tag_id', Integer, ForeignKey('article_tag.id'))
)


# article table

class Article(Base):
    __tablename__ = "article"

    id = Column(Integer, primary_key=True)
    article_author_id = Column(Integer, ForeignKey('article_author.id'))  # Many quotes to one author

    article_title = Column('article_title', Text(), nullable=False)
    article_url = Column('article_url', Text(), nullable=False)
    article_meta_title = Column('article_meta_title', Text(), nullable=False)
    article_meta_description = Column('article_meta_description', Text(), nullable=True)
    article_publishing_date = Column('article_publishing_date', Integer(), nullable=False)

    article_tag = relationship('ArticleTag', secondary='article_to_tag', lazy='dynamic', backref="article")  # M-to-M for article and tags
    comments = relationship('Comment', backref="article") # O-to-M for article and comments


# article_tag

class ArticleTag(Base):
    __tablename__ = "article_tag"

    id = Column(Integer, primary_key=True)

    article_tag_name = Column('article_tag_name', Text(), nullable=True)


# article_author

class ArticleAuthor(Base):
    __tablename__ = "article_author"

    id = Column(Integer, primary_key=True)

    article_author_name = Column('article_author_name', Text(), nullable=True)
    articles = relationship('Article', backref="article_author") # O-to-M for article_author and article


# comment

class Comment(Base):
    __tablename__ = "comment"

    id = Column(Integer, primary_key=True)

    article_id = Column(Integer, ForeignKey('article.id'))  # Many comments to one article
    comment_author_id = Column(Integer, ForeignKey('comment_author.id'))  # Many comments to one author

    comment_html_id = Column('comment_html_id', Integer(), nullable=False)
    comment_publishing_date = Column('comment_publishing_date', Integer(), nullable=False)
    comment_upvotes =  Column('comment_upvotes', Integer(), default=0, nullable=False)
    comment_downvotes = Column('comment_downvotes', Integer(), default=0, nullable=False)
    comment_content = Column('comment_content', Text(), nullable=True)


# comment_author

class CommentAuthor(Base):
    __tablename__ = "comment_author"

    id = Column(Integer, primary_key=True)

    comment_author_name = Column('comment_author_name', Text(), nullable=False)

    comments = relationship('Comment', backref="comment_author") # O-to-M for author and comments
