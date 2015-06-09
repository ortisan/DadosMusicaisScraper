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
#CONCURRENT_REQUESTS_PER_DOMAIN = 24

MONGODB_URI = 'mongodb://localhost:27017'
MONGODB_DATABASE = 'scrapy_tcc'
MONGODB_COLLECTION = 'musicas'
MONGODB_COLLECTION_DA = 'dicionario_acordes'
MONGODB_UNIQUE_KEY = '_id'
# MONGODB_BUFFER_DATA = 1


# Instrucoes de: https://github.com/sebdah/scrapy-mongodb
ITEM_PIPELINES = {
    'DadosMusicaisScraper.pipelines.CustomMongoDBPipeline': 300,
    # 'scrapy_mongodb.MongoDBPipeline': 300,
}

# CONFIGURACOES_LASTFM
LASTFM_API_KEY = "ede9abf4427ec6bfefe56f88753d5722"
LASTFM_API_SECRET = "80aeefd388b84e218f8c0683f8143f5c"

# In order to perform a write operation you need to authenticate yourself
LASTFM_USERNAME = "tentativafc"
import pylast

LASTFM_PASSWORD = pylast.md5("mos12345")

SPOTIFY_CLIENT_ID="812b124fec3c457eb23cd21ef6f2d20d"
SPOTIFY_CLIENT_SECRET="0c4ab397e0324c808b3a71602a1a20ff"

