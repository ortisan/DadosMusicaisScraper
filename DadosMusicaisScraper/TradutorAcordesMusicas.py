# -*- coding: utf-8 -*-
__author__ = 'marcelo'

from pymongo import MongoClient

from DadosMusicaisScraper.settings import *
from utils import *


client = MongoClient(MONGODB_URI)
db = client[MONGODB_DATABASE]
colecao_musicas = db[MONGODB_COLLECTION]
colecao_dicionario = db[MONGODB_COLLECTION_DA]

import logging

LOG_FILENAME = 'atualizador.log'
logging.basicConfig(filename=LOG_FILENAME,
                    level=logging.ERROR)

# TODO Talvez tenha que trazer o tom, caso haja diferencas entre os acordes e os acordes especificos do tom.

acordes = {}

def traduzir_acordes_musicas(registros):
    for registro in registros:
        id = registro['_id']

        try:
            seq_acordes = registro["seq_acordes_cifraclub"]
            capo = registro["capo_cifraclub"]
            unicos = []
            modos = []
            tonicas = []
            baixos = []

            # flag_triades_maiores = []
            # flag_triades_menores = []
            # flag_sextas = []
            # flag_setimas = []
            # flag_aumentadas = []
            # flag_diminutas = []
            # flag_dominantes = []
            #
            # qtd_maiores = 0
            # qtd_menores = 0
            # qtd_sextas = 0
            # qtd_setimas = 0
            # qtd_aumentadas = 0
            # qtd_diminutas = 0
            # qtd_dominantes = 0

            for acorde in seq_acordes:
                obj_acorde = acordes[acorde]
                novo_idx_notas, novas_notas, acorde_21 = transpor_acorde(obj_acorde, capo)

                tonica = acorde_21.root().name
                novo_nome_acorde = tonica + " - " + acorde_21.commonName

                if novo_nome_acorde not in unicos:
                    unicos.append(novo_nome_acorde)
                    tonicas.append(tonica)
                    baixo = acorde_21.bass().name
                    baixos.append(baixo)
                    modos.append(acorde_21.commonName)

                    # eh_maior = acorde_21.isMajorTriad() or acorde_21.isIncompleteMajorTriad()
                    # if eh_maior:
                    #     qtd_maiores = qtd_maiores + 1
                    # flag_triades_maiores.append(eh_maior)
                    #
                    # eh_menor = acorde_21.isMinorTriad() or acorde_21.isIncompleteMinorTriad()
                    # if eh_menor:
                    #     qtd_menores = qtd_menores + 1
                    # flag_triades_menores.append(eh_menor)
                    #
                    # eh_sexta = acorde_21.isSwissAugmentedSixth()
                    # if eh_sexta:
                    #     qtd_sextas = qtd_sextas + 1
                    # flag_sextas.append(eh_sexta)
                    #
                    # eh_setima = acorde_21.isSeventh() or acorde_21.isDiminishedSeventh()
                    # if eh_setima:
                    #     qtd_setimas = qtd_setimas + 1
                    # flag_setimas.append(eh_setima)
                    #
                    # eh_aumentada = acorde_21.isAugmentedTriad()
                    # if eh_aumentada:
                    #     qtd_aumentadas = qtd_aumentadas + 1
                    # flag_aumentadas.append(eh_aumentada)
                    #
                    # eh_diminuta = acorde_21.isDiminishedTriad()
                    # if eh_diminuta:
                    #     qtd_diminutas = qtd_diminutas + 1
                    # flag_diminutas.append(eh_diminuta)
                    #
                    # eh_dominante = acorde_21.isDominantSeventh()
                    # if eh_dominante:
                    #     qtd_dominantes = qtd_dominantes + 1
                    # flag_dominantes.append(eh_dominante)

            dictUpdate = {"unicos_music21": unicos,
                          "tonicas_music21": tonicas,
                          "baixos_music21": baixos,
                          "modos_music21": modos,
                          # "flag_triades_maiores_music21": flag_triades_maiores,
                          # "flag_triades_menores_music21": flag_triades_menores,
                          # "flag_sextas_music21": flag_sextas,
                          # "flag_setimas_music21": flag_setimas,
                          # "flag_aumentadas_music21": flag_aumentadas,
                          # "flag_diminutas_music21": flag_diminutas,
                          # "flag_dominantes_music21": flag_dominantes,
                          # "qtd_triades_maiores_music21": qtd_maiores,
                          # "qtd_triades_menores_music21": qtd_menores,
                          # "qtd_sextas_music21": qtd_setimas,
                          # "qtd_setimas_music21": qtd_setimas,
                          # "qtd_aumentadas_music21": qtd_aumentadas,
                          # "qtd_diminutas_music21": qtd_diminutas,
                          # "qtd_dominantes_music21": qtd_dominantes,
                          "foi_sucesso_music21": True,
                          "mensagem": "Traducao com sucesso."}

        except BaseException as exc:
            dictUpdate = {"unicos_music21": [],
                          "tonicas_music21": [],
                          "baixos_music21": [],
                          "modos_music21": [],
                          # "flag_triades_maiores_music21": [],
                          # "flag_triades_menores_music21": [],
                          # "flag_sextas_music21": [],
                          # "flag_setimas_music21": [],
                          # "flag_aumentadas_music21": [],
                          # "flag_diminutas_music21": [],
                          # "flag_dominantes_music21": [],
                          # "qtd_triades_maiores_music21": 0,
                          # "qtd_triades_menores_music21": 0,
                          # "qtd_sextas_music21": 0,
                          # "qtd_setimas_music21": 0,
                          # "qtd_aumentadas_music21": 0,
                          # "qtd_diminutas_music21": 0,
                          # "qtd_dominantes_music21": 0,
                          "foi_sucesso_music21": False,
                          "mensagem": "Erro ao processar o registro <%s>. Detalhes: %s..." % (id, exc)}

            logging.error("Erro ao processar o registro <%s>. Detalhes: %s..." % (id, exc))

        finally:
            colecao_musicas.update({"_id": id}, {'$set': dictUpdate}, upsert=True)


if __name__ == "__main__":
    query = {}

    registros_acordes = colecao_dicionario.find(query)
    for registro in registros_acordes:
        acordes[registro["_id"]] = registro

    registros_musicas = colecao_musicas.find({"$where": "this.seq_acordes_cifraclub.length > 2"})

    qtd_registros = registros_musicas.count()

    import concurrent.futures

    qtd_registros_por_thread = 50
    with concurrent.futures.ProcessPoolExecutor(max_workers=50) as executor:
        for i in range(0, qtd_registros, qtd_registros_por_thread):
            idx = 0
            lista_processar = []
            for registro in registros_musicas:
                lista_processar.append(registro)
                idx = idx + 1
                if idx >= qtd_registros_por_thread:
                    break

            executor.submit(traduzir_acordes_musicas, lista_processar)