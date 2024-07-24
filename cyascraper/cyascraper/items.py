# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CyascraperItem(scrapy.Item):
    """
    Defines the data model for the items extracted during scraping.
    """
    url = scrapy.Field()
    name = scrapy.Field()
    description = scrapy.Field()
    sku = scrapy.Field()
    image = scrapy.Field()
    price_currency = scrapy.Field() # -> Offers
    price = scrapy.Field()
    availability = scrapy.Field()
    
    
