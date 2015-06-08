# -*- coding: utf-8 -*-
__author__ = 'marcelo'

from pymongo import MongoClient

from DadosMusicaisScraper.settings import *

client = MongoClient(MONGODB_URI)
db = client[MONGODB_DATABASE]
colecao = db[MONGODB_COLLECTION]
CLIENT_ID = SPOTIFY_CLIENT_ID
CLIENT_SECRET = SPOTIFY_CLIENT_SECRET

import spotipy.oauth2

auth = spotipy.oauth2.SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
token = auth.get_access_token()

scope = 'user-library-read'

qtd_nao_processados = 0


def obter_dados_spotify(registros):
    for registro in registros:
        duracao = -1
        popularidade = -1
        url_musica = ""

        try:
            id = registro["_id"]
            artista = registro['artista']
            nome = registro['nome']

            import spotipy

            spotify = spotipy.Spotify(token)
            results = spotify.search(q='artist:' + artista + ' track:' + nome, type='track', limit=1)
            if len(results['tracks']) > 0 and len(results['tracks']['items']):
                duracao = results['tracks']['items'][0]['duration_ms']
                popularidade = results['tracks']['items'][0]['popularity']
                url_musica = results['tracks']['items'][0]['external_urls']['spotify']

        except BaseException as exc:
            # TODO LOGAR OS QUE NAO FORAM ENCONTRADOS.
            global qtd_nao_processados
            qtd_nao_processados = qtd_nao_processados + 1
            print exc

        dictUpdate = {"duracao_spotify": duracao,
                      "popularidade_spotify": popularidade,
                      "url_spotify": url_musica}
        # atualizamos o registro com os dados do spotify
        colecao.update({"_id": id}, {'$set': dictUpdate})


if __name__ == "__main__":
    qtd_registros = colecao.find({"$or": [{"duracao_spotify": {"$exists": 0}}, {"duracao_spotify": -1}]},
                                 {'_id': True, "artista": True, "nome": True}).count()

    #registros = colecao.find({"duracao_spotify": {'$exists': 0}}, {'_id': True, "artista": True, "nome": True})
    registros = colecao.find({"duracao_spotify": -1}, {'_id': True, "artista": True, "nome": True})

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

            executor.submit(obter_dados_spotify, lista_processar)
