# -*- coding: utf-8 -*-
__author__ = 'marcelo'

from urlparse import urljoin
from urlparse import urlsplit
from urlparse import urlunsplit
import datetime

import scrapy
from scrapy.http import Request
from scrapy.selector import Selector
from selenium import webdriver
from scrapy import log

from DadosMusicaisScraper.utils import *
from DadosMusicaisScraper.items import Musica


class MusicasPorEstiloCifraClubSpider(scrapy.Spider):
    name = 'MusicasPorEstiloCifraClubSpider'
    allwed_domains = ['cifraclub.com.br']
    start_urls = ['http://www.cifraclub.com.br/estilos/']

    def __init__(self):
        self.driver_cifra = webdriver.Firefox()


    def parse(self, response):
        for a_estilo in response.css('.lista_estilos li a'):
            try:
                href_estilo = a_estilo.css('::attr(href)')[0].extract()
                nome_estilo = a_estilo.css('::text')[0].extract()

                scrapy.log.msg(">> Estilo <%s (%s)> sera processado..." % (nome_estilo, href_estilo),
                               level=scrapy.log.INFO)

                self.driver_cifra.get(urljoin(response.url, href_estilo))

                qtd_clicks_bt_mais_musicas = 4

                while qtd_clicks_bt_mais_musicas > 1:
                    bt_mais_musicas = self.driver_cifra.find_element_by_css_selector("button.btn_full")
                    if bt_mais_musicas and bt_mais_musicas.is_displayed():
                        bt_mais_musicas.click()
                        self.driver_cifra.implicitly_wait(1)
                        qtd_clicks_bt_mais_musicas = qtd_clicks_bt_mais_musicas - 1
                    else:
                        break

                lista_musicas = self.driver_cifra.find_element_by_css_selector("ol.top.spr1").get_attribute('innerHTML')

                for a_musicas in Selector(text=lista_musicas).css('li a'):
                    href_musica = a_musicas.css('::attr(href)')[0].extract()
                    nome_musica = a_musicas.css('strong.top-txt_primary::text')[0].extract()
                    artista = a_musicas.css('strong.top-txt_secondary::text')[0].extract()

                    scrapy.log.msg(">> Musica <%s - %s (%s)> sera lida..." % (artista, nome_musica, href_musica),
                                   level=scrapy.log.INFO)

                    scheme, netloc, path, query, fragment = urlsplit(response.url)
                    path = href_musica
                    query = ''
                    url_musica = urlunsplit((scheme, netloc, path, query, fragment))

                    ## TRANSPORTA DADOS PARA O PROXIMO CALLBACK
                    request = Request(url_musica, callback=self.parse_musicas)
                    request.meta['estilo'] = nome_estilo
                    request.meta['nome'] = nome_musica
                    request.meta['artista'] = artista
                    yield request

            except BaseException as exc:
                scrapy.log.msg("Erro ao processar o estilo <%s>. Detalhes: %s..." % (nome_estilo, exc),
                               loglevel=scrapy.log.ERROR, logstdout=None)


    def parse_musicas(self, response):

        scrapy.log.msg(">> Musica <(%s)> lida..." % (response.url),
                       level=scrapy.log.INFO)

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
        nome_musica = response.meta['nome']
        artista = response.meta['artista']
        estilo = response.meta['estilo']
        # import hashlib
        # hashlib.sha224(artista + ' - ' + nome_musica).hexdigest()
        _id = artista + ' - ' + nome_musica

        yield Musica(_id=_id,
                     dt_insercao=datetime.datetime.today(),
                     estilo_cifraclub=estilo,
                     nome=nome_musica,
                     artista=artista,
                     tom_cifraclub=tom,
                     possui_tabs_cifraclub=possui_tabs,
                     possui_capo_cifraclub=possui_capo,
                     capo_cifraclub=capo,
                     seq_acordes_cifraclub=seq_acordes,
                     qtd_exibicoes_cifraclub=qtd_exibicoes_cifraclub,
                     url_cifraclub=response.url,
                     linhas_html_cifraclub=linhas_html_cifra)
