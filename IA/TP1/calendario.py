#Utilizar aima-python como biblioteca
import sys
sys.path.insert(0, sys.path[0]+'\\repo\\aima-python')

from csp import *

import math
import warnings
warnings.filterwarnings("ignore")

        
dominio = {
    #'name': set(['portugues']), 'dia':set(range(2,6+1)), 'duracao':set(range(1,2+1)), 'hora':set(range(8,17+1)), 'tipo':set(['online', 'presencial']), 
    #'name': set(['matematica']), 'dia':set(range(2,6+1)), 'duracao':set(range(1,2+1)), 'hora':set(range(8,17+1)), 'tipo':set(['online', 'presencial']),
    #'name': set(['ingles']), 'dia':set(range(2,6+1)), 'duracao':set(range(1,2+1)), 'hora':set(range(8,17+1)), 'tipo':set(['online', 'presencial'])
    'name1': set(['Portugues']), 'dia1' : set(range(2,6+1)), 'dur1' : set(range(1,2+1)), 'hora1' : set(range(8,17+1)), 'tipo1' : set(['online','presencial']),
    'name2': set(['Matematica']), 'dia2' : set(range(2,6+1)), 'dur2' : set(range(1,2+1)), 'hora2' : set(range(8,17+1)), 'tipo2' : set(['online','presencial']),
    'name3': set(['Ingles']), 'dia3' : set(range(2,6+1)), 'dur3' : set(range(1,2+1)), 'hora3' : set(range(8,17+1)), 'tipo3' : set(['online','presencial']),
    #'name4': set(['lesson4']), 'dia4' : set(range(2,6+1)), 'dur4' : set(range(1,2+1)), 'hora4' : set(range(8,17+1)), 'tipo4' : set(['online','presencial']),
    #'name5': set(['lesson5']), 'dia5' : set(range(2,6+1)), 'dur5' : set(range(1,2+1)), 'hora5' : set(range(8,17+1)), 'tipo5' : set(['online','presencial']),
    #'name6': set(['lesson6']), 'dia6' : set(range(2,6+1)), 'dur6' : set(range(1,2+1)), 'hora6' : set(range(8,17+1)), 'tipo6' : set(['online','presencial']),
    #'name7': set(['lesson7']), 'dia7' : set(range(2,6+1)), 'dur7' : set(range(1,2+1)), 'hora7' : set(range(8,17+1)), 'tipo7' : set(['online','presencial']),
    #'name8': set(['lesson8']), 'dia8' : set(range(2,6+1)), 'dur8' : set(range(1,2+1)), 'hora8' : set(range(8,17+1)), 'tipo8' : set(['online','presencial']),
    #'name9': set(['lesson9']), 'dia9' : set(range(2,6+1)), 'dur9' : set(range(1,2+1)), 'hora9' : set(range(8,17+1)), 'tipo9' : set(['online','presencial']),
    #'name10': set(['lesson10']), 'dia10' : set(range(2,6+1)), 'dur10' : set(range(1,2+1)), 'hora10' : set(range(8,17+1)), 'tipo10' : set(['online','presencial']),
}        

class lesson:
    
    def __init__(self, name ,dia, dur, hora, tipo):
        self.name = name
        self.dia = dia
        self.dur = dur
        self.hora = hora
        self.tipo = tipo

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
              Constraint(tuple(dominio.keys()), teste_condicoes),

              ]

# days_too_short
days_too_short = NaryCSP(dominio, restricoes)
print(days_too_short.variables)

# Result
k = ac_solver(days_too_short, arc_heuristic=sat_up)

print(k)