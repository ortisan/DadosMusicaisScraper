# -*- coding: utf-8 -*-
__author__ = 'marcelo'


# Scrapy settings for CifraClubScraperUngit project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
# http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'DadosMusicaisScraper'

SPIDER_MODULES = ['DadosMusicaisScraper.spiders']

LOG_ENABLED = True
LOG_LEVEL = 'INFO'
LOG_FILE = './logs/dadosmusicais.log'
LOG_STDOUT = True

CONCURRENT_REQUESTS = 100

MONGODB_URI = 'mongodb://localhost:27017'
MONGODB_DATABASE = 'scrapy'
MONGODB_COLLECTION = 'musicas'
MONGODB_COLLECTION_DA = 'acordes_estilos'
MONGODB_UNIQUE_KEY = '_id'
# MONGODB_BUFFER_DATA = 1


# Instrucoes de: https://github.com/sebdah/scrapy-mongodb
ITEM_PIPELINES = {
    'DadosMusicaisScraper.pipelines.CustomMongoDBPipeline': 300,
    # 'scrapy_mongodb.MongoDBPipeline': 300,
}

# CONFIGURACOES_LASTFM
LASTFM_API_KEY = ""
LASTFM_API_SECRET = ""

# In order to perform a write operation you need to authenticate yourself
LASTFM_USERNAME = ""
import pylast

LASTFM_PASSWORD = pylast.md5("")

