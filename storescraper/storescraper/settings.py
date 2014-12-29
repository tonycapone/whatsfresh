# Scrapy settings for storescraper project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

AUTOTHROTTLE_ENABLED = True
LOG_LEVEL = 'DEBUG'
BOT_NAME = 'storescraper'

SPIDER_MODULES = ['storescraper.spiders']
NEWSPIDER_MODULE = 'storescraper.spiders'

ITEM_PIPELINES = {
    'storescraper.pipelines.SchnucksImgPipeline':10,
    'storescraper.pipelines.CleanseCategories':15,
    'storescraper.pipelines.DuplicatesPipeline' : 17,
    'storescraper.pipelines.StorescraperPipeline' : 20,
}

EXTENSIONS = {
    'storescraper.update-stores.UpdateStores':400,
	'storescraper.notifier.Notifier':500
}

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'storescraper (+http://www.yourdomain.com)'
