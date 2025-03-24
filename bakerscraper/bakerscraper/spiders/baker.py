import scrapy
from scrapy.spiders import CrawlSpider
# from ..items import BakerscraperItem

class BakeSpider(CrawlSpider):
    name = "baker"
    allowed_domains = ["sallysbakingaddiction.com"]
    start_urls = ["https://sallysbakingaddiction.com/homemade-artisan-bread/"]

    def start_requests(self):
        # Initial request to start scraping
        yield scrapy.Request(
            self.start_urls[0],
            callback=self.parse_article
        )

    def parse_article(self, response):
        item = BakerscraperItem()

        item["name"] = response.css("h1.entry-title::text").get()
        item["image"] = response.css("div.entry-content img::attr(src)").get()

        # Ingredients
        ingredients = ""
        for i, li in enumerate(response.css("div.tasty-recipes-ingredients-body li"), 1):
            full_text = "".join(li.css("*::text").getall()).strip()
            ingredients += f"{i}. {full_text}\n"
        item["ingredients"] = ingredients.strip()

        # Instructions
        instructions = ""
        for i, li in enumerate(response.css("div.tasty-recipes-instructions-body li"), 1):
            full_text = "".join(li.css("*::text").getall()).strip()
            instructions += f"{i}. {full_text}\n"
        item["instructions"] = instructions.strip()

        # Notes
        notes = ""
        for i, li in enumerate(response.css("div.tasty-recipes-notes-body li"), 1):
            full_text = "".join(li.css("*::text").getall()).strip()
            notes += f"{i}. {full_text}\n"
        item["notes"] = notes.strip()

        # Reviews
        reviews = ""
        for i, li in enumerate(response.css("ol.comment-list li"), 1):
            author = li.css(".comment-author-name::text").get()
            date = li.css(".comment-date::text").get()
            comment = li.css(".comment-content p::text").get()

            if author:
                reviews += f"{i}. {author} ({date}): {comment}\n"
        item["reviews"] = reviews.strip()

        yield item
