# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import sqlite3
from datetime import datetime


class BakerscraperPipeline:
    def __init__(self, db_name="bakerscraper.db"):
        self.db_name = db_name
        self.conn = None

    def open_spider(self, spider):
        self.conn = sqlite3.connect(self.db_name)
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS bakerscraper (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            image_url TEXT NOT NULL,
            ingredients TEXT NOT NULL,
            instructions TEXT NOT NULL,
            notes TEXT NOT NULL,
            reviews TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP )
        """)
        self.conn.commit()

    def close_spider(self, spider):
        if self.conn:
            self.conn.close()
            self.conn = None

    def process_item(self, item, spider):
        cursor = self.conn.cursor()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("""INSERT INTO bakerscraper
                      (name, image_url, ingredients, instructions, notes, reviews, timestamp)
                      VALUES (?, ?, ?, ?, ?, ?, ?)""",
                       (item["name"], item["image"], item["ingredients"], item["instructions"],
                        item["notes"], item["reviews"], timestamp)
                       )
        self.conn.commit()
        print(
            f"Stored in database: {self.db_name}, name: {item['name']}...")
        return item
