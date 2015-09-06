__author__ = 'marcelo'

from DadosMusicaisScraper.utils import *

client = MongoClient(MONGODB_URI)
db = client[MONGODB_DATABASE]
colecao = db[MONGODB_COLLECTION]
colecao_sna = db['SNA']

import logging as log_atualizador

LOG_FILENAME = 'atualizador_cifras.log'
log_atualizador.basicConfig(filename=LOG_FILENAME, filemode='w', level=log_atualizador.ERROR)


def normalizar_dados_cifras(registros):
    for registro in registros:
        id = registro['_id']
        try:
            seq_acordes = registro['seq_acordes_cifraclub']
            capo = registro['capo_cifraclub']

            # Removo os duplicados.
            # set_acordes_str = set(seq_acordes)

            chords = []

            for acorde_str in seq_acordes:
                try:
                    logging.info(u"Obtendo dados do acorde <%s>..." % acorde_str)
                    acorde_21 = obter_acorde_music21(acorde_str, capo, False)
                    chords.append(acorde_21.pitchedCommonName)
                except BaseException as exc:
                    logging.error(u"Erro ao traduzir o acorde: <%s>. Detalhes: %s" % (acorde_str, exc))
                    # raise exc

            dict_update = {'acordes': chords}

            # atualizamos o registro com os dados dos acordes.
            colecao_sna.update({"_id": id}, {'$set': dict_update}, upsert=True)

        except BaseException as exc:
            log_atualizador.error("Erro ao processar o registro <%s>. Detalhes: %s..." % (id, exc))


if __name__ == '__main__':

    carregar_dicionario_acordes()

    query = {"$and": [{"seq_acordes_cifraclub": {'$exists': 1}},
                      {"$where": "this.seq_acordes_cifraclub.length > 0"}]}

    fields = {'_id': True, "seq_acordes_cifraclub": True, "capo_cifraclub": True}

    registros = colecao.find(query, fields)

    qtd_registros = colecao.find(query, {'_id': True}).count()

    import concurrent.futures

    qtd_registros_por_thread = 50
    idx = 0

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
