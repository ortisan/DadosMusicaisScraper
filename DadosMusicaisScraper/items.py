import scrapy


class Musica(scrapy.Item):
    _id = scrapy.Field()
    estilo = scrapy.Field()
    nome = scrapy.Field()
    artista = scrapy.Field()
    tom = scrapy.Field()
    seq_acordes = scrapy.Field()
    acordes = scrapy.Field()
    tonicas = scrapy.Field()
    modos = scrapy.Field()
    inversoes = scrapy.Field()
    qtd_exibicoes_cifraclub = scrapy.Field()
    qtd_exibicoes_youtube = scrapy.Field()
    qtd_gostei_youtube = scrapy.Field()
    qtd_nao_gostei_youtube = scrapy.Field()
    possui_tabs = scrapy.Field()
    possui_capo = scrapy.Field()
    url_cifraclub = scrapy.Field()
    html_cifraclub = scrapy.Field()
    url_busca_youtube = scrapy.Field()
    url_video_youtube = scrapy.Field()


