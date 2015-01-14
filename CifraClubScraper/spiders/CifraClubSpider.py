__author__ = 'marcelo'

from urlparse import urljoin
from urlparse import urlsplit
from urlparse import urlunsplit

import scrapy
from scrapy.http import Request

from CifraClubScraper.items import Musica


class CifraClubSpider(scrapy.Spider):
    name = 'cifraclub'
    allwed_domains = ['cifraclub.com.br']
    start_urls = ['http://www.cifraclub.com.br/estilos/']
    # CLASS CAPO: info_capo_cifra

    def parse(self, response):

        for a_estilo in response.css('.lista_estilos li a'):
            href_estilo = a_estilo.css('::attr(href)')[0].extract()
            nome_estilo = a_estilo.css('::text')[0].extract()
            print(href_estilo, nome_estilo)
            request = Request(urljoin(response.url, href_estilo),
                              callback=self.parse_musicas_do_estilo)
            request.meta['estilo'] = nome_estilo

            yield request


    def parse_musicas_do_estilo(self, response):
        for a_musicas in response.css('ol.top.spr1 li a'):
            href_musica = a_musicas.css('::attr(href)')[0].extract()
            musica = a_musicas.css('strong.top-txt_primary::text')[0].extract()
            artista = a_musicas.css('strong.top-txt_secondary::text')[0].extract()
            qtd_exibicoes = a_musicas.css('small::text')[0].extract()

            print(href_musica, musica, artista, qtd_exibicoes)

            scheme, netloc, path, query, fragment = urlsplit(response.url)
            path = href_musica
            query = ''
            url_musica = urlunsplit((scheme, netloc, path, query, fragment))

            request = Request(url_musica, callback=self.parse_musicas)
            request.meta['estilo'] = response.meta['estilo']
            request.meta['musica'] = musica
            request.meta['artista'] = artista
            request.meta['exibicoes'] = qtd_exibicoes

            yield request

    def parse_musicas(self, response):

        div_cifra = response.css('#cifra_cnt')
        # qtd_exibicoes = response.css('#v_exibicoes b::text').extract()

        tom = div_cifra.css('pre#ct_tom_cifra a#cifra_troca_tom::text').extract()
        acordes = div_cifra.css('pre#ct_cifra b::text').extract()

        print('$$$EXIBICOES....', response.meta['exibicoes'])

        yield Musica(estilo=response.meta['estilo'],
                     nome=response.meta['musica'],
                     artista=response.meta['artista'],
                     tom=tom,
                     acordes=acordes,
                     exibicoes=response.meta['exibicoes'],
                     url=response.url)