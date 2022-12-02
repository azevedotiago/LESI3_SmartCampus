#Utilizar aima-python como biblioteca
import sys
sys.path.insert(0, sys.path[0]+'\\repo\\aima-python')

from csp import *

import math
import warnings
warnings.filterwarnings("ignore")

Disciplinas = 'Portugues Ingles Matematica Historia Informatica'.split()
Dias = 'Segunda Terca Quarta Quinta Sexta'.split()
Horas = '8 10 12 14 16'.split()
Tipo = 'Online Presencial'.split()
variaveis = set(Disciplinas + Dias + Horas + Tipo)

dominio = {}
for var in variaveis:
    dominio[var] = set(range(1,6))
dominio['Portugues'] = {1}
dominio['Quarta'] = {3}

def __init__(self, disciplinas, dias, horas, tipo):
    self.disciplinas = disciplinas
    self.dias = dias
    self.horas = horas
    self.tipo = tipo
        
