__author__ = 'marcelo'

from urlparse import urljoin
from urlparse import urlsplit
from urlparse import urlunsplit
import re

import scrapy
from scrapy.http import Request
from selenium import webdriver

from CifraClubScraper.items import Musica


class CifraClubSpider(scrapy.Spider):
    name = 'cifraclub'
    allwed_domains = ['cifraclub.com.br']
    start_urls = ['http://www.cifraclub.com.br/estilos/']
    driver = webdriver.Firefox()
    driver.get("http://www.youtube.com")
    notas = ['A', 'A#', 'B', 'C','C#', 'D','D#', 'E', 'F', 'F#', 'G', 'G#']
    notas_bemois = ['A', 'Bb', 'B', 'C','Db', 'D','Eb', 'E', 'F', 'Gb', 'G', 'Ab']
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
            qtd_exibicoes_cifraclub = a_musicas.css('small::text')[0].extract()

            print(href_musica, musica, artista, qtd_exibicoes_cifraclub)

            scheme, netloc, path, query, fragment = urlsplit(response.url)
            path = href_musica
            query = ''
            url_musica = urlunsplit((scheme, netloc, path, query, fragment))

            ## IMPORTA DADOS DO YOUTUBE

            # youtube_search_term = CifraClubSpider.driver.find_element_by_id("masthead-search-term")
            # youtube_search_term.clear()
            # youtube_search_term.send_keys(artista + ' ' + musica)
            #
            # search = CifraClubSpider.driver.find_element_by_id("search-btn")
            # search.click()
            #
            # results_youtube = WebDriverWait(CifraClubSpider.driver, 10).until(
            # EC.presence_of_element_located((By.ID, "results"))
            # )
            #
            # CifraClubSpider.driver.find_element_by_id("search-btn")
            # CifraClubSpider.driver.find_element_by_css_selector("#results li")
            #
            # visualizacoes = CifraClubSpider.driver.find_element_by_css_selector(".yt-lockup-content .yt-lockup-meta-info li:nth-child(2)")
            # m = re.search('(\d+\.*)+', visualizacoes.text)
            # qtd_exibicoes_youtube = m.group(0)

            ## TRANSPORTA DADOS PARA O PROXIMO CALLBACK

            qtd_exibicoes_youtube = 0

            request = Request(url_musica, callback=self.parse_musicas)
            request.meta['estilo'] = response.meta['estilo']
            request.meta['musica'] = musica
            request.meta['artista'] = artista
            request.meta['exibicoes_cifraclub'] = qtd_exibicoes_cifraclub
            request.meta['exibicoes_youtube'] = qtd_exibicoes_youtube

            yield request

    def parse_musicas(self, response):
        div_cifra = response.css('#cifra_cnt')

        # span.tablatura

        tom_txt = div_cifra.css('pre#ct_tom_cifra a#cifra_troca_tom::text')
        tom = None
        if len(tom_txt) > 0:
            tom = tom_txt[0].extract()

        acordes = div_cifra.css('pre#ct_cifra b::text').extract()

        capo = None

        capo_txt = div_cifra.css('pre#ct_tom_cifra span#info_capo_cifra a::text')
        if len(capo_txt) > 0:
            capo = int(re.search('(\d+)', capo_txt[0].extract()).group(0))
            novos_acordes = []
            for acorde in acordes:
                idx_letra = 1
                notas = CifraClubSpider.notas
                if acorde.find("#") == 1:
                    idx_letra = 2
                if acorde.find("b") == 1:
                    idx_letra = 2
                    notas = CifraClubSpider.notas_bemois

                try:
                    idx = notas.index(acorde[0:idx_letra])
                    # Busco as notas
                    novo_acorde = notas[(capo + idx) % 12]
                    novos_acordes.append(novo_acorde + acorde[idx:])
                except BaseException as exc:
                    print exc

            acordes = novos_acordes

        yield Musica(estilo=response.meta['estilo'],
                     nome=response.meta['musica'],
                     artista=response.meta['artista'],
                     tom=tom,
                     acordes=acordes,
                     exibicoes_cifraclub=response.meta['exibicoes_cifraclub'],
                     exibicoes_youtube=response.meta['exibicoes_youtube'],
                     url=response.url)