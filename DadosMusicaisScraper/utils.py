# -*- coding: utf-8 -*-

__author__ = 'marcelo'

def obter_valor_default(valor, valor_default):
    retorno = valor
    if valor is None or valor == '':
        retorno = valor_default
    return retorno

notas = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']
notas_bemois = ['A', 'Bb', 'B', 'C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab']

import re

def obter_tonica_modo_inversao(acorde):
    acorde = acorde.replace(r'maj', '')
    acorde = acorde.replace(r'min', 'm')
    acorde = acorde.replace(r'°', '-')
    acorde = acorde.replace(r'º', '-')
    acorde = acorde.replace(r'aum', '+')
    acorde = acorde.replace(r'dim', '-')

    regex_tonica = '([A-G](#|b){0,1})'
    regex_notas_acrescentadas = '(\d){0,2}'
    regex_modo = '(m|\+|-){0,1}'
    regex_inversao = '\/{0,1}([A-G]#{0,1}|b{0,1})'
    m = re.search(regex_tonica + regex_notas_acrescentadas + regex_modo + regex_inversao, acorde)
    tonica = obter_valor_default(m.group(1), '')
    modo = obter_valor_default(m.group(4), 'M')
    inversao = obter_valor_default(m.group(5), '')
    return tonica, modo, inversao

def obter_unicos_tonicas_modos_inversoes (acordes, capo_txt=''):
    """
    Dada uma lista de acordes, devolvemos os acordes unicos, as tonicas de cada acorde, os modos de cada acorde e as inversoes de cada acorde.
    :param acordes: Lista com os acordes.
    :return: listas contendo os acordes unicos, as tonicas, os modos e as inversoes
    """

    if len(capo_txt) > 0:
        capo = int(re.search('(\d+)', capo_txt[0].extract()).group(0))

    tonicas = []
    modos = []
    inversoes = []
    acordes_unicos = []

    for acorde in acordes:
        if capo > 0 :

            idx_letra = 1
            notas_local = notas
            if acorde.find("#") == 1:
                idx_letra = 2
            if acorde.find("b") == 1:
                idx_letra = 2
                notas_local = notas_bemois
                try:
                    idx = notas.index(acorde[0: idx_letra])
                    # Busco as notas
                    novo_acorde = notas_local[(capo + idx) % 12]
                    acorde = novo_acorde + acorde[idx:]
                except BaseException as exc:
                    print exc

        if not acorde in acordes_unicos:
            acordes_unicos.append(acorde)

        tonica, modo, inversao = obter_tonica_modo_inversao(acorde)
        tonicas.append(tonica)
        modos.append(modo)
        inversoes.append(inversao)

    return acordes_unicos, tonicas, modos, inversoes


if __name__ == '__main__':

    # TODO CRIAR TESTE UNITARIO

    tonica, modo, inversao = obter_tonica_modo_inversao('G')
    assert (tonica == 'G')

    tonica, modo, inversao = obter_tonica_modo_inversao('Gm')
    assert (tonica == 'G' and  modo == 'm')

    tonica, modo, inversao = obter_tonica_modo_inversao('F#')
    assert (tonica == 'F#')

    tonica, modo, inversao = obter_tonica_modo_inversao('Ab')
    assert (tonica == 'Ab')

    tonica, modo, inversao = obter_tonica_modo_inversao('F°')
    assert (tonica == 'F' and  modo == '-' and inversao == '')

    tonica, modo, inversao = obter_tonica_modo_inversao('E/G#')
    assert (tonica == 'E' and modo == 'M' and inversao == 'G#')

    tonica, modo, inversao = obter_tonica_modo_inversao('G4')
    assert (tonica == 'G' and modo == 'M' and inversao == '')

    tonica, modo, inversao = obter_tonica_modo_inversao('F7M')
    assert (tonica == 'F' and modo == 'M' and inversao == '')

    tonica, modo, inversao = obter_tonica_modo_inversao('C#7+')
    assert (tonica == 'C#' and modo == '+' and inversao == '')

    tonica, modo, inversao = obter_tonica_modo_inversao('Cº')
    assert (tonica == 'C' and modo == '-' and inversao == '')

    tonica, modo, inversao = obter_tonica_modo_inversao('G#7(#5)')
    assert (tonica == 'G#' and modo == 'M' and inversao == '')

    tonica, modo, inversao = obter_tonica_modo_inversao('E7+')
    assert (tonica == 'E' and modo == '+' and inversao == '')

    tonica, modo, inversao = obter_tonica_modo_inversao('Amaj7')
    assert (tonica == 'A' and modo == 'M' and inversao == '')

    tonica, modo, inversao = obter_tonica_modo_inversao('Fmin+11')
    assert (tonica == 'F' and modo == 'm' and inversao == '')

    tonica, modo, inversao = obter_tonica_modo_inversao('A7+')
    assert (tonica == 'A' and modo == '+' and inversao == '')

    tonica, modo, inversao = obter_tonica_modo_inversao('Caum(C5+)')
    assert (tonica == 'C' and modo == '+' and inversao == '')

    tonica, modo, inversao = obter_tonica_modo_inversao('A/F#')
    assert (tonica == 'A' and modo == 'M' and inversao == 'F#')

    tonica, modo, inversao = obter_tonica_modo_inversao('G/13')
    # TODO VERIFICAR ESSA REGRA DE INVERSAO
    assert (tonica == 'G' and modo == 'M' and inversao == '')

    tonica, modo, inversao = obter_tonica_modo_inversao('G7/D')
    # TODO VERIFICAR ESSA REGRA DE INVERSAO
    assert (tonica == 'G' and modo == 'M' and inversao == 'D')

    acordes = ['G7/D', 'Am','C7+','D#º','Dm7','G11','G7','C7+','G7/5+','Em7','D#º','Dm7','Dm4/7','C#7/5-','C7+','G7/13','C7+','D#º','Dm7','G11','G7','Gm7','C7/13','F7+','G#7/9','Em7','A7/9-','D7','G7/9-','C7+','G7/13','C7+','D#º','Dm7','G11','G7','C7+','G7/5+','Em7','D#º','Dm7','Dm4/7','C#7/5-','C7+','G7/13','C7+','D#º','Dm7','G11','G7','Gm7','C7/13','F7+','G#7/9','Em7','A7/9-','D7','G7/9-','C7+']

    acordes_unicos, tonicas, modos, inversoes = obter_unicos_tonicas_modos_inversoes(acordes)

    assert(len(acordes_unicos) < len(acordes))




