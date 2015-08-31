# -*- coding: utf-8 -*-
__author__ = 'marcelo'

import sys
import getopt

from scrapy import cmdline

def main(argv):
    try:
        opts, args = getopt.getopt(argv, 's:')
        if len(opts) == 0:
            raise getopt.GetoptError(u'Argumento "-s" obrigatorio')
        for opt, arg in opts:
            if opt != '-s' or arg == '':
                raise getopt.GetoptError(u'Argumento "-s" obrigatorio')
            cmdline.execute(('scrapy crawl ' + arg).split())
            break
    except getopt.GetoptError:
        print('Erro!\nUtilize o comando: main.py -s <nome do spider>')
        sys.exit(2)


if __name__ == "__main__":
    #main(sys.argv[1:])
    from music21 import chord
    from music21 import pitch

    for i in range(0,12):
        print(i, str(pitch.Pitch(i)))

    #print(pitch.Pitch("D#"))

    c = chord.Chord([0, 4, 7])
    print(c.commonName)

    c = chord.Chord([0, 3, 7])
    print(c.commonName)

    c = chord.Chord([0, 1, 5, 7, 8])
    print(c.commonName)

    c = chord.Chord([0,3,4,7,8])
    print(c.commonName)

    c = chord.Chord([0,1,4,6,9])
    print(c.commonName)

    c = chord.Chord([0,1,4,6,9])
    print(c.commonName)

    c = chord.Chord([0,1,4,7,8])
    print(c.commonName)

    c = chord.Chord([0,1,4,6])
    print(c.commonName)

    c = chord.Chord([0,1,3,4])
    print(c.commonName)

    c = chord.Chord([0,3,4,6,8])
    print(c.commonName)

    c = chord.Chord([0,3,4,8])
    c = chord.Chord([0,2,4,8])
    c = chord.Chord([0,2,3,6,8])
    c = chord.Chord([0,2,3,4,7])
    c = chord.Chord([0,3,6])
    c = chord.Chord([0,2,3,5,8])
    c = chord.Chord([0,3,5,6,8])
    c = chord.Chord([0,1,2,5,8])
    c = chord.Chord([0,3,6,9])
    c = chord.Chord([0,3,6])
    c = chord.Chord([0,2,4,6,7,9])
    c = chord.Chord([0,2,4,6,9])
    c = chord.Chord([0,3,6,8])
    c = chord.Chord([0,1,5,6])
    c = chord.Chord([0,2,3,6,9])
    c = chord.Chord([0,2,5,8])
    c = chord.Chord([0,2,3,6])
    c = chord.Chord([0,3,5])
    c = chord.Chord([0,4,6])
    c = chord.Chord([0,1,5])
    c = chord.Chord([0,2,5])
    c = chord.Chord([0,1,3,5,6,8])
    c = chord.Chord([0,1,3,5])
    c = chord.Chord([0,2,4,5,7])
    c = chord.Chord([0,2,4,7,9])
    c = chord.Chord([0,2,4,7])
    c = chord.Chord([0,2,3,7])
    c = chord.Chord([0,4,7])
    c = chord.Chord([0,1,4,8])
    c = chord.Chord([0,3,5,6,8])
    c = chord.Chord([0,2,3,5,7,8])
    c = chord.Chord([0,1,3,4,8])
    c = chord.Chord([0,3,5,7,8])
    c = chord.Chord([0,1,3,6])
    c = chord.Chord([0,1,5,7])
    c = chord.Chord([0,3,5,8])
    c = chord.Chord([0,3,5,6,7])
    c = chord.Chord([0,3,5,7])
    c = chord.Chord([0,1,3,5,7,8])
    c = chord.Chord([0,1,3,5,7])
    c = chord.Chord([0,1,3,5])
    c = chord.Chord([0,2,5,7])
    c = chord.Chord([0,1,6])
    c = chord.Chord([0,2,6,7])
    c = chord.Chord([0,2,4,6,8])
    c = chord.Chord([0,2,4,6])
    c = chord.Chord([0,2,4])
    c = chord.Chord([0,1,2,6,7,8])
    c = chord.Chord([0,1,2,3,4,5])
    c = chord.Chord([0,2,6,8])
    c = chord.Chord([0,2,4,5,7,9])
    c = chord.Chord([0,2,3,5,7])
    c = chord.Chord([0,5])
    c = chord.Chord([0,2,4,5])
    c = chord.Chord([0,1,4,7])
    c = chord.Chord([0,1,3,4,7])
    c = chord.Chord([0,3,4,7])
    c = chord.Chord([0,1,3,5,8])
    c = chord.Chord([0,2,5,7])
    c = chord.Chord([0,1,2,5,7,8])

    print(c.commonName)















