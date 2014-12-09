import scrapy


class Musica(scrapy.Item):
    estilo = scrapy.Field
    nome = scrapy.Field
    artista = scrapy.Field
    tom = scrapy.Field
    acordes = scrapy.Field
    exibicoes = scrapy.Field
    url = scrapy.Field


