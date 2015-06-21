# -*- coding: utf-8 -*-
__author__ = 'marcelo'

import logging as log_atualizador

from pymongo import MongoClient

from DadosMusicaisScraper.settings import *

LOG_FILENAME = 'atualizador_lasfm.log'
log_atualizador.basicConfig(filename=LOG_FILENAME, filemode='w',
                            level=log_atualizador.ERROR)

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

        id = registro["_id"]
        artista = registro['artista']
        nome = registro['nome']

        try:
            track = network.get_track(artista, nome)
            duracao = track.get_duration()
            qtd_audicoes = track.get_playcount()
            url_musica = track.get_url()
        except BaseException as exc:
            # TODO LOGAR OS QUE NAO FORAM ENCONTRADOS.
            global qtd_nao_processados
            qtd_nao_processados = qtd_nao_processados + 1
            log_atualizador.error("Erro ao processar o registro <%s>. Detalhes: %s..." % (id, exc))

        dictUpdate = {"duracao_lastfm": duracao,
                      "qtd_audicoes_lastfm": qtd_audicoes,
                      "url_lastfm": url_musica}

        # atualizamos o registro com os dados da lastfm.
        colecao.update({"_id": id}, {'$set': dictUpdate})


if __name__ == "__main__":
    # Busca os registros que nao possuem dados do lastfm

    query = {"$or": [{"duracao_lastfm": {'$exists': 0}}, {"duracao_lastfm": -1}]}
    fields = {'_id': True, "artista": True, "nome": True}
    qtd_registros = colecao.find(query, fields).count()
    registros = colecao.find(query, fields)
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
