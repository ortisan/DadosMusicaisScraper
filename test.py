# -*- coding: utf-8 -*-
__author__ = 'marcelo'

import mingus.core.chords as chords
from music21 import *


if __name__ == '__main__':
    acorde = 'G7/9-'
    #acorde = 'Fm+11'
    acorde = 'G7(9)'



    #TODO REMOVER TUDO QUE TEM EM PARENTESES
    acorde = acorde.replace('+11', '11')
    #acorde = acorde.replace('(', '').replace(')', '')
    #print chords.from_shorthand(acorde)
    #print chords.determine(x, True)

    from music21.harmony import *

    x = harmony.ChordSymbol('Cm')

    x = harmony.ChordSymbol('G#7')


    import datetime
    dt_publicacao_str = 'Publicado em 14 de jul de 2014'
    dt_publicacao = datetime.datetime.strptime(dt_publicacao_str, 'Publicado em %d de %b de %Y')
    data_atual = datetime.datetime.today()
    delta = data_atual - dt_publicacao

    dias = delta.days




    print(x)



