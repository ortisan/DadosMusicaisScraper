# -*- coding: utf-8 -*-
__author__ = 'marcelo'

from urlparse import urlsplit
from urlparse import urlunsplit
import datetime

import scrapy
from scrapy.http import Request
from scrapy import log
from pymongo import MongoClient

from DadosMusicaisScraper.utils import *
from DadosMusicaisScraper.items import Musica
from DadosMusicaisScraper.settings import *


class MusicasPorArtistaCifraClubSpider(scrapy.Spider):
    name = 'MusicasPorArtistaCifraClubSpider'
    allwed_domains = ['cifraclub.com.br']
    start_urls = ['http://www.cifraclub.com.br']

    def __init__(self):
        client = MongoClient(MONGODB_URI)
        db = client[MONGODB_DATABASE]
        self.colecao = db[MONGODB_COLLECTION]


    def parse(self, response):

        registros_mongo = self.colecao.find({}, {'url_cifraclub': 1, 'estilo': 1})

        artistas_ja_processados = []

        for registro_mongo in registros_mongo:
            url_musica_cifraclub = registro_mongo['url_cifraclub']
            scheme, netloc, path, query, fragment = urlsplit(url_musica_cifraclub)
            artista = path.split('/')[1]

            if not artista in artistas_ja_processados:
                artistas_ja_processados.append(artista)
            else:
                continue

            path = artista
            query = ''
            url_musicas_artista = urlunsplit((scheme, netloc, path, query, fragment))
            request = Request(url_musicas_artista, callback=self.parse_listagem_musicas_artista)
            ## TRANSPORTA DADOS PARA O PROXIMO CALLBACK
            request.meta['estilo'] = registro_mongo['estilo']

            yield request


    def parse_listagem_musicas_artista(self, response):

        for a_musica in response.css('li a.a_vio'):
            href_musica = a_musica.css('::attr(href)')[0].extract()

            scheme, netloc, path, query, fragment = urlsplit(response.url)
            path = href_musica
            query = ''
            url_musica = urlunsplit((scheme, netloc, path, query, fragment))

            ## TRANSPORTA DADOS PARA O PROXIMO CALLBACK
            request = Request(url_musica, callback=self.parse_musicas)
            request.meta['estilo'] = response.meta['estilo']
            yield request


    def parse_musicas(self, response):

        scrapy.log.msg(">> Musica <(%s)> lida..." % (response.url),
                       level=scrapy.log.INFO)

        nome_musica = response.css('#ai_musica::text')[0].extract()
        artista = response.css('#ai_artista a::text')[0].extract()
        qtd_exibicoes_cifraclub_str = response.css('#v_exibicoes')[0].extract()
        regex = re.compile(r'[^0-9]*')
        qtd_exibicoes_cifraclub = int(obter_valor_default(regex.sub('', qtd_exibicoes_cifraclub_str), '0'))

        div_cifra = response.css('#cifra_cnt')

        linhas_html_cifra = div_cifra[0].extract().replace('\t', '').replace('\r', '').split('\n')

        tom_txt = div_cifra.css('pre#ct_tom_cifra a#cifra_troca_tom::text')
        tom = None
        if len(tom_txt) > 0:
            tom = tom_txt[0].extract()

        seq_acordes = div_cifra.css('pre#ct_cifra b::text').extract()

        capo_txt = div_cifra.css('pre#ct_tom_cifra span#info_capo_cifra a::text')
        capo = 0
        if len(capo_txt) > 0:
            capo = int(re.search('(\d+)', capo_txt[0].extract()).group(0))

        possui_capo = capo > 0
        possui_tabs = len(div_cifra.css('span.tablatura')) > 0
        estilo = response.meta['estilo']
        # import hashlib
        # hashlib.sha224(artista + ' - ' + nome_musica).hexdigest()
        _id = artista + ' - ' + nome_musica

        yield Musica(_id=_id,
                     dt_insercao=datetime.datetime.today(),
                     estilo=estilo,
                     nome=nome_musica,
                     artista=artista,
                     tom=tom,
                     possui_tabs=possui_tabs,
                     possui_capo=possui_capo,
                     capo=capo,
                     seq_acordes=seq_acordes,
                     qtd_exibicoes_cifraclub=qtd_exibicoes_cifraclub,
                     url_cifraclub=response.url,
                     linhas_html_cifraclub=linhas_html_cifra)


if __name__ == '__main__':
    url = 'http://www.cifraclub.com.br/banda-ego/juro/'
    scheme, netloc, path, query, fragment = urlsplit(url)

    path = path.split('/')[1]

    query = ''

    url_musicas_artista = urlunsplit((scheme, netloc, path, query, fragment))

    print url
