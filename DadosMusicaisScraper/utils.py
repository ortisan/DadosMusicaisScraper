# -*- coding: utf-8 -*-
__author__ = 'marcelo'

import logging
import urllib
import urllib2
import json
import re

from music21 import chord
from music21 import interval


LOG_FILENAME = 'utils.log'
logging.basicConfig(filename=LOG_FILENAME,
                    level=logging.ERROR)

notas_escala_sus = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']
notas_escala_bemol = ['A', 'B-', 'B', 'C', 'D-', 'D', 'E-', 'E', 'F', 'G-', 'G', 'A-']
idx_inicio_capo = [7, 12, 17, 22, 26, 31]
acordes_cache = {}
desenhos_acordes_cache = {}
idx_notas_acordes_cache = {}


def eh_vazio(valor):
    """

    :param valor:
    :return:
    """
    retorno = False
    if valor is None or valor == '':
        retorno = True
    return retorno


def obter_valor_default(valor, valor_default):
    """
    Caso o valor seja None ou '', retornamos o valor_default
    :param valor: Valor que será avaliado
    :param valor_default: Valor default.
    :return: Valor caso seja != None e != '', senão valor_default.
    """
    retorno = valor
    if eh_vazio(valor):
        retorno = valor_default
    return retorno


def obter_dados_acorde(acorde_str, capo):
    acorde = acordes_cache.get(acorde_str)

    match_bemol = re.match("^([A-G]b)", acorde_str)

    lista_notas_escala = notas_escala_sus

    if match_bemol != None:
        lista_notas_escala = notas_escala_bemol

    if acorde == None:
        # desenho_acorde_str = obter_desenho_cifraclub(acorde_str)
        desenho_acorde_str = obter_desenho_echord(acorde_str)

        lista_notas_acorde = []
        desenho_acorde = desenho_acorde_str.split()
        lista_idx_notas = []
        for i in range(0, 6):
            nota_str = desenho_acorde[i]
            if nota_str != "X":
                nota = int(nota_str)
                inicio_capo = idx_inicio_capo[i]
                idx_nota = (inicio_capo + nota) % 12
                # nota_traduzida = notas[idx_nota]
                # lista_notas.append(nota_traduzida)
                lista_idx_notas.append(idx_nota)

        for i in lista_idx_notas:
            lista_notas_acorde.append(lista_notas_escala[i])

        acorde = chord.Chord(lista_notas_acorde)

    tonica = [nota for nota in lista_notas_escala if nota[0] == acorde_str[0]][0]

    acorde.root(tonica)

    math_inversao = re.match("^.+\/([A-G])", acorde_str)

    baixo = tonica

    if math_inversao != None:
        primeira_nota_baixo = math_inversao.group(1)
        baixo = [nota for nota in lista_notas_escala if nota[0] == primeira_nota_baixo][0]
        # TODO VERIFICAR SE ACHA A NOTA

    acorde.bass(baixo)
    acordes_cache[acorde_str] = acorde
    # if sinonimo != sinonimo:
    # acordes_cache[sinonimo] = acorde

    aInterval = interval.Interval(capo)
    acorde_com_capo = acorde.transpose(aInterval)

    return acorde_com_capo




def transpor_acorde(obj_acorde, capo):
    foi_sucesso = obj_acorde['foi_sucesso']
    if foi_sucesso:
        desenho_acorde = obj_acorde['desenho_acorde']
        lista_idx_notas, lista_oitavas = obter_lista_idx_oitava_notas(desenho_acorde)
        nova_lista_idx_notas = [(idx_nota + capo) % 12 for idx_nota in lista_idx_notas]

        lista_notas_escala = notas_escala_sus
        nome_acorde = obj_acorde['_id']
        match_bemol = re.match("^([A-G]b)", nome_acorde)

        if match_bemol != None:
            lista_notas_escala = notas_escala_bemol

        novas_notas = []
        for i in range(0, len(lista_idx_notas)):
            idx_nota = lista_idx_notas[i]
            oitava = lista_oitavas[i]
            novas_notas.append(lista_notas_escala[idx_nota] + str(oitava))

        acorde_21 = chord.Chord(novas_notas)
        return nova_lista_idx_notas, novas_notas, acorde_21
    else:
        return [], [], None


    def obter_desenho_lista_idx_notas(acorde_str):
        # desenho_acorde_str = obter_desenho_cifraclub(acorde_str)
        if acorde_str in desenhos_acordes_cache:
            desenho_acorde_str = desenhos_acordes_cache[acorde_str]
            idx_lista_notas_acorde = idx_notas_acordes_cache[acorde_str]
            return desenho_acorde_str, idx_lista_notas_acorde, True, 'Sucesso - Cache'
        else:
            try:
                try:
                    desenho_acorde_str = obter_desenho_echord(acorde_str)
                except BaseException as exc:
                    desenho_acorde_str = obter_desenho_cifraclub(acorde_str)

                desenho_acorde = desenho_acorde_str.split()
                lista_idx_notas = []
                lista_notas = []
                for i in range(0, 6):
                    nota_str = desenho_acorde[i]
                    if nota_str != "X":
                        nota = int(nota_str)
                        inicio_capo = idx_inicio_capo[i]
                        idx_nota = (inicio_capo + nota) % 12
                        nota_traduzida = notas_escala_sus[idx_nota]
                        lista_notas.append(nota_traduzida)
                        lista_idx_notas.append(idx_nota)
                return desenho_acorde_str, lista_idx_notas, lista_notas, True, 'Sucesso'

            except BaseException as exc:
                # TODO VERIFICAR O TIPO DE ERRO
                return '', [], [], False, "Erro: %s" % exc


