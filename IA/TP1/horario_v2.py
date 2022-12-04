#Utilizar aima-python como biblioteca
import sys
sys.path.insert(0, sys.path[0]+'\\repo\\aima-python')

from csp import *

import math
import warnings
warnings.filterwarnings("ignore")

Disciplinas = 'Portugues Ingles Matematica Historia Informatica'.split()
Dias = 'Segunda Terca Quarta Quinta Sexta'.split()
Horas = 'H8 H10 H12 H14 H16'.split()
Tipo = 'Online Presencial'.split()
Turma = 'T1 T2 T3 T4 T5'.split()
variaveis = set(Disciplinas + Dias + Horas + Tipo + Turma)

dominio = {}
for var in variaveis:
    dominio[var] = set(range(1,6))
#dominio['Portugues'] = {1}
#dominio['Quarta'] = {3}

class lesson:
    
    def __init__(self, Disciplinas, Dias, Horas, Tipo):
        self.Disciplinas = Disciplinas
        self.Dias = Dias
        self.Horas = Horas
        self.Tipo = Tipo
        self.Turma = Turma

    @staticmethod
    def cond1_all_lessons_friday_durantion2hours(l):
        for x  in l:
            if x.dia == 4 and x.dur != 2:
                return False
        return True
    
    @staticmethod
    def cond2_one_or_two_are_online(l):
        online = 0
        for x  in l:
            if x.tipo == 'online':
                online = online + 1
        if online > 0 and online <= 2:
            return True
        return False
    
    @staticmethod
    def cond3_class_should_not_have_more_3_lessons_day(l):
        lessons_per_day = [0,0,0,0,0]
        for x  in l:
            lessons_per_day[x.dia-2] = lessons_per_day[x.dia-2] + 1
        
        for ld in lessons_per_day:
            if ld > 3:
                return False
        return True
    
    @staticmethod
    def cond4_online_lessons_cannot_be_booked_immediately(l):
        return True
    
    @staticmethod
    def cond5_only_2_lessons_per_half_day(l):
        lessons_per_morning = [0,0,0,0,0]
        lessons_per_afternoon = [0,0,0,0,0]
        for x  in l:
            if x.hora <= 13:
                lessons_per_morning[x.dia-2] = lessons_per_morning[x.dia-2] + 1
            else:
                lessons_per_afternoon[x.dia-2] = lessons_per_afternoon[x.dia-2] + 1

        for ld in lessons_per_morning:
            if ld > 2:
                return False
        
        for ld in lessons_per_afternoon:
            if ld > 2:
                return False
            
        return True
    
    @staticmethod
    def cond6_two_classes_specific_classRoom(l):
        return True
    
    @staticmethod
    def cond(l):
        if lesson.cond1_all_lessons_friday_durantion2hours(l) == False:
            return False
        if lesson.cond2_one_or_two_are_online(l) == False:
            return False
        if lesson.cond3_class_should_not_have_more_3_lessons_day(l) == False:
            return False
        if lesson.cond4_online_lessons_cannot_be_booked_immediately(l) == False:
            return False
        if lesson.cond5_only_2_lessons_per_half_day(l) == False:
            return False
        if lesson.cond6_two_classes_specific_classRoom(l) == False:
            return False
        return True 

def teste_condicoes(*values):
    i = 0
    lessons = []
    while i < len(values):
        lessons.append(lesson(values[i], values[i+1], values[i+2], values[i+3], values[i+4]))
        i += 5   
        
    #print(values)
    
    return lesson.cond(lessons)

# constraints
restricoes = [
    Constraint(tuple(dominio.keys()), teste_condicoes)
]

# days_too_short
days_too_short = NaryCSP(dominio, restricoes)
print(days_too_short.variables)

# Result
k = ac_solver(days_too_short, arc_heuristic=sat_up)

print(k)