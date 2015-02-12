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





    print(x)



