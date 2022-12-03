#Utilizar aima-python como biblioteca
import sys
sys.path.insert(0, sys.path[0]+'\\repo\\aima-python')

from csp import *

import math
import warnings
warnings.filterwarnings("ignore")

# Solve Zebra using ac_sover

# variables
Colors = 'Red Yellow Blue Green Ivory'.split()
Pets = 'Dog Fox Snails Horse Zebra'.split()
Drinks = 'OJ Tea Coffee Milk Water'.split()
Countries = 'Englishman Spaniard Norwegian Ukranian Japanese'.split()
Smokes = 'Kools Chesterfields Winston LuckyStrike Parliaments'.split()
variables = set (Colors + Pets + Drinks + Countries + Smokes)

# Domains
dominio = {}
for var in variables:
    dominio[var] = set(range(1, 6))     # list(range(1, 6))
dominio['Norwegian'] = {1}
dominio['Milk'] = {3}

# Constraints
restricoes = [
              Constraint(Colors, all_diff_constraint),
              Constraint(Pets, all_diff_constraint),
              Constraint(Drinks, all_diff_constraint),
              Constraint(Countries, all_diff_constraint),
              Constraint(Smokes, all_diff_constraint),
              Constraint(('Englishman', 'Red'), eq),
              Constraint(('Spaniard', 'Dog'), eq),
              Constraint(('Kools', 'Yellow'), eq),
              Constraint(('Winston', 'Snails'), eq),
              Constraint(('LuckyStrike', 'OJ'), eq),
              Constraint(('Ukranian', 'Tea'), eq),
              Constraint(('Japanese', 'Parliaments'), eq),
              Constraint(('Coffee', 'Green'), eq),
              Constraint(('Chesterfields', 'Fox'), lambda a, b: abs(a - b) == 1),
              Constraint(('Norwegian', 'Blue'), lambda a, b: abs(a - b) == 1),
              Constraint(('Kools', 'Horse'), lambda a, b: abs(a - b) == 1),
              Constraint(('Green', 'Ivory'), lambda a, b: b == a - 1),
              ]

# days_too_short
zebra_csp = NaryCSP(dominio, restricoes)
print(zebra_csp.variables)

# Apply solver
ans = ac_solver(zebra_csp, arc_heuristic=sat_up)

# Print result
for h in range(1, 6):
        print('House', h, end=' ')
        for (var, val) in ans.items():
            if val == h:
                print(var, end=' ')
        print()