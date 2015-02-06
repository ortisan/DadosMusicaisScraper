__author__ = 'marcelo'

import concurrent.futures
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from pymongo import MongoClient

from DadosMusicaisScraper.settings import *


client = MongoClient(MONGODB_URI)
db = client[MONGODB_DATABASE]
colecao = db[MONGODB_COLLECTION]


def atualizar_dados_rating_youtube(idx, qtd):
    registros = colecao.find({}, {'_id': True, "artista": True, "nome": True}).skip(idx).limit(qtd)

    driver_youtube = webdriver.Firefox()
    driver_youtube.get("http://youtube.com")

    for registro in registros:

        id = registro['_id']
        artista = registro['artista']
        musica = registro['nome']

        try:
            youtube_search_term = driver_youtube.find_element_by_id("masthead-search-term")
            youtube_search_term.clear()
            youtube_search_term.send_keys(artista + ' ' + musica)

            search = driver_youtube.find_element_by_id("search-btn")
            search.click()

            WebDriverWait(driver_youtube, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "ol#section-list"))
            )

            link_musica = driver_youtube.find_element_by_css_selector(
                "ol#section-list div.yt-lockup-video:nth-child(1) a")
            link_musica.click()

            WebDriverWait(driver_youtube, 10).until(
                EC.presence_of_element_located((By.ID, "watch-header"))
            )

            qtd_exibicoes_youtube_str = driver_youtube.find_element_by_css_selector(
                "#watch-header .watch-view-count").text
            qtd_exibicoes_youtube = qtd_exibicoes_youtube_str.replace(".", "")

            qtd_gostei_youtube_str = driver_youtube.find_element_by_css_selector(
                "#watch-header #watch-like-dislike-buttons span:nth-child(1)").text
            qtd_gostei_youtube = qtd_gostei_youtube_str.replace(".", "")

            qtd_nao_gostei_youtube_srt = driver_youtube.find_element_by_css_selector(
                "#watch-header #watch-like-dislike-buttons span:nth-child(2)").text
            qtd_nao_gostei_youtube = qtd_nao_gostei_youtube_srt.replace(".", "")

            dictUpdate = {"exibicoes_youtube": qtd_exibicoes_youtube,
                          "qtd_gostei_youtube": qtd_gostei_youtube,
                          "qtd_nao_gostei_youtube": qtd_nao_gostei_youtube}

            # atualizamos o registro com os dados dos ratings do youtube.
            colecao.update({"_id": id}, {'$set': dictUpdate})

        except BaseException as exc:
            print exc

    driver_youtube.close()


if __name__ == "__main__":
    qtd_registros = colecao.count()

    with concurrent.futures.ProcessPoolExecutor(max_workers=3) as executor:
        for i in range(0, qtd_registros, 50):
            executor.submit(atualizar_dados_rating_youtube, i, 50)

