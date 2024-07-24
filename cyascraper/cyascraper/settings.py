# Scrapy settings for cyascraper project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "cyascraper"

SPIDER_MODULES = ["cyascraper.spiders"]
NEWSPIDER_MODULE = "cyascraper.spiders"

FEEDS = {
			'products.csv' : {'format' : 'csv'}
}

SCRAPEOPS_API_KEY = '1c71c482-b827-4eaf-bb9f-d6615a1f0969'
SCRAPEOPS_FAKE_USER_AGENT_ENDPOINT = 'https://headers.scrapeops.io/v1/user-agents'
SCRAPEOPS_FAKE_USER_AGENT_ENABLED = True
SCRAPEOPS_FAKE_BROWSER_HEADER_ENABLED = True
SCRAPEOPS_NUM_RESULTS = 50

ROTATING_PROXY_LIST = [
  "187.188.169.169:8080",
  "187.188.16.28:999",
  "177.229.210.66:8080",
  "201.77.110.129:999",
  "186.96.15.7:8080",
  "200.39.120.45:999",
  "45.231.170.137:999",
  "200.76.42.198:999",
  "201.131.239.233:999",
  "159.54.149.67:80",
  "45.174.77.192:999",
  "201.77.108.72:999",
  "187.245.214.7:999",
  "201.77.96.153:999",
  "45.188.167.25:999",
  "189.195.139.178:999",
  "177.240.4.125:999",
  "187.102.236.209:999",
  "45.231.220.79:999",
  "201.77.108.1:999",
  "200.39.120.44:999",
  "201.174.38.160:999",
  "170.0.231.254:999",
  "187.251.222.69:8080",
  "38.7.20.137:999",
  "45.188.164.47:999",
  "201.147.124.253:8111",
  "189.240.60.168:9090",
  "200.76.42.197:999",
  "189.240.60.169:9090",
  "189.240.60.163:9090",
  "189.240.60.171:9090",
  "187.249.20.153:8081",
  "189.203.201.146:8080",
  "45.174.79.8:999",
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
