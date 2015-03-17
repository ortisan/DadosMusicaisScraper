# -*- coding: utf-8 -*-
__author__ = 'marcelo'

from pymongo import MongoClient

from DadosMusicaisScraper.settings import *
from utils import *


client = MongoClient(MONGODB_URI)
db = client[MONGODB_DATABASE]
colecao_dicionario = db[MONGODB_COLLECTION_DA]

import logging

LOG_FILENAME = 'atualizador.log'
logging.basicConfig(filename=LOG_FILENAME,
                    level=logging.ERROR)

# TODO Talvez tenha que trazer o tom, caso haja diferencas entre os acordes e os acordes especificos do tom.


def traduzir_acordes(idx, qtd):
    registros = colecao_dicionario.find({"$or": [{"foi_sucesso": {"$exists": 0}}, {"foi_sucesso": False}]}).skip(        idx).limit(qtd)
    # registros = colecao_dicionario.find({"desenho_acorde": {"$exists": 0}}).skip(idx).limit(qtd)

    for registro in registros:
        id = registro['_id']

        try:

            # atualizamos o registro com os dados dos ratings do youtube.
            desenho_acorde, lista_idx_notas, foi_sucesso, mensagem = obter_desenho_lista_idx_notas(id)
            dictUpdate = {"desenho_acorde": desenho_acorde, "lista_idx_notas": lista_idx_notas,
                          "foi_sucesso": foi_sucesso, "mensagem": mensagem}

        except BaseException as exc:
            dictUpdate = {"desenho_acorde": desenho_acorde, "lista_idx_notas": [],
                          "foi_sucesso": False, "mensagem": mensagem}

            logging.error("Erro ao processar o registro <%s>. Detalhes: %s..." % (id, exc))

        finally:
            colecao_dicionario.update({"_id": id}, {'$set': dictUpdate}, upsert=True)


if __name__ == "__main__":
    # registros = colecao_dicionario.find({"desenho_acorde": {"$exists": 0}})
    #
    # qtd_registros = registros.count()

    traduzir_acordes(0, 10000)


    # colecao_dicionario = db["acordes_sucesso_erro"]
    #
    # erros = colecao_dicionario.find_one({"_id":False})['acordes']
    #
    # count_sim = 0
    # count_nao = 0
    #
    # for acorde in erros:
    # try:
    # desenho = obter_desenho_cifraclub(acorde)
    # print acorde, "SIM"
    #         count_sim = count_sim + 1
    #     except BaseException as exc:
    #         print acorde, "NAO"
    #         count_nao = count_nao + 1
    #
    #
    # print(count_sim, count_nao)


    # import concurrent.futures
    #
    # with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    #     for i in range(0, qtd_registros, 50):
    #         executor.submit(traduzir_acordes, i, 50)


