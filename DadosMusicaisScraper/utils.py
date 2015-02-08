__author__ = 'marcelo'

def obter_valor_default(valor, valor_default):
    retorno = valor
    if valor is None or valor == '':
        retorno = valor_default
    return retorno

