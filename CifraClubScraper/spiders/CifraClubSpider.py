__author__ = 'marcelo'

import scrapy
from scrapy.http import Request
from urlparse import urljoin
from urlparse import urlparse
from urlparse import urlsplit
from urlparse import urlunsplit

# TODO persistir os dados

class CifraClubSpider(scrapy.Spider):
    name='cifraclub'
    allwed_domains = ['cifraclub.com.br']
    start_urls = ['http://www.cifraclub.com.br/estilos/']

    def parse(self, response):

        for a_estilo in response.css('.lista_estilos li a'):
            href_estilo = a_estilo.css('::attr(href)')[0].extract()
            nome_estilo = a_estilo.css('::text')[0].extract()
            print(href_estilo, nome_estilo)

            yield Request(urljoin(response.url, href_estilo),
                    callback=self.parse_musicas_do_estilo)

    def parse_musicas_do_estilo(self, response):
        for a_musicas in response.css('ol.top.spr1 li a'):
            href_musica = a_musicas.css('::attr(href)')[0].extract()
            musica = a_musicas.css('strong.top-txt_primary::text')[0].extract()
            artista = a_musicas.css('strong.top-txt_secondary::text')[0].extract()
            qtd_exibicoes = a_musicas.css('small::text')[0].extract()

            print(href_musica, musica , artista, qtd_exibicoes)

            scheme, netloc, path, query, fragment = urlsplit(response.url)
            path = href_musica
            query = ''
            url_musica = urlunsplit((scheme, netloc, path, query, fragment))
            yield Request(url_musica, callback=self.parse_musicas)

    def parse_musicas(self, response):

        div_cifra = response.css('#cifra_cnt')
        qtd_exibicoes = response.css('#v_exibicoes b::text').extract()

        tom = div_cifra.css('pre#ct_tom_cifra a#cifra_troca_tom::text').extract()
        acordes = div_cifra.css('pre#ct_cifra b::text').extract()
        print(qtd_exibicoes)




