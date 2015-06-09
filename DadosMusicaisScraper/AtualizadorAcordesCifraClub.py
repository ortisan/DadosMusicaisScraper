# -*- coding: utf-8 -*-
__author__ = 'marcelo'

from pymongo import MongoClient

from DadosMusicaisScraper.settings import *
from utils import *

client = MongoClient(MONGODB_URI)
db = client[MONGODB_DATABASE]
colecao = db[MONGODB_COLLECTION]

import logging

LOG_FILENAME = 'atualizador.log'
logging.basicConfig(filename=LOG_FILENAME,
                    level=logging.ERROR)

# TODO Talvez tenha que trazer o tom, caso haja diferencas entre os acordes e os acordes especificos do tom.

def normalizar_dados_cifras(registros):

    for registro in registros:
        id = registro['_id']
        try:
            seq_acordes = registro['seq_acordes_cifraclub']
            capo = registro['capo_cifraclub']
            unicos, tonicas, modos = obter_novos_unicos_tonicas_baixos_modos(seq_acordes, capo)
            dictUpdate = {"acordes_unicos_cifraclub": unicos,
                          "tonicas_cifraclub": tonicas,
                          "modos_cifraclub": modos}
            # atualizamos o registro com os dados dos ratings do youtube.
            colecao.update({"_id": id}, {'$set': dictUpdate})

        except BaseException as exc:
            logging.error("Erro ao processar o registro <%s>. Detalhes: %s..." % (id, exc))


if __name__ == "__main__":

    query = {"$and": [{"acordes_unicos_cifraclub": {"$exists": 0}},
                                           {"seq_acordes_cifraclub": {'$exists': 1}},
                                           {"$where": "this.seq_acordes_cifraclub.length > 0"}]}
    # Busca os registros que nao possuem dados do lastfm
    qtd_registros = colecao.find(query, {'_id': True}).count()

    registros = colecao.find(query, {'_id': True, "seq_acordes_cifraclub": True, "capo_cifraclub": True})
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

            executor.submit(normalizar_dados_cifras, lista_processar)
