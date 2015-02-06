# -*- coding: utf-8 -*-

# Scrapy settings for CifraClubScraperUngit project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'DadosMusicaisScraper'

SPIDER_MODULES = ['DadosMusicaisScraper.spiders']
NEWSPIDER_MODULE = 'DadosMusicaisScraper.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'CifraClubScraperUngit (+http://www.yourdomain.com)'

#Instrucoes de: https://github.com/sebdah/scrapy-mongodb
ITEM_PIPELINES = {
    #'DadosMusicaisScraper.pipelines.CifraClubPipeline': 300
    'scrapy_mongodb.MongoDBPipeline',
}

MONGODB_URI = 'mongodb://localhost:27017'
MONGODB_DATABASE = 'scrapy'
MONGODB_COLLECTION = 'musicas2'

LOG_LEVEL = 'INFO'
CONCURRENT_REQUESTS = 100