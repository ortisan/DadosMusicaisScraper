__author__ = 'marcelo'

import concurrent.futures
from pymongo import MongoClient
import scrapy
from scrapy import log

from utils import *

from DadosMusicaisScraper.settings import *


client = MongoClient(MONGODB_URI)
db = client[MONGODB_DATABASE]
colecao = db[MONGODB_COLLECTION]


def normalizar_dados_cifras(idx, qtd):
    # TODO Talvez tenha que trazer o tom, caso haja diferencas entre os acordes e os acordes especificos do tom.
    registros = colecao.find({}, {'_id': True, "seq_acordes_brutos": True, "capo": True}).skip(idx).limit(qtd)

    for registro in registros:

        try:
            id = registro['_id']

            seq_acordes_brutos = registro['seq_acordes_brutos']
            capo = registro['capo']

            acordes_unicos, tonicas, modos = obter_unicos_tonicas_baixos_modos(seq_acordes_brutos, capo)

            dictUpdate = {"acordes_unicos": acordes_unicos,
                          "tonicas": tonicas,
                          "modos": modos}

            # atualizamos o registro com os dados dos ratings do youtube.
            colecao.update({"_id": id}, {'$set': dictUpdate})

        except BaseException as exc:
            scrapy.log.msg("Erro ao processar o registro <%s>. Detalhes: %s..." % ((str(registro)), exc),
                           loglevel=scrapy.log.ERROR, logstdout=None)


if __name__ == "__main__":
    qtd_registros = colecao.count()

    with concurrent.futures.ProcessPoolExecutor(max_workers=3) as executor:
        for i in range(0, qtd_registros, 50):
            executor.submit(normalizar_dados_cifras, i, 50)
