# -*- coding: utf-8 -*-
__author__ = 'marcelo'

import logging
import re

import mingus.core.chords as chords
from music21 import harmony
from music21 import interval


logging.basicConfig(filename="logs/utils.log", level=logging.INFO)

# acorde = acorde.replace(u'4', 'sus4')
regex_nota = u'([A-G]#*4*(M7)*(7(?!M))*)'
regex_bemol = u'(?P<bemol>b)*'
regex_menor = u'(m)*'
# regex_aug = u'(?P<aug>4)*'
regex_maior7 = u'(?P<maior7>7M|7\+)*'
regex_menor7 = u'(?P<menor7>7m|m7)*'
regex_dom7 = u'(7)*'
regex_dim = u'(?P<dim>°|º|7\-)*'
# NAO USAREMOS OS ACORDES COM AS VARIACOES (9), (9/13), (13) etc
# TODO VERIFICAR SE O 5 NAO SIGNIFICA UM POWER CHORD
regex_nao_usados = u'(?P<nao_usados>(5\-|5\+|5)*b*(\/.*)*(\/[0-9])*(\(.+\))*)'

regex_compilado = re.compile(regex_nota +
                             regex_bemol +
                             regex_menor +
                             regex_maior7 +
                             regex_menor7 +
                             regex_dom7 +
                             regex_dim +
                             regex_nao_usados)


def eh_vazio(valor):
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


dict_troca_notacao = {'bemol': '-',
                      'aug': 'sus4',
                      'maior7': 'M7',
                      'menor7': 'm7',
                      'dim': 'dim',
                      'nao_usados': ''}


def trocar_notacao_acordes(acorde):
    m = regex_compilado.match(acorde)

    dict_group = m.groupdict()
    if dict_group is not None:
        for chave, valor in dict_group.iteritems():
            if not eh_vazio(valor):
                novo_valor = dict_troca_notacao.get(chave)
                acorde = acorde.replace(valor, novo_valor)
    return acorde


def obter_unicos_tonicas_baixos_modos(acordes, capo=0):

    tonicas = []
    baixos = []
    modos = []
    inversoes = []
    acordes_unicos = []

    for acorde in acordes:
        try:
            logging.info(u"Alterando o acorde <%s>, caso nao esteja previsto..." % acorde)
            novo_acorde = trocar_notacao_acordes(acorde)
            logging.info(u"Acorde alterado. De <%s> para <%s>..." % (acorde, novo_acorde))
            acorde = novo_acorde
            logging.info(u"Traduzindo acorde <%s> no music21..." % acorde)

            obj_acorde = harmony.ChordSymbol(acorde)

            if capo > 0:
                try:
                    # novas_notas = []
                    # for nota_str in notas:
                    # nota_obj = Note(nota_str)
                    # nova_nota_int = int(nota_obj) + capo
                    #     nota_obj.from_int(nova_nota_int)
                    #     novas_notas.append(nota_obj.name)
                    # notas = novas_notas
                    #novo_acorde = harmony.ChordSymbol(acorde)
                    aInterval = interval.Interval(capo)
                    obj_acorde.transpose(aInterval, inPlace=True)
                except BaseException as exc:
                    logging.info(u"Erro ao transpor a nota no music21. Detalhes: %s..." % exc)

            # acorde_traduzido = chords.determine(notas, True, True)[0]
            acorde_traduzido, modo = harmony.chordSymbolFigureFromChord(obj_acorde, True)
            if not acorde_traduzido in acordes_unicos:
                acordes_unicos.append(acorde_traduzido)
                modos.append(modo)
                tonicas.append(obj_acorde.root().name)
                baixos.append(obj_acorde.bass().name)
        except BaseException as exc:
            logging.error(u"Erro ao traduzir o acorde: <%s>. Detalhes: %s" % (acorde, exc))

            # if capo > 0:
    return acordes_unicos, tonicas, modos


