# 🤖 Web Scraping 🛒 to CyA E-commerce

This project has the goal of scraping the website of C&amp;A, an online clothing store. Using various advanced tools and techniques, this project allows to extract relevant data from the online store for further analysis and use.

![image](https://github.com/user-attachments/assets/b70615bf-fde3-4185-961e-7d4647884d61)


***

## Features
* **Scrapy**: Used as the main scraping framework.
* **Playwright**: Integrated to handle dynamically loaded content through infinite scrolling.
* **Pipelines**: Implemented to process and store the extracted data efficiently.
* **Middlewares**: Used to manage requests and responses, including proxy, user-agent and browser header agent rotation.
* **Items**: Defined to structure and organize the extracted data.
* **Proxies**: Used to avoid blocking and IP restrictions.

***

## 🕷️ Spyder Class

````python
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
````

***

## 📦 Item Class

````python
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
    
````

***

## 🔃 Middlewares

````python
from urllib.parse import urlencode
from random import randint
import requests

class ScrapeOpsFakeUserAgentMiddleware: # ----------------------------- User-Agent --------------------------

    @classmethod
    def from_crawler(cls, crawler):
        """
        Class method to initialize the middleware from the crawler.
        """
        return cls(crawler.settings)


    def __init__(self, settings):
        """
        Initializes the middleware configurations.
        """
        self.scrapeops_api_key = settings.get('SCRAPEOPS_API_KEY')
        self.scrapeops_endpoint = settings.get('SCRAPEOPS_FAKE_USER_AGENT_ENDPOINT', 'http://headers.scrapeops.io/v1/user-agents?') 
        self.scrapeops_fake_user_agents_active = settings.get('SCRAPEOPS_FAKE_USER_AGENT_ENABLED', False)
        self.scrapeops_num_results = settings.get('SCRAPEOPS_NUM_RESULTS')
        self.headers_list = []
        self._get_user_agents_list()
        self._scrapeops_fake_user_agents_enabled()


    def _get_user_agents_list(self):
        """
        Gets the list of User Agents from the configured endpoint.
        """
        payload = {'api_key': self.scrapeops_api_key}
        if self.scrapeops_num_results is not None:
            payload['num_results'] = self.scrapeops_num_results
        response = requests.get(self.scrapeops_endpoint, params=urlencode(payload))
        json_response = response.json()
        self.user_agents_list = json_response.get('result', [])


    def _get_random_user_agent(self):
        """
        Returns a random User Agent from the list.
        """
        random_index = randint(0, len(self.user_agents_list) - 1)
        return self.user_agents_list[random_index]


    def _scrapeops_fake_user_agents_enabled(self):
        """
        Enables or disables the use of fake User Agents according to the configuration.
        """
        if self.scrapeops_api_key is None or self.scrapeops_api_key == '' or self.scrapeops_fake_user_agents_active == False:
            self.scrapeops_fake_user_agents_active = False
        else:
            self.scrapeops_fake_user_agents_active = True

    
    def process_request(self, request, spider):
        """
        Modifies the User Agent of the request with a random one from the list.
        """     
        random_user_agent = self._get_random_user_agent()
        request.headers['User-Agent'] = random_user_agent


class ScrapeOpsFakeBrowserHeaderAgentMiddleware: #---------------------- Browser Header Agent ----------------------------
	
    @classmethod
    def from_crawler(cls, crawler):
        """
        Class method to initialize the middleware from the crawler
        """
        return cls(crawler.settings)


    def __init__(self, settings):
        """
        Initializes the middleware configurations.
        """
        self.scrapeops_api_key = settings.get('SCRAPEOPS_API_KEY')
        self.scrapeops_endpoint = settings.get('SCRAPEOPS_FAKE_BROWSER_HEADER_ENDPOINT', 'http://headers.scrapeops.io/v1/browser-headers?') 
        self.scrapeops_fake_browser_headers_active = settings.get('SCRAPEOPS_FAKE_BROWSER_HEADER_ENABLED', False)
        self.scrapeops_num_results = settings.get('SCRAPEOPS_NUM_RESULTS')
        self.headers_list = []
        self._get_headers_list()
        self._scrapeops_fake_browser_headers_enabled()


    def _get_headers_list(self):
        """
        Gets the list of browser headers from the configured endpoint.
        """
        payload = {'api_key': self.scrapeops_api_key}
        if self.scrapeops_num_results is not None:
          payload['num_results'] = self.scrapeops_num_results
        response = requests.get(self.scrapeops_endpoint, params=urlencode(payload))
        json_response = response.json()
        self.headers_list = json_response.get('result', [])


    def _get_random_browser_header(self):
        """
        Returns a random browser header from the list.
        """
        random_index = randint(0, len(self.headers_list) - 1)
        return self.headers_list[random_index]


    def _scrapeops_fake_browser_headers_enabled(self):
        """
        Enables or disables the use of fake browser headers depending on the configuration.
        """
        if self.scrapeops_api_key is None or self.scrapeops_api_key == '' or self.scrapeops_fake_browser_headers_active == False:
          self.scrapeops_fake_browser_headers_active = False
        else:
          self.scrapeops_fake_browser_headers_active = True


    def process_request(self, request, spider):
        """
        Modifies the request headers with a random one from the list of browser headers.
        """   
        random_browser_header = self._get_random_browser_header()
        
        request.headers['accept-language'] = random_browser_header['accept-language']
        request.headers['accept'] = random_browser_header['accept']
        request.headers['accept-encoding'] = random_browser_header['accept-encoding']
        request.headers['user-agent'] = random_browser_header['user-agent']
        request.headers['upgrade-insecure-requests'] = random_browser_header.get('upgrade-insecure-requests')

    
````

***

## Pipeline

````python
from itemadapter import ItemAdapter
import re

class CyascraperPipeline:
    def process_item(self, item, spider):
        """
        Create an adapter to access and modify the item more easily.
        """
        adapter = ItemAdapter(item)

        ## availability -> extract the items in stock
        item_availability = adapter.get('availability')
        adapter['availability'] = item_availability.split('/')[3]

        ## description -> Delete html tags and merge all list into one
        item_description = adapter.get('description')
        description_cleaned = ''.join(re.sub(r'<br>|<p>|</p>', ' ', item_description))
        adapter['description'] = description_cleaned

        ##price -> convert to float 
        item_price = adapter.get('price')
        adapter['price'] = float(item_price)

        return item
````

***

## ⚙️ Settings.py

````python
BOT_NAME = "cyascraper"

SPIDER_MODULES = ["cyascraper.spiders"]
NEWSPIDER_MODULE = "cyascraper.spiders"

FEEDS = {
    'products.csv' : {'format' : 'csv'}
}

SCRAPEOPS_API_KEY = 'YOUR_API_KEY'
SCRAPEOPS_FAKE_USER_AGENT_ENDPOINT = 'YOUR_ENDPOINT'
SCRAPEOPS_FAKE_USER_AGENT_ENABLED = True
SCRAPEOPS_FAKE_BROWSER_HEADER_ENABLED = True
SCRAPEOPS_NUM_RESULTS = 50

ROTATING_PROXY_LIST = [
    # add your proxies here
]

DNS_TIMEOUT = 120

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = "cyascraper (+http://www.yourdomain.com)"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Language": "en",
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    "cyascraper.middlewares.CyascraperSpiderMiddleware": 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    "cyascraper.middlewares.ScrapeOpsFakeUserAgentMiddleware": 400,
    "cyascraper.middlewares.ScrapeOpsFakeBrowserHeaderAgentMiddleware": 543,
    "rotating_proxies.middlewares.RotatingProxyMiddleware": 610,
    "rotating_proxies.middlewares.BanDetectionMiddleware": 620,
}

DOWNLOAD_HANDLERS = {
    "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
    "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
}

PLAYWRIGHT_BROWSER_TYPE = "chromium"

# PLAYWRIGHT_LAUNCH_OPTIONS = {
#     "headless": False,
#     "timeout": 20 * 1000,  # 20 seconds
# }

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    "cyascraper.pipelines.CyascraperPipeline": 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = "httpcache"
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"

````
