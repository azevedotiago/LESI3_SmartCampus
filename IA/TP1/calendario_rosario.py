#Utilizar aima-python como biblioteca
import sys
sys.path.insert(0, sys.path[0]+'\\repo\\aima-python')

from csp import *

import math
import warnings
warnings.filterwarnings("ignore")

Disciplinas = 'Portugues Ingles Matematica Historia Informatica Ciencias Direito Fiscalidade Redes Fisica'.split()
Dias = 'Segunda Terca Quarta Quinta Sexta Segunda Terca Quarta Quinta Sexta'.split()
Horas = 'H8 H10 H12 H14 H16 H8 H10 H12 H14 H16'.split()
Tipo = 'Online Presencial'.split()
Turma = 'T1 T2 T3 T4 T5 T6 T7 T8 T9'.split()
Sala = 'S1 S2 S3 S4 S5'.split()
variaveis = list(Disciplinas + Dias + Horas + Tipo + Turma + Sala)

dominio = {}
for var in variaveis:
    dominio[var] = list(range(1,11))
#dominio['Portugues'] = {1}
#dominio['Quarta'] = {3}

# constraints
restricoes = [
              #Constraint(tuple(dominio.keys()), teste_condicoes),
              Constraint(Disciplinas, all_diff_constraint),
              Constraint(Horas, all_diff_constraint),
              Constraint(Dias, all_diff_constraint),
              Constraint(Turma, all_diff_constraint),
              Constraint(Tipo, all_diff_constraint),
              Constraint(Sala, all_diff_constraint),
              Constraint(('Segunda','Ingles'), eq),
            
              ]

# days_too_short
days_too_short = NaryCSP(dominio, restricoes)
print(days_too_short.variables)

# Result
k = ac_solver(days_too_short, arc_heuristic=sat_up)

#Print result
for h in range(1,11):
    print('Solucao', h, end=' ')
    for (var,val) in h.items():
        if val == h:
            print(var, end=' ')
    print()

#print(k)