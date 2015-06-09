__author__ = 'marcelo'
import unittest

from DadosMusicaisScraper.utils import *


class TesteUtils(unittest.TestCase):
    def test_traducao_acordes(self):
        seq_acordes = ['C', 'Db']
        unicos, tonicas, modos = obter_novos_unicos_tonicas_baixos_modos(seq_acordes, 2)

        self.assertEqual(unicos[0] == 'true')


