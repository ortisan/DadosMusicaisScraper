# -*- coding: utf-8 -*-
__author__ = 'marcelo'

import datetime
from urlparse import urlsplit
from urlparse import urlunsplit

import scrapy
from scrapy.http import Request
from scrapy import log

from DadosMusicaisScraper.utils import *
from DadosMusicaisScraper.items import Musica


class MusicasEchordSpider(scrapy.Spider):
    name = 'MusicasEchordSpider'
    allwed_domains = ['e-chords.com/']
    start_urls = ['http://www.e-chords.com/music-genres']

    def __init__(self):
        pass

    def parse(self, response):
        for a_estilo in response.css('div.lista_artista h1 a'):
            try:
                href_estilo = a_estilo.css('::attr(href)')[0].extract()
                nome_estilo = a_estilo.css('::text')[0].extract()

                log.msg(">> Estilo <%s (%s)> sera processado..." % (nome_estilo, href_estilo),
                        level=log.INFO)

                ## TRANSPORTA DADOS PARA O PROXIMO CALLBACK
                request = Request(href_estilo, callback=self.parse_estilos)
                request.meta['estilo'] = nome_estilo
                yield request

            except BaseException as exc:
                log.msg("Erro ao processar o estilo <%s>. Detalhes: %s..." % (nome_estilo, exc),
                        loglevel=log.ERROR, logstdout=None)

    def parse_estilos(self, response):
        url_estilo = response.url

        log.msg(">> Estilo <(%s)> lido..." % (url_estilo),
                level=log.INFO)

        estilo = response.meta['estilo']

        for a_artista in response.css('table.pages td.alphabet p a'):
            try:
                href_artista = a_artista.css('::attr(href)')[0].extract()
                artista = a_artista.css('::text')[0].extract()

                scheme, netloc, path, query, fragment = urlsplit(url_estilo)
                path = href_artista
                query = ''
                url_artista = urlunsplit((scheme, netloc, path, query, fragment))

                log.msg(">> Artista <%s (%s)> sera processado..." % (artista, href_artista),
                        level=log.INFO)

                ## TRANSPORTA DADOS PARA O PROXIMO CALLBACK
                request = Request(url_artista, callback=self.parse_artista)
                request.meta['estilo'] = estilo
                request.meta['artista'] = artista

                yield request

            except BaseException as exc:
                log.msg("Erro ao processar o estilo <%s>. Detalhes: %s..." % (estilo, exc),
                        loglevel=log.ERROR, logstdout=None)

    def parse_artista(self, response):
        url_artista = response.url

        log.msg(">> Artista <(%s)> lido..." % (url_artista),
                level=log.INFO)

        estilo = response.meta['estilo']
        artista = response.meta['artista']

        for a_musica in response.css('ul#results p.itm a'):
            try:
                href_musica = a_musica.css('::attr(href)')[0].extract()
                musica = a_musica.css('::text')[0].extract()

                scheme, netloc, path, query, fragment = urlsplit(url_artista)
                path = href_musica
                query = ''
                url_musica = urlunsplit((scheme, netloc, path, query, fragment))

                log.msg(">> Musica <%s (%s)> sera processado..." % (musica, url_musica),
                        level=log.INFO)

                ## TRANSPORTA DADOS PARA O PROXIMO CALLBACK
                request = Request(url_musica, callback=self.parse_musicas)
                request.meta['estilo'] = estilo
                request.meta['artista'] = artista
                request.meta['nome'] = musica

                yield request

            except BaseException as exc:
                log.msg("Erro ao processar o estilo <%s>. Detalhes: %s..." % (estilo, exc),
                        loglevel=log.ERROR, logstdout=None)

    def parse_musicas(self, response):
        url_musica = response.url

        log.msg(">> Musica <(%s)> lida..." % (url_musica),
                level=log.INFO)

        estilo = response.meta['estilo']
        nome_musica = response.meta['nome']
        artista = response.meta['artista']

        _id = artista + ' - ' + nome_musica

        try:
            div_cifra = response.css('.coremain')
            html_div_cifra = div_cifra[0].extract()
            linhas_html_cifra = html_div_cifra.replace('\t', '').replace('\r', '').split('\n')

            tom_txt = response.css('div.tom .actualkey::text')
            tom = None
            if len(tom_txt) > 0:
                tom = tom_txt[0].extract()

            seq_acordes = div_cifra.css('u::text').extract()

            capo_txt = html_div_cifra[0: 200]
            capo = 0
            if "CAPO" in capo_txt:
                capo = int(re.search('CAPO (\d+)', capo_txt).group(1))
            possui_capo = capo > 0

            yield Musica(_id=_id,
                         dt_insercao=datetime.datetime.today(),
                         estilo=estilo,
                         nome=nome_musica,
                         artista=artista,
                         tom=tom,
                         possui_capo=possui_capo,
                         capo=capo,
                         seq_acordes=seq_acordes,
                         url_cifras=url_musica,
                         linhas_html_cifras=linhas_html_cifra,
                         processamento_cifras=True)

        except BaseException as exc:
            log.msg("Erro ao processar a musica <%s>. Detalhes: %s..." % (_id, exc),
                    loglevel=log.ERROR, logstdout=None)
            yield Musica(_id=_id,
                         dt_insercao=datetime.datetime.today(),
                         estilo=estilo,
                         nome=nome_musica,
                         url_cifras=url_musica,
                         artista=artista,
                         processamento_cifras=False)
