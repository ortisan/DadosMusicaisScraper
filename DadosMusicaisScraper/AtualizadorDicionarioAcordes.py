# -*- coding: utf-8 -*-
__author__ = 'marcelo'

from utils import *

client = MongoClient(MONGODB_URI)
db = client[MONGODB_DATABASE]
colecao_dicionario = db[MONGODB_COLLECTION_DA]

import logging

LOG_FILENAME = 'atualizador_dicionario_acordes.log'
logging.basicConfig(filename=LOG_FILENAME, filemode='w', level=logging.ERROR)

# TODO Talvez tenha que trazer o tom, caso haja diferencas entre os acordes e os acordes especificos do tom.

def traduzir_acordes(registros):
    for registro in registros:
        id = registro['_id']
        desenho_acorde = None
        if 'desenho_acorde' in registro:
            desenho_acorde = registro['desenho_acorde']
        try:
            acorde21, desenho_acorde, lista_idx_notas, lista_notas, foi_sucesso, mensagem = obter_acorde21_desenho_listanotas_idxnotas(
                id, desenho_acorde)
            dictUpdate = {"desenho_acorde": desenho_acorde, "lista_idx_notas": lista_idx_notas,
                          "lista_notas": lista_notas,
                          "foi_sucesso": foi_sucesso, "mensagem": mensagem}

        except BaseException as exc:
            dictUpdate = {"desenho_acorde": desenho_acorde, "lista_idx_notas": [], "lista_notas": [],
                          "foi_sucesso": False, "mensagem": mensagem}

            logging.error("Erro ao processar o registro <%s>. Detalhes: %s..." % (id, exc))

        finally:
            colecao_dicionario.update({"_id": id}, {'$set': dictUpdate}, upsert=True)


if __name__ == "__main__":

    query = {"$or": [{"foi_sucesso": {"$exists": 0}}, {"foi_sucesso": False}]}
    fields = {"_id": 1, "desenho_acorde": 1}
    # query = {"foi_sucesso": True}
    # query = {}
    qtd_registros = colecao_dicionario.find(query, fields).count()
    registros = colecao_dicionario.find(query, fields)

    import concurrent.futures

    qtd_registros_por_thread = 50
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        for i in range(0, qtd_registros, qtd_registros_por_thread):
            idx = 0
            lista_processar = []
            for registro in registros:
                lista_processar.append(registro)
                idx += 1
                if idx >= qtd_registros_por_thread:
                    break

            executor.submit(traduzir_acordes, lista_processar)
