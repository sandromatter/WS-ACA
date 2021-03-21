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
from .models import Article, Comment, CommentAuthor, ArticleAuthor, ArticleTag, ArticleKeyword, db_connect, create_table
from scrapy.exceptions import DropItem
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


        # Check if the ArticleAuthor already exists
        article_author = (
            self.session.query(ArticleAuthor)
            .filter_by(article_author_name = item["article_author_name"])
            .first()
        )

        if article_author is None:
            article_author = ArticleAuthor(article_author_name = item["article_author_name"])

        # try:
        #     self.session.add(article_author)
        # except:
        #     self.session.rollback()
        #     raise
        # finally:
        #     self.session.commit()

        self.session.add(article_author)
        self.session.commit()


        # Check if the Article already exists
        article = (
            self.session.query(Article)
            .filter_by(article_author_id = article_author.id, article_title = item["article_title"], article_url = item["article_url"])
            .first()
        )

        if article is None:
            article = Article(article_author_id = article_author.id, article_title = item["article_title"], article_url = item["article_url"])

        article.article_meta_title = item["article_meta_title"]
        article.article_meta_description = item["article_meta_description"]
        article.article_publishing_date = item["article_publishing_date"]

        # try:
        #     self.session.add(article)
        # except:
        #     self.session.rollback()
        #     raise
        # finally:
        #     self.session.commit()

        self.session.add(article)
        self.session.commit()


        # Check if the ArticleTag already exists
        if "article_tag_name" in item:
            for i in item["article_tag_name"]:

                tag = self.session.query(ArticleTag).filter_by(article_tag_name = i).first()

                # check whether the current tag already exists in the database
                if tag is None:  # the current tag exists
                    tag = ArticleTag(article_tag_name = i)
                    article.article_tag.append(tag)

        # try:
        #     self.session.add(article)
        # except:
        #     self.session.rollback()
        #     raise
        # finally:
        #     self.session.commit()

        self.session.add(article)
        self.session.commit()


        # Check if the ArticleKeyword already exists
        if "article_keyword_name" in item:
            for j in item["article_keyword_name"]:

                keyword = self.session.query(ArticleKeyword).filter_by(article_keyword_name = j).first()

                # check whether the current keyword already exists in the database
                if keyword is None:  # the current keyword exists
                    keyword = ArticleKeyword(article_keyword_name = j)
                    article.article_keyword.append(keyword)

        # try:
        #     self.session.add(article)
        # except:
        #     self.session.rollback()
        #     raise
        # finally:
        #     self.session.commit()

        self.session.add(article)
        self.session.commit()


        # Check if the CommentAuthor already exists
        if "comment_author_name" in item:
            for k in item["comment_author_name"]:

                comment_author = self.session.query(CommentAuthor).filter_by(comment_author_name = k).first()

                # check whether the current comment_author already exists in the database
                if comment_author is None:  # the current comment_author exists
                    comment_author = CommentAuthor(comment_author_name = k)

        # try:
        #     self.session.add(comment_author)
        #     self.session.commit()
        # except:
        #     self.session.rollback()
        #     raise
        # finally:
        #     self.session.close()

        self.session.add(comment_author)
        self.session.commit()


        # Check if the Comment already exists
        comment = (
            self.session.query(Comment)
            .filter_by(comment_author_id = comment_author.id, comment_publishing_date = item["comment_publishing_date"])
            .first()
        )

        if comment is None:
            comment = Comment(comment_author_id = comment_author.id, comment_publishing_date = item["comment_publishing_date"])

        comment.comment_upvotes = item["comment_upvotes"]
        comment.comment_downvotes = item["comment_downvotes"]
        comment.comment_content = item["comment_content"]

        # try:
        #     self.session.add(comment)
        # except:
        #     self.session.rollback()
        #     raise
        # finally:
        #     self.session.commit()

        self.session.add(comment)
        self.session.commit()


        return item

    def process_item(self, item, spider):
        self.store_db(item)
        logging.info(item)
        logging.info("****Item stored in database****")
        return item