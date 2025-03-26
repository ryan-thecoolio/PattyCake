import scrapy
from scrapy.spiders import CrawlSpider
from ..items import BakerscraperItem
import json

absolute_path = r"C:\Users\mayma\PycharmProjects\BakingAdvisor\bakerscraper\bakerscraper\recipe_list_scraped.json"
with open(absolute_path, "r", encoding="utf-8") as f:
    d = json.load(f)


class BakeSpider(CrawlSpider):
    name = "baker"

    def start_requests(self):
        for recipe in d:
            yield scrapy.Request(
                recipe['url'],
                callback=self.parse_article
            )

    def parse_article(self, response):
        item = BakerscraperItem()

        item["name"] = response.css("h1.entry-title::text").get()
        item["image"] = response.css("div.entry-content img::attr(src)").get()

        # Ingredients
        ingredients = ""
        for j, li in enumerate(response.css("div.tasty-recipes-ingredients-body li"), 1):
            full_text = "".join(li.css("*::text").getall()).strip()
            ingredients += f"{j}. {full_text}\n"
            if ingredients == "":
                break
        item["ingredients"] = ingredients.strip()

        # Instructions
        if ingredients != "":
            instructions = ""
            for j, li in enumerate(response.css("div.tasty-recipes-instructions-body li"), 1):
                full_text = "".join(li.css("*::text").getall()).strip()
                instructions += f"{j}. {full_text}\n"
            item["instructions"] = instructions.strip()

            # Notes
            notes = ""
            for j, li in enumerate(response.css("div.tasty-recipes-notes-body li"), 1):
                full_text = "".join(li.css("*::text").getall()).strip()
                notes += f"{j}. {full_text}\n"
            item["notes"] = notes.strip()

            # Reviews
            reviews = ""
            for j, li in enumerate(response.css("ol.comment-list li"), 1):
                author = li.css(".comment-author-name::text").get()
                date = li.css(".comment-date::text").get()
                comment = li.css(".comment-content p::text").get()

                if author:
                    reviews += f"{j}. {author} ({date}): {comment}\n"
            item["reviews"] = reviews.strip()

            yield item
