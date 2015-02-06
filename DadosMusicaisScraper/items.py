import scrapy


class Musica(scrapy.Item):
    _id = scrapy.Field()
    estilo = scrapy.Field()
    nome = scrapy.Field()
    artista = scrapy.Field()
    tom = scrapy.Field()
    acordes = scrapy.Field()
    exibicoes_cifraclub = scrapy.Field()
    exibicoes_youtube = scrapy.Field()
    qtd_gostei_youtube = scrapy.Field()
    qtd_nao_gostei_youtube = scrapy.Field()
    url = scrapy.Field()
    possui_tabs = scrapy.Field()
    url_cifraclub = scrapy.Field()
    url_youtube = scrapy.Field()
    html = scrapy.Field()


