# -*- coding: utf-8 -*-
__author__ = 'marcelo'

from pymongo import MongoClient

from DadosMusicaisScraper.settings import *

network = pylast.LastFMNetwork(api_key=LASTFM_API_KEY, api_secret=LASTFM_API_SECRET, username=LASTFM_USERNAME,
                               password_hash=LASTFM_PASSWORD)

client = MongoClient(MONGODB_URI)
db = client[MONGODB_DATABASE]
colecao = db[MONGODB_COLLECTION]

qtd_nao_processados = 0


def obter_dados_last_fm(registros):
    for registro in registros:
        duracao = -1
        qtd_audicoes = -1
        url_musica = ""

        try:
            id = registro["_id"]
            artista = registro['artista']
            nome = registro['nome']
            track = network.get_track(artista, nome)
            duracao = track.get_duration()
            qtd_audicoes = track.get_playcount()
            url_musica = track.get_url()
        except BaseException as exc:
            # TODO LOGAR OS QUE NAO FORAM ENCONTRADOS.
            global qtd_nao_processados
            qtd_nao_processados = qtd_nao_processados + 1
            print exc

        dictUpdate = {"duracao_lastfm": duracao,
                      "qtd_audicoes_lastfm": qtd_audicoes,
                      "url_lastfm": url_musica}

        # atualizamos o registro com os dados dos ratings do youtube.
        colecao.update({"_id": id}, {'$set': dictUpdate})


if __name__ == "__main__":
    # Busca os registros que nao possuem dados do lastfm


    qtd_registros = colecao.find({"$or": [{"duracao_lastfm": {'$exists': 0}}, {"duracao_lastfm": -1}]},
                                 {'_id': True, "artista": True, "nome": True}).count()
    registros = colecao.find({"$or": [{"duracao_lastfm": {'$exists': 0}}, {"duracao_lastfm": -1}]},
                             {'_id': True, "artista": True, "nome": True})
    import concurrent.futures

    qtd_registros_por_thread = 50
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        for i in range(0, qtd_registros, qtd_registros_por_thread):
            idx = 0
            lista_processar = []
            for registro in registros:
                lista_processar.append(registro)
                idx = idx + 1
                if idx >= qtd_registros_por_thread:
                    break

            executor.submit(obter_dados_last_fm, lista_processar)
