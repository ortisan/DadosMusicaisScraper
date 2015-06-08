# -*- coding: utf-8 -*-
__author__ = 'marcelo'

from urlparse import urlsplit
from urlparse import urlunsplit
import datetime

import scrapy
from pymongo import MongoClient
from scrapy.http import Request

from DadosMusicaisScraper.settings import *
from DadosMusicaisScraper.items import Musica
from DadosMusicaisScraper.utils import *

#TODO ACRESCENTAR DOIS RATINGS
class RatingsYoutubeSpider(scrapy.Spider):
    name = "RatingsYoutubeSpider"
    allowed_domains = ["youtube.com"]
    start_urls = ['http://www.youtube.com/']

    def __init__(self):

        client = MongoClient(MONGODB_URI)
        db = client[MONGODB_DATABASE]
        self.colecao = db[MONGODB_COLLECTION]

    def parse(self, response):
        # Obtemos os registros_mongo da colecao
        registros_mongo = self.colecao.find({'qtd_exibicoes_youtube': {'$exists': 0}}, {"artista": 1, "nome": 1})

        url = 'https://www.youtube.com/results'
        scheme, netloc, path, query, fragment = urlsplit(url)

        for registro_mongo in registros_mongo:
            id = registro_mongo['_id']
            artista = registro_mongo['artista']
            musica = registro_mongo['nome']

            query = 'search_query=%s %s' % (artista, musica)

            url_busca_video = urlunsplit((scheme, netloc, path, query, fragment))

            request = Request(url_busca_video, callback=self.parse_listagem_videos)

            ## TRANSPORTA DADOS PARA O PROXIMO CALLBACK
            request.meta['_id'] = id
            request.meta['url_busca_youtube'] = url_busca_video

            yield request

    def parse_listagem_videos(self, response):
        try:
            link_video = response.css("ol.section-list div.yt-lockup-video:nth-child(1) a")
            url_video_youtube = 'https://www.youtube.com'

            if (len(link_video) > 0):
                url_video_youtube = url_video_youtube + link_video[0].css('::attr(href)')[0].extract()

            request = Request(url_video_youtube, callback=self.parse_video_youtube)

            request.meta['_id'] = response.meta['_id']
            request.meta['url_busca_youtube'] = response.meta['url_busca_youtube']

            yield request
        except BaseException as exc:
            scrapy.log.msg("Erro ao processar a url <%s>. Detalhes: %s..." % (response.url, exc),
                           loglevel=scrapy.log.ERROR)

    def parse_video_youtube(self, response):

        id = response.meta["_id"]
        url_busca_youtube = response.meta["url_busca_youtube"]

        try:
            regex = re.compile(r'[^0-9]*')

            qtd_exibicoes_youtube_str = response.css("#watch-header .watch-view-count::text")[0].extract()
            qtd_exibicoes_youtube = int(obter_valor_default(regex.sub('', qtd_exibicoes_youtube_str), '0'))

            array_span_rating = response.css(
                "#watch-header #watch-like-dislike-buttons span.yt-uix-button-content::text").extract()

            qtd_gostei_youtube_str = array_span_rating[0] if len(array_span_rating) > 0 else '0'
            qtd_gostei_youtube = int(obter_valor_default(regex.sub('', qtd_gostei_youtube_str), '0'))

            qtd_nao_gostei_youtube_srt = array_span_rating[2] if len(array_span_rating) >= 3 else '0'
            qtd_nao_gostei_youtube = int(obter_valor_default(regex.sub('', qtd_nao_gostei_youtube_srt), '0'))

            dt_publicacao_str = response.css(".watch-time-text::text")[0].extract();

            dt_publicacao_str = re.sub('\w+\son\s', '', dt_publicacao_str)

            dt_publicacao = datetime.datetime.strptime(dt_publicacao_str, '%b %d, %Y')
            data_atual = datetime.datetime.today()
            delta = data_atual - dt_publicacao

            dias = delta.days

            yield Musica(_id=id,
                         url_busca_youtube=url_busca_youtube,
                         url_video_youtube=response.url,
                         qtd_exibicoes_youtube=qtd_exibicoes_youtube,
                         qtd_gostei_youtube=qtd_gostei_youtube,
                         qtd_nao_gostei_youtube=qtd_nao_gostei_youtube,
                         dt_publicacao_youtube=dt_publicacao,
                         dias_desde_publicacao_youtube=dias)

        except BaseException as exc:
            scrapy.log.msg("Erro ao processar a url <%s>. Detalhes: %s..." % (response.url, exc),
                           loglevel=scrapy.log.ERROR)
            yield Musica(_id=id,
                         url_busca_youtube=url_busca_youtube,
                         url_video_youtube=response.url,
                         qtd_exibicoes_youtube=0,
                         qtd_gostei_youtube=0,
                         qtd_nao_gostei_youtube=0)