def obter_lista_idx_oitava_notas(desenho_acorde):
    desenho_acorde = desenho_acorde.split()
    lista_idx_notas = []
    lista_oitavas = []
    for i in range(0, 6):
        nota_str = desenho_acorde[i]
        if nota_str != "X":
            nota = int(nota_str)
            inicio_capo = idx_inicio_capo[i]
            idx_nota = (inicio_capo + nota) % 12
            oitava = int((inicio_capo + nota) / 12)
            lista_idx_notas.append(idx_nota)
            lista_oitavas.append(oitava)
    return lista_idx_notas, lista_oitavas


def obter_desenho_cifraclub(acorde):
    acorde = substituir_caracteres_acorde(acorde)

    form_data = {'acorde': acorde, "capo": 0, 'afinacao': 'E-A-D-G-B-E', 'casas': 'X X X X X X', 'bcp': False}
    params = urllib.urlencode(form_data)
    response = urllib2.urlopen('http://www.cifraclub.com.br/ajax/dicionario.php', params)
    json_data = response.read()
    data = json.loads(json_data)
    # sinonimo = data['sinonimo']
    desenho_acorde_str = data['violao'][0]
    return desenho_acorde_str


def obter_desenho_echord(acorde):
    acorde = substituir_caracteres_acorde(acorde)

    form_data = {'type': '', "method": 2, 'chord': acorde}
    params = urllib.urlencode(form_data)

    response = urllib2.urlopen("http://www.e-chords.com/site/chords2.asp?" + params)
    html_data = response.read()

    import re

    desenho_acorde_str = re.search("variations':'(([0-9]|,|X)+)", html_data).group(1)

    return desenho_acorde_str.replace(",", " ")


# def obter_desenho_chord_c(acorde):
# acorde = substituir_caracteres_acorde(acorde)
#
# form_data = {'searchFor': acorde}
# params = urllib.urlencode(form_data)
# response = urllib2.urlopen('http://chord-c.com/guitar-chord-search/', params)
# html_data = response.read()
# # sinonimo = data['sinonimo']
# from bs4 import BeautifulSoup
# soup = BeautifulSoup(html_data)
# div = soup.find_all("div", class_="diaM")[0]
# soup.find(class="diaM")
# return ''


def substituir_caracteres_acorde(acorde):
    regex_dim = u'(°|º|7\-)+'
    import re

    return re.sub(regex_dim, 'dim', acorde)


def obter_novos_unicos_tonicas_baixos_modos(acordes_str, capo=0):
    unicos = []
    tonicas = []
    modos = []

    for acorde_str in acordes_str:
        try:
            logging.info(u"Obtendo dados do acorde <%s>..." % acorde_str)

            logging.info(u"Traduzindo acorde <%s> no music21..." % acorde_str)

            acorde = obter_dados_acorde(acorde_str, capo)

            nome_acorde = acorde.fullName
            tonica = acorde.root().name
            modo = acorde.quality

            if not nome_acorde in unicos:
                unicos.append(nome_acorde)
                tonicas.append(tonica)
                modos.append(modo)
        except BaseException as exc:
            logging.error(u"Erro ao traduzir o acorde: <%s>. Detalhes: %s" % (acorde_str, exc))
            raise exc

    return unicos, tonicas, modos


if __name__ == '__main__':
    # import re
    #
    # acorde_str = "D7/B"
    # m = re.match("^.+\/([A-G])", acorde_str)
    # print(m)

    seq_acordes = [
        u"D°",
        "Abm",
        "D5",
        "A7(11+)",
        "Am(11+)",
        "D7/9",
        "Am6",
        "Em6",
        "Am7",
        "Am6",
        "Am7",
        "D7/9b"]

    # unicos, tonicas, modos = obter_novos_unicos_tonicas_baixos_modos(seq_acordes, 0)
    #
    # print(unicos)

    # obter_desenho_chord_c('Abm');










