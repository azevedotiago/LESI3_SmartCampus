import csv
import copy
from collections import defaultdict
from statistics import stdev
from qpsolvers import solve_qp
from probabilistic_learning import NaiveBayesLearner
from utils import *

# Criação da Class DataSet
class DataSet:
    def __init__(self, id=int, name= "", local="", rank=int, des="", tf= int, state="", ue=int):
        self.id = id
        self.name = name
        self.local = local
        self.rank = rank
        self.des = des 
        self.tf = tf
        self.state = state
        self.ue = ue

# Ler ficheiro CSV e guardar os dados num array
def csv_handler(file_name):
    array = []
    with open(file_name, 'r') as csv_file:
        reader = csv.reader(csv_file)
    
        for row in reader:
            data = DataSet(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
            array.append(data)

    return array

# Teste de Leitura do Array
array = csv_handler('National Universities Rankings.csv')
for i in range(len(array)):
    print('ID: ' + array[i].id)
    print('Name: ' + array[i].name)
    print('Location: ' + array[i].local)
    print('Rank: ' + array[i].rank)
    print('Description: ' + array[i].des)
    print('Tuition and Fees: ' + array[i].tf)
    print('In-State: ' + array[i].state)
    print('Undergrad Enrollment: ' + array[i].ue)
    print ('------------------')