# -*- coding: utf-8 -*-
__author__ = 'marcelo'
import unittest

from DadosMusicaisScraper.utils import *


class TesteUtils(unittest.TestCase):
    def test_traducao_acordes(self):
        seq_notas = ['A#5/F']

        unicos, tonicas, baixos, modos = obter_unicos_tonicas_baixos_modos(seq_notas)
        unicos2, tonicas2, baixos2, modos2 = obter_unicos_tonicas_baixos_modos(seq_notas, 2)

        self.assertNotEqual(unicos[0], unicos2[0])
        self.assertNotEqual(tonicas[0], tonicas2[0])
        self.assertNotEqual(baixos[0], baixos2[0])
        self.assertEqual(modos[0], modos2[0])

        seq_notas = ['C']
        unicos, tonicas, baixos, modos = obter_unicos_tonicas_baixos_modos(seq_notas)
        unicos2, tonicas2, baixos2, modos2 = obter_unicos_tonicas_baixos_modos(seq_notas, 2)

        self.assertNotEqual(unicos[0], unicos2[0])
        self.assertNotEqual(tonicas[0], tonicas2[0])
        self.assertNotEqual(baixos[0], baixos2[0])
        self.assertEqual(modos[0], modos2[0])
