import scrapy
import json
from cyascraper.items import CyascraperItem
from scrapy_playwright.page import PageMethod



class CyaspiderSpider(scrapy.Spider):
    name = "cyaspider"
    start_urls = ["https://www.cyamoda.com/todos-los-productos/?start=0&sz=264&grid-view=grid-2"]


    def start_requests(self):
        """
        Initiates requests to home URLs with configurations to use Playwright.
        """
        for url in self.start_urls:
            yield scrapy.Request(
                url,
                meta = {
                    'playwright' : True,
                    'playwright_page_methods' : [
                        PageMethod("wait_for_selector", ".pdp-link a"), # Wait for product links to become visible
                        PageMethod("evaluate", "window.scrollBy(0, document.body.scrollHeight)"), # Performs scrolling down
                        PageMethod("wait_for_timeout", 30000), # Wait 30 seconds to load the content
                    ],
                },
            )


    async def parse(self, response):
        """
        Process the initial response by fetching the relative URLs of the items.
        """
        relative_url = response.css('.pdp-link a::attr(href)').getall()
        for url in relative_url:
            article_url = f"https://www.cyamoda.com{url}"
            yield scrapy.Request(url=article_url, callback=self.parse_article_page)

            
    def parse_article_page(self, response):
        """
        Processes the page for each item, extracting the data and storing it in an item.
        """
        article_item = CyascraperItem()

        # Extracts the JSON-LD with the product data
        product = json.loads(
            response.css("script[type='application/ld+json']::text").get()
        )
    
        # Fill in the item fields with the product data.
        article_item['url'] = response.url 
        article_item['name'] = product['name']
        article_item['description'] = product['description']
        article_item['sku'] = product['sku']
        article_item['image'] = json.dumps(product['image'])
        article_item['price_currency'] = product['offers']['priceCurrency']
        article_item['price'] = product['offers']['price']
        article_item['availability'] = product['offers']['availability']

        # Returns the item
        yield article_item