if __name__ == '__main__':
    # TODO CRIAR TESTE UNITARIO


    novo_acorde = harmony.ChordSymbol('A4')
    [str(p) for p in novo_acorde.pitches]
    novo_acorde = harmony.ChordSymbol('Asus')
    [str(p) for p in novo_acorde.pitches]
    novo_acorde = harmony.ChordSymbol('Asus4')
    [str(p) for p in novo_acorde.pitches]
    novo_acorde = harmony.ChordSymbol('AM7')
    [str(p) for p in novo_acorde.pitches]

    novo_acorde = harmony.ChordSymbol('A-m')
    [str(p) for p in novo_acorde.pitches]

    aInterval = interval.Interval(2)
    b = novo_acorde.transpose(aInterval, inPlace=True)

    print b

    novo_acorde = harmony.ChordSymbol('C#7')
    [str(p) for p in novo_acorde.pitches]





    # novo_acorde = trocar_notacao_acordes(u'A4')
    # notas = chords.from_shorthand(novo_acorde)
    # assert len(notas) > 0
    #
    # novo_acorde = trocar_notacao_acordes(u'Asus')
    # notas = chords.from_shorthand(novo_acorde)
    # assert len(notas) > 0
    #
    # novo_acorde = trocar_notacao_acordes(u'Asus4')
    # notas = chords.from_shorthand(novo_acorde)
    # assert len(notas) > 0

    # novo_acorde = trocar_notacao_acordes(u'A7M')
    # notas = chords.from_shorthand(novo_acorde)
    # assert len(notas) > 0

    # regex_nota = r'7(?!M)'
    #
    # m = re.match(regex_nota, r'7M')
    #
    # x = m.group(0)



    regex_nota = u'([A-G]#*4*(M7)*(7(?!M))*)'

    m = re.match(regex_nota, "D7M")



    print x

    novo_acorde = trocar_notacao_acordes(u'D7M')

    novo_acorde = trocar_notacao_acordes(u'D5(6)')
    notas = chords.from_shorthand(novo_acorde)
    assert len(notas) > 0

    novo_acorde = trocar_notacao_acordes(u'A°')
    notas = chords.from_shorthand(novo_acorde)
    assert len(notas) > 0

    novo_acorde = trocar_notacao_acordes(u'Aº')
    notas = chords.from_shorthand(novo_acorde)
    assert len(notas) > 0

    novo_acorde = trocar_notacao_acordes(u'D5(6/9)')
    notas = chords.from_shorthand(novo_acorde)
    assert len(notas) > 0

    novo_acorde = trocar_notacao_acordes(u'G#7(#5)')
    notas = chords.from_shorthand(novo_acorde)
    assert len(notas) > 0

    novo_acorde = trocar_notacao_acordes(u'Em7(9)')
    notas = chords.from_shorthand(novo_acorde)
    assert len(notas) > 0

    novo_acorde = trocar_notacao_acordes(u'B5b')
    notas = chords.from_shorthand(novo_acorde)
    assert len(notas) > 0

    novo_acorde = trocar_notacao_acordes(u'B5b/6/9')
    notas = chords.from_shorthand(novo_acorde)
    assert len(notas) > 0

    novo_acorde = trocar_notacao_acordes(u'G#m7(b13)')
    notas = chords.from_shorthand(novo_acorde)
    assert len(notas) > 0

    # novo_acorde = trocar_notacao_acordes(u'D4/F#')
    # notas = chords.from_shorthand(novo_acorde)
    # assert len(notas) > 0

    novo_acorde = trocar_notacao_acordes(u'Gsus4')
    assert len(notas) > 0

    novo_acorde = trocar_notacao_acordes(u'C#m5+/7')
    print novo_acorde

    novo_acorde = trocar_notacao_acordes(u'G#7+/9-')
    print novo_acorde
    regex_nao_usados = u'(?P<nao_usados>(5\-|5\+|5)*b*(\/.*)*(\/[0-9])*(\(.+\))*)'

    m = re.match(regex_nao_usados, "/9-")

    dict_group = m.groupdict()

    print dict_group



    # obter_unicos_tonicas_modos_inversoes('G', 1)




















    # tonica, modo, inversao = obter_tonica_modo_inversao(u'G')
    # assert (tonica == 'G')
    #
    # tonica, modo, inversao = obter_tonica_modo_inversao(u'Gm')
    # assert (tonica == 'G' and modo == 'm')
    #
    # tonica, modo, inversao = obter_tonica_modo_inversao(u'F#')
    # assert (tonica == 'F#')
    #
    # tonica, modo, inversao = obter_tonica_modo_inversao(u'Ab')
    # assert (tonica == 'Ab')
    #
    # tonica, modo, inversao = obter_tonica_modo_inversao(u'F°')
    # assert (tonica == 'F' and modo == '-' and inversao == '')
    #
    # tonica, modo, inversao = obter_tonica_modo_inversao(u'E/G#')
    # assert (tonica == 'E' and modo == 'M' and inversao == 'G#')
    #
    # tonica, modo, inversao = obter_tonica_modo_inversao(u'G4')
    # assert (tonica == 'G' and modo == 'M' and inversao == '')
    #
    # tonica, modo, inversao = obter_tonica_modo_inversao(u'F7M')
    # assert (tonica == 'F' and modo == 'M' and inversao == '')
    #
    # tonica, modo, inversao = obter_tonica_modo_inversao(u'C#7+')
    # assert (tonica == 'C#' and modo == '+' and inversao == '')
    #
    # tonica, modo, inversao = obter_tonica_modo_inversao(u'Cº')
    # assert (tonica == 'C' and modo == '-' and inversao == '')
    #
    # tonica, modo, inversao = obter_tonica_modo_inversao(u'G#7(#5)')
    # assert (tonica == 'G#' and modo == 'M' and inversao == '')
    #
    # tonica, modo, inversao = obter_tonica_modo_inversao(u'E7+')
    # assert (tonica == 'E' and modo == '+' and inversao == '')
    #
    # tonica, modo, inversao = obter_tonica_modo_inversao(u'Amaj7')
    # assert (tonica == 'A' and modo == 'M' and inversao == '')
    #
    # tonica, modo, inversao = obter_tonica_modo_inversao(u'Fmin+11')
    # assert (tonica == 'F' and modo == 'm' and inversao == '')
    #
    # tonica, modo, inversao = obter_tonica_modo_inversao(u'A7+')
    # assert (tonica == 'A' and modo == '+' and inversao == '')
    #
    # tonica, modo, inversao = obter_tonica_modo_inversao(u'Caum(C5+)')
    # assert (tonica == 'C' and modo == '+' and inversao == '')
    #
    # tonica, modo, inversao = obter_tonica_modo_inversao(u'A/F#')
    # assert (tonica == 'A' and modo == 'M' and inversao == 'F#')
    #
    # tonica, modo, inversao = obter_tonica_modo_inversao(u'G/13')
    # # TODO VERIFICAR ESSA REGRA DE INVERSAO
    # assert (tonica == 'G' and modo == 'M' and inversao == '')
    #
    # tonica, modo, inversao = obter_tonica_modo_inversao(u'G7/D')
    # # TODO VERIFICAR ESSA REGRA DE INVERSAO
    # assert (tonica == 'G' and modo == 'M' and inversao == 'D')
    #
    # acordes = ['G7/D', 'Am', 'C7+', u'D#º', 'Dm7', 'G11', 'G7', 'C7+', 'G7/5+', 'Em7', u'D#º', 'Dm7', 'Dm4/7', 'C#7/5-',
    # 'C7+', 'G7/13', 'C7+', u'D#º', 'Dm7', 'G11', 'G7', 'Gm7', 'C7/13', 'F7+', 'G#7/9', 'Em7', 'A7/9-', 'D7',
    # 'G7/9-', 'C7+', 'G7/13', 'C7+', u'D#º', 'Dm7', 'G11', 'G7', 'C7+', 'G7/5+', 'Em7', u'D#º', 'Dm7',
    # 'Dm4/7', 'C#7/5-', 'C7+', 'G7/13', 'C7+', u'D#º', 'Dm7', 'G11', 'G7', 'Gm7', 'C7/13', 'F7+', 'G#7/9',
    #            'Em7', 'A7/9-', 'D7', 'G7/9-', 'C7+']
    #
    # acordes_unicos, tonicas, modos, inversoes = obter_unicos_tonicas_modos_inversoes(acordes)
    #
    # assert (len(acordes_unicos) < len(acordes))
    #
    # acordes = [
    #     "C",
    #     "D",
    #     "Em",
    #     "Em/B",
    #     "C",
    #     "D",
    #     "Em",
    #     "D9",
    #     "Em",
    #     "Bm",
    #     "Em",
    #     "Bm",
    #     "Em",
    #     "Bm",
    #     "Am",
    #     "D9",
    #     "D9",
    #     "Em",
    #     "Bm",
    #     "Em",
    #     "Bm",
    #     "Em",
    #     "Bm",
    #     "Am",
    #     "D9",
    #     "C",
    #     "D",
    #     "Em",
    #     "Em/B",
    #     "C",
    #     "D",
    #     "Em",
    #     "D9",
    #     "C",
    #     "D",
    #     "Em",
    #     "Em/B",
    #     "C",
    #     "D",
    #     "Em",
    #     "D9",
    #     "Em",
    #     "Bm",
    #     "Em",
    #     "Bm",
    #     "Em",
    #     "Bm",
    #     "Am",
    #     "D9",
    #     "D9",
    #     "Em",
    #     "Bm",
    #     "Em",
    #     "Bm",
    #     "Em",
    #     "Bm",
    #     "Am",
    #     "D9",
    #     "C",
    #     "D",
    #     "Em",
    #     "Em/B",
    #     "C",
    #     "D",
    #     "Em",
    #     "D9",
    #     "Em",
    #     "D",
    #     "C",
    #     "D",
    #     "G",
    #     "A9",
    #     "G",
    #     "A9",
    #     "G",
    #     "A9",
    #     "G",
    #     "A9",
    #     "Em",
    #     "Bm",
    #     "Em",
    #     "Bm",
    #     "Em",
    #     "Bm",
    #     "Am",
    #     "D9",
    #     "C",
    #     "D",
    #     "Em",
    #     "Em/B",
    #     "C",
    #     "D",
    #     "Em",
    #     "C",
    #     "D",
    #     "Em",
    #     "Em/B",
    #     "C",
    #     "D",
    #     "Em",
    #     "Em/B",
    #     "C",
    #     "D",
    #     "Em",
    #     "Em/B",
    #     "C",
    #     "D",
    #     "Em",
    #     "D9",
    #     "Em"
    # ]
    #
    # acordes_unicos, tonicas, modos, inversoes = obter_unicos_tonicas_modos_inversoes(acordes, 5)
    #
    # assert (len(acordes_unicos) < len(acordes))

    print 'teste'




