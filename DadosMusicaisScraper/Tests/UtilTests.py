# -*- coding: utf-8 -*-
__author__ = 'marcelo'

import unittest

from DadosMusicaisScraper.utils import *


class UnitTests(unittest.TestCase):
    def test_eh_vazio(self):
        self.assertTrue(eh_vazio(None))
        self.assertTrue(eh_vazio(''))
        self.assertFalse(eh_vazio('abc'))
        self.assertFalse(eh_vazio(123))

    def test_valor_default(self):
        self.assertEqual(obter_valor_default(None, 'abc'), 'abc')
        self.assertEqual(obter_valor_default('', 'abc'), 'abc')
        self.assertEqual(obter_valor_default('abc', ''), 'abc')
        self.assertEqual(obter_valor_default(None, '0'), '0')
        self.assertEqual(obter_valor_default('', '0'), '0')
        self.assertEqual(obter_valor_default(None, 0), 0)
        self.assertEqual(obter_valor_default('', 0), 0)

    def test_normalizacao_acordes(self):
        seq_acordes = ["Am7",
                       "G7",
                       "D7",
                       "G",
                       "Bm7",
                       "Em",
                       "Em/D#"]

        unicos, tonicas, modos = obter_unicos_tonicas_baixos_modos(seq_acordes)
        self.assertEqual(['Am7', 'G7', 'D7', 'G', 'Bm7', 'Em'], unicos)
        self.assertEqual(['A', 'G', 'D', 'G', 'B', 'E'], tonicas)
        self.assertEqual(['minor-seventh', 'dominant-seventh', 'dominant-seventh', 'major', 'minor-seventh', 'minor'],
                         modos)

        seq_acordes = ["Dm",
                       "F",
                       "Bb",
                       "C",
                       "A"]

        unicos, tonicas, modos = obter_unicos_tonicas_baixos_modos(seq_acordes)
        self.assertEqual(['Dm', 'F', 'B-', 'C', 'A'], unicos)
        self.assertEqual(['D', 'F', 'B-', 'C', 'A'], tonicas)
        self.assertEqual(['minor', 'major', 'major', 'major', 'major'], modos)

        seq_acordes = ["A7M",
                       "A6",
                       "Am(7M)",
                       "Am6",
                       "B/A",
                       "E",
                       "C#7",
                       "A7M",
                       "A6",
                       "Am(7M)",
                       "Am6",
                       "B/A",
                       "E",
                       "E4",
                       "E",
                       "F7M(13)/C",
                       "F#m7",
                       "B7(b9)",
                       "G#m7",
                       "E7(4)",
                       "E7",
                       "C#7(4)",
                       "C#7",
                       "F#m7",
                       "B7(b9)",
                       "G#m7",
                       "C#7(4)",
                       "C#7",
                       "F#m7",
                       "B7(4)",
                       "B7",
                       "G#m7",
                       "C#7(4/9)",
                       "C#7",
                       "F#m7",
                       "B7(4)",
                       "B7",
                       "G#m7",
                       "C#7(4/9)",
                       "C#7",
                       "A7M",
                       "A6",
                       "A7M",
                       "A6",
                       "Am(7M)",
                       "Am6",
                       "B/A",
                       "E",
                       "E4",
                       "E",
                       "F7M(13)/C",
                       "F#m7",
                       "B7(b9)",
                       "G#m7",
                       "E7(4)",
                       "E7",
                       "C#7(4)",
                       "C#7",
                       "A7M",
                       "Am(7M)",
                       "B7(4/9)",
                       "E7M(9)",
                       "E7(9)",
                       "C#7(4)",
                       "C#7",
                       "F#m7",
                       "B7(4)",
                       "B7",
                       "G#m7",
                       "C#7(4/9)",
                       "C#7",
                       "F#m7",
                       "B7(4)",
                       "B7",
                       "G#m7"]

        h = harmony.ChordSymbol('B7')
        h.addChordStepModification(harmony.ChordStepModification('add', 4))
        harmony.chordSymbolFigureFromChord(h, True)

        novo_acorde = harmony.ChordSymbol('B11')
        [str(p) for p in novo_acorde.pitches]

        for acorde in seq_acordes:
            print(acorde)
            try:
                novo_acorde = harmony.ChordSymbol(acorde)
                [str(p) for p in novo_acorde.pitches]
            except BaseException as exc:
                print(exc)




