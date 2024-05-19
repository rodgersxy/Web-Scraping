# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3
import logging

class SQLitePipeline:
    def open_spider(self, spider):
        self.connection = sqlite3.connect('transcripts.db')
        self.cursor = self.connection.cursor()
        # query
        try:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS transcripts (
                    title TEXT,
                    plot TEXT,
                    transcript TEXT,
                    url TEXT
                    )
                """)
            self.connection.commit()
        except sqlite3.OperationalError:
            pass
    
    def close_spider(self, spider):
        self.connection.close()

    def process_item(self, item, spider):
        self.cursor.execute("""
            INSERT INTO transcripts (title, plot, transcript, url) VALUES (?,?,?,?)
            """, (
                item.get('title'),
                item.get('plot'),
                item.get('transcript'),
                item.get('url')
            ))
        self.connection.commit()
        return item
