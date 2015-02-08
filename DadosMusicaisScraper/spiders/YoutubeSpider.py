# -*- coding: utf-8 -*-
from urlparse import urlsplit
from urlparse import urlunsplit
import re

import scrapy
from pymongo import MongoClient
from scrapy.http import Request

from DadosMusicaisScraper.settings import *
from DadosMusicaisScraper.items import Musica
from DadosMusicaisScraper.utils import *

class YoutubespiderSpider(scrapy.Spider):

    name = "YoutubeSpider"
    allowed_domains = ["youtube.com"]
    start_urls = ['http://www.youtube.com/']

    def __init__(self):

        client = MongoClient(MONGODB_URI)
        db = client[MONGODB_DATABASE]
        self.colecao = db[MONGODB_COLLECTION]

    def parse(self, response):
        # Obtemos os registros_mongo da colecao
        registros_mongo = self.colecao.find({'qtd_exibicoes_youtube': {'$exists': 0}})

        url = 'https://www.youtube.com/results'
        scheme, netloc, path, query, fragment = urlsplit(url)

        for registro_mongo in registros_mongo:
            artista = registro_mongo['artista']
            musica = registro_mongo['nome']

            query = 'search_query=%s %s' % (artista, musica)

            url_busca_video = urlunsplit((scheme, netloc, path, query, fragment))

            ## TRANSPORTA DADOS PARA O PROXIMO CALLBACK
            request = Request(url_busca_video, callback=self.parse_listagem_videos)

            registro_mongo['url_busca_youtube'] = url_busca_video
            request.meta['registro_mongo'] = registro_mongo

            yield request

    def parse_listagem_videos(self, response):
        link_video = response.css("ol#section-list div.yt-lockup-video:nth-child(1) a")
        registro_mongo = response.meta['registro_mongo']
        if (len(link_video) > 0):
            url_video_youtube = 'https://www.youtube.com' + link_video[0].css('::attr(href)')[0].extract()
            request = Request(url_video_youtube, callback=self.parse_video_youtube)
            request.meta['registro_mongo'] = registro_mongo
            yield request
        else:
            yield Musica(_id=registro_mongo['_id'],
                         estilo=registro_mongo['estilo'],
                         nome=registro_mongo['nome'],
                         artista=registro_mongo['artista'],
                         tom=registro_mongo['tom'],
                         acordes=registro_mongo['acordes'],
                         qtd_exibicoes_cifraclub=registro_mongo['qtd_exibicoes_cifraclub'],
                         possui_tabs=registro_mongo['possui_tabs'],
                         url_cifraclub=registro_mongo['url_cifraclub'],
                         html_cifraclub=registro_mongo['html_cifraclub'],
                         url_busca_youtube=registro_mongo['url_busca_youtube'],
                         url_video_youtube=response.url,
                         qtd_exibicoes_youtube=0,
                         qtd_gostei_youtube=0,
                         qtd_nao_gostei_youtube=0)


    def parse_video_youtube(self, response):

        try:
            registro_mongo = response.meta['registro_mongo']

            regex = re.compile(r'[^0-9]*')

            qtd_exibicoes_youtube_str = response.css("#watch-header .watch-view-count::text")[0].extract()
            qtd_exibicoes_youtube = int(obter_valor_default(regex.sub('', qtd_exibicoes_youtube_str), '0'))

            array_span_rating = response.css(
                "#watch-header #watch-like-dislike-buttons span.yt-uix-button-content::text").extract()

            qtd_gostei_youtube_str = array_span_rating[0]
            qtd_gostei_youtube = int(obter_valor_default(regex.sub('', qtd_gostei_youtube_str), '0'))

            qtd_nao_gostei_youtube_srt = array_span_rating[2]
            qtd_nao_gostei_youtube = int(obter_valor_default(regex.sub('', qtd_nao_gostei_youtube_srt), '0'))

            registro_mongo['qtd_exibicoes_youtube'] = qtd_exibicoes_youtube
            registro_mongo['qtd_gostei_youtube'] = qtd_gostei_youtube
            registro_mongo['qtd_nao_gostei_youtube'] = qtd_nao_gostei_youtube

            yield Musica(_id=registro_mongo['_id'],
                         estilo=registro_mongo['estilo'],
                         nome=registro_mongo['nome'],
                         artista=registro_mongo['artista'],
                         tom=registro_mongo['tom'],
                         acordes=registro_mongo['acordes'],
                         qtd_exibicoes_cifraclub=registro_mongo['qtd_exibicoes_cifraclub'],
                         possui_tabs=registro_mongo['possui_tabs'],
                         url_cifraclub=registro_mongo['url_cifraclub'],
                         html_cifraclub=registro_mongo['html_cifraclub'],
                         url_busca_youtube=registro_mongo['url_busca_youtube'],
                         url_video_youtube=response.url,
                         qtd_exibicoes_youtube=qtd_exibicoes_youtube,
                         qtd_gostei_youtube=qtd_gostei_youtube,
                         qtd_nao_gostei_youtube=qtd_nao_gostei_youtube)

        except BaseException as exc:
            scrapy.log.msg("Erro ao processar a url <%s>. Detalhes: %s..." % (response.url, exc), loglevel=scrapy.log.ERROR, logstdout=None)