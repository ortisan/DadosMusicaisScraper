__author__ = 'marcelo'

from urlparse import urljoin
from urlparse import urlsplit
from urlparse import urlunsplit
import re

import scrapy
from scrapy.http import Request
from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scrapy import log

from CifraClubScraper.items import Musica


scrapy.log.start(logfile="cifraclub.log", loglevel=scrapy.log.INFO, logstdout=None)


class CifraClubSpider(scrapy.Spider):
    name = 'cifraclub'
    allwed_domains = ['cifraclub.com.br']
    start_urls = ['http://www.cifraclub.com.br/estilos/']
    driver_cifra = webdriver.Firefox()
    ## USO DOIS DRIVERS PELA PERFORMANCE DE ABERTURA DAS PAGINAS
    driver_youtube = webdriver.Firefox()
    driver_youtube.get('http://www.youtube.com')
    notas = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']
    notas_bemois = ['A', 'Bb', 'B', 'C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab']
    # CLASS CAPO: info_capo_cifra

    def parse(self, response):
        for a_estilo in response.css('.lista_estilos li a'):
            href_estilo = a_estilo.css('::attr(href)')[0].extract()
            nome_estilo = a_estilo.css('::text')[0].extract()

            CifraClubSpider.driver_cifra.get(urljoin(response.url, href_estilo))

            qtd_clicks_bt_mais_musicas = 4

            while qtd_clicks_bt_mais_musicas > 1:
                bt_mais_musicas = CifraClubSpider.driver_cifra.find_element_by_css_selector("button.btn_full")
                if bt_mais_musicas and bt_mais_musicas.is_displayed():
                    bt_mais_musicas.click()
                    CifraClubSpider.driver_cifra.implicitly_wait(1)
                    qtd_clicks_bt_mais_musicas = qtd_clicks_bt_mais_musicas - 1
                else:
                    break

            lista_musicas = CifraClubSpider.driver_cifra.find_element_by_css_selector("ol.top.spr1").get_attribute(
                'innerHTML')
            Selector(text=lista_musicas)

            for a_musicas in Selector(text=lista_musicas).css('li a'):
                href_musica = a_musicas.css('::attr(href)')[0].extract()
                musica = a_musicas.css('strong.top-txt_primary::text')[0].extract()
                artista = a_musicas.css('strong.top-txt_secondary::text')[0].extract()
                qtd_exibicoes_cifraclub = a_musicas.css('small::text')[0].extract()

                scheme, netloc, path, query, fragment = urlsplit(response.url)
                path = href_musica
                query = ''
                url_musica = urlunsplit((scheme, netloc, path, query, fragment))

                ## TRANSPORTA DADOS PARA O PROXIMO CALLBACK
                request = Request(url_musica, callback=self.parse_musicas)
                request.meta['estilo'] = nome_estilo
                request.meta['musica'] = musica
                request.meta['artista'] = artista
                request.meta['exibicoes_cifraclub'] = qtd_exibicoes_cifraclub
                yield request


    def parse_musicas(self, response):
        html = response.body

        div_cifra = response.css('#cifra_cnt')

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

        possui_tabs = len(div_cifra.css('span.tablatura')) > 0

        musica = response.meta['musica']
        artista = response.meta['artista']

        ## IMPORTA DADOS DO YOUTUBE
        try:
            youtube_search_term = CifraClubSpider.driver_youtube.find_element_by_id("masthead-search-term")
            youtube_search_term.clear()
            youtube_search_term.send_keys(artista + ' ' + musica)

            search = CifraClubSpider.driver_youtube.find_element_by_id("search-btn")
            search.click()

            results_youtube = WebDriverWait(CifraClubSpider.driver_youtube, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "ol#section-list"))
            )

            CifraClubSpider.driver_youtube.find_element_by_css_selector("#search-btn")

            # visualizacoes = CifraClubSpider.driver_youtube.find_element_by_css_selector(".yt-lockup-content .yt-lockup-meta-info li:nth-child(2)")
            # m = re.search('(\d+\.*)+', visualizacoes.text)
            # qtd_exibicoes_youtube = m.group(0)

            link_musica = CifraClubSpider.driver_youtube.find_element_by_css_selector(
                "ol#section-list div.yt-lockup-video:nth-child(1) a")
            link_musica.click()

            results_youtube = WebDriverWait(CifraClubSpider.driver_youtube, 10).until(
                EC.presence_of_element_located((By.ID, "watch-header"))
            )

            qtd_exibicoes_youtube_str = CifraClubSpider.driver_youtube.find_element_by_css_selector(
                "#watch-header .watch-view-count").text
            qtd_exibicoes_youtube = qtd_exibicoes_youtube_str.replace(".", "")

            qtd_gostei_youtube_str = CifraClubSpider.driver_youtube.find_element_by_css_selector(
                "#watch-header #watch-like-dislike-buttons span:nth-child(1)").text
            qtd_gostei_youtube = qtd_gostei_youtube_str.replace(".", "")

            qtd_nao_gostei_youtube_srt = CifraClubSpider.driver_youtube.find_element_by_css_selector(
                "#watch-header #watch-like-dislike-buttons span:nth-child(2)").text
            qtd_nao_gostei_youtube = qtd_nao_gostei_youtube_srt.replace(".", "")

            yield Musica(estilo=response.meta['estilo'],
                         nome=musica,
                         artista=artista,
                         tom=tom,
                         acordes=acordes,
                         exibicoes_cifraclub=response.meta['exibicoes_cifraclub'],
                         exibicoes_youtube=qtd_exibicoes_youtube,
                         qtd_gostei_youtube=qtd_gostei_youtube,
                         qtd_nao_gostei_youtube=qtd_nao_gostei_youtube,
                         url=response.url,
                         possui_tabs=possui_tabs,
                         url_cifraclub = response.url,
                         url_youtube = CifraClubSpider.driver_youtube.current_url,
                         html=html)

        except BaseException as exc:
            scrapy.log.msg("Erro ao obter dados da musica: %s - %s. \nDetalhes: %s" % (artista, musica, exc),
                           level=scrapy.log.ERROR, spider=CifraClubSpider)

