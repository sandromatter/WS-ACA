# ---------------------------------------------------------------------------------------
#
# database.py
#
# ---------------------------------------------------------------------------------------
# Import packages
# ---------------------------------------------------------------------------------------

import sqlite3


# ---------------------------------------------------------------------------------------
# Variables
# ---------------------------------------------------------------------------------------



# ---------------------------------------------------------------------------------------
# App initialization / configuration
# ---------------------------------------------------------------------------------------

# Create database
db = sqlite3.connect("src/pinkbike__archive.db")
c = db.cursor()

c.execute(""" CREATE TABLE IF NOT EXISTS articles(
    article_id INTEGER NOT NULL PRIMARY KEY,
    article_title TEXT,
    article_url TEXT,
    article_author TEXT,
    article_description TEXT,
    article_publishing_date TEXT,
    article_number_of_comments INTEGER
    article_scrape_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    ) """)

# c.execute(""" CREATE TABLE IF NOT EXISTS articles(
#     article_title TEXT,
#     article_url TEXT,
#     article_author TEXT,
#     article_description TEXT,
#     article_publishing_date_yyyy INTEGER,
#     article_publishing_date_mm INTEGER,
#     article_publishing_date_dd INTEGER,
#     article_publishing_date_HH INTEGER,
#     article_publishing_date_MM INTEGER,
#     article_publishing_date_SS INTEGER,
#     article_publishing_date_timezone TEXT,
#     article_number_of_comments INTEGER
#     article_scrape_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
#     ) """)

c.execute(""" SELECT * FROM articles """)
results = c.fetchall()

print(results)
print("Command executed successfully...")

db.commit()

db.close()