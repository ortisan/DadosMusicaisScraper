# -*- coding: utf-8 -*-
__author__ = 'marcelo'

import scrapy


class Musica(scrapy.Item):
    _id = scrapy.Field()
    dt_insercao = scrapy.Field()
    estilo_cifraclub = scrapy.Field()
    nome = scrapy.Field()
    artista = scrapy.Field()
    tom_cifraclub = scrapy.Field()
    seq_acordes_cifraclub = scrapy.Field()
    acordes_cifraclub = scrapy.Field()
    tonicas_cifraclub = scrapy.Field()
    modos_cifraclub = scrapy.Field()
    inversoes_cifraclub = scrapy.Field()
    qtd_exibicoes_cifraclub = scrapy.Field()
    qtd_exibicoes_youtube = scrapy.Field()
    qtd_gostei_youtube = scrapy.Field()
    qtd_nao_gostei_youtube = scrapy.Field()
    possui_tabs_cifraclub = scrapy.Field()
    possui_capo_cifraclub = scrapy.Field()
    capo_cifraclub = scrapy.Field()
    url_cifraclub = scrapy.Field()
    linhas_html_cifraclub = scrapy.Field()
    url_busca_youtube = scrapy.Field()
    url_video_youtube = scrapy.Field()
    dt_publicacao_youtube = scrapy.Field()
    dias_desde_publicacao_youtube = scrapy.Field()


