# -*- coding: utf-8 -*-
from urlparse import urlsplit
from urlparse import urlunsplit

import scrapy
from pymongo import MongoClient
from scrapy.http import Request

from DadosMusicaisScraper.settings import *
from DadosMusicaisScraper.items import Musica
from DadosMusicaisScraper.utils import *


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
        registros_mongo = self.colecao.find({'qtd_exibicoes_youtube': {'$exists': 0}})

        url = 'https://www.youtube.com/results'
        scheme, netloc, path, query, fragment = urlsplit(url)

        for registro_mongo in registros_mongo:
            artista = registro_mongo['artista']
            musica = registro_mongo['nome']

            query = 'search_query=%s %s' % (artista, musica)

            url_busca_video = urlunsplit((scheme, netloc, path, query, fragment))

            request = Request(url_busca_video, callback=self.parse_listagem_videos)

            ## TRANSPORTA DADOS PARA O PROXIMO CALLBACK
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
                         dt_insercao=registro_mongo['dt_insercao'],
                         estilo=registro_mongo['estilo'],
                         nome=registro_mongo['nome'],
                         artista=registro_mongo['artista'],
                         tom=registro_mongo['tom'],
                         possui_tabs=registro_mongo['possui_tabs'],
                         possui_capo=registro_mongo['possui_capo'],
                         capo=registro_mongo['capo'],
                         seq_acordes=registro_mongo['seq_acordes'],
                         seq_acordes_brutos=registro_mongo['seq_acordes_brutos'],
                         qtd_exibicoes_cifraclub=registro_mongo['qtd_exibicoes_cifraclub'],
                         url_cifraclub=registro_mongo['url_cifraclub'],
                         linhas_html_cifraclub=registro_mongo['linhas_html_cifraclub'],
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

            qtd_gostei_youtube_str = array_span_rating[0] if len(array_span_rating) > 0 else '0'
            qtd_gostei_youtube = int(obter_valor_default(regex.sub('', qtd_gostei_youtube_str), '0'))

            qtd_nao_gostei_youtube_srt = array_span_rating[2] if len(array_span_rating) >= 3 else '0'
            qtd_nao_gostei_youtube = int(obter_valor_default(regex.sub('', qtd_nao_gostei_youtube_srt), '0'))

            dt_publicacao_str = response.css(".watch-time-text::text")[0].extract();

            import datetime

            dt_publicacao_str = re.sub('\w+\son\s', '', dt_publicacao_str)

            dt_publicacao = datetime.datetime.strptime(dt_publicacao_str, '%b %d, %Y')
            data_atual = datetime.datetime.today()
            delta = data_atual - dt_publicacao

            dias = delta.days

            yield Musica(_id=registro_mongo['_id'],
                         dt_insercao=registro_mongo['dt_insercao'],
                         estilo=registro_mongo['estilo'],
                         nome=registro_mongo['nome'],
                         artista=registro_mongo['artista'],
                         tom=registro_mongo['tom'],
                         possui_tabs=registro_mongo['possui_tabs'],
                         possui_capo=registro_mongo['possui_capo'],
                         capo=registro_mongo['capo'],
                         seq_acordes=registro_mongo['seq_acordes'],
                         qtd_exibicoes_cifraclub=registro_mongo['qtd_exibicoes_cifraclub'],
                         url_cifraclub=registro_mongo['url_cifraclub'],
                         linhas_html_cifraclub=registro_mongo['linhas_html_cifraclub'],
                         url_busca_youtube=registro_mongo['url_busca_youtube'],
                         url_video_youtube=response.url,
                         qtd_exibicoes_youtube=qtd_exibicoes_youtube,
                         qtd_gostei_youtube=qtd_gostei_youtube,
                         qtd_nao_gostei_youtube=qtd_nao_gostei_youtube,
                         dt_publicacao_youtube=dt_publicacao,
                         dias_desde_publicacao_youtube=dias)

        except BaseException as exc:
            scrapy.log.msg("Erro ao processar a url <%s>. Detalhes: %s..." % (response.url, exc),
                           loglevel=scrapy.log.ERROR, logstdout=None)