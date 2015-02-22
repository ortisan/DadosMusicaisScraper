# -*- coding: utf-8 -*-
__author__ = 'marcelo'

from pymongo import MongoClient
import scrapy
from scrapy import log

from DadosMusicaisScraper.settings import *


client = MongoClient(MONGODB_URI)
db = client[MONGODB_DATABASE]
colecao = db[MONGODB_COLLECTION]


def atualizar_qtd_acordes():
    registros = colecao.find({"qtd_acordes_cifraclub": {"$exists": 0}}, {'_id': True, "seq_acordes_cifraclub": True})

    for registro in registros:

        id = registro['_id']

        try:
            seq_acordes = registro['seq_acordes_cifraclub']
            set_acordes = set()
            set_acordes_add = set_acordes.add
            [x for x in seq_acordes if not (x in set_acordes or set_acordes_add(x))]
            qtd_acordes = len(set_acordes)
            dictUpdate = {"qtd_acordes_cifraclub": qtd_acordes}
            # atualizamos o registro com os dados dos ratings do youtube.
            colecao.update({"_id": id}, {'$set': dictUpdate})

        except BaseException as exc:
            scrapy.log.msg("Erro ao processar o registro <%s>. Detalhes: %s..." % (id, exc),
                           loglevel=scrapy.log.ERROR, logstdout=None)


if __name__ == "__main__":
    atualizar_qtd_acordes()
