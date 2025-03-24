import scrapy


class IndexRecipesSpider(scrapy.Spider):
    name = "index_recipes"
    allowed_domains = ["sallysbakingaddiction.com"]
    start_urls = ["https://sallysbakingaddiction.com/recipe-index/page/20/"]

    def parse(self, response):
        table = response.css("div.archive-content article.post-filter")
        for item in table:
            recipe_name = item.css("h3.article-title a::text").get()
            recipe_link = item.css("h3.article-title a::attr(href)").get()
            print(f"{recipe_name}: {recipe_link}")

            yield {
                "name": recipe_name,
                "url": recipe_link,
            }

        next_page = response.css("div a.next.page-numbers::attr(href)").get()
        if response.css("div a.next.page-numbers").get():
            yield response.follow(next_page, callback=self.parse)
