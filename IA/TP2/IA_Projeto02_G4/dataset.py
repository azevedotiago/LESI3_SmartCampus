import csv
from collections import defaultdict
from statistics import stdev
from qpsolvers import solve_qp

# Criação da Class DataSet
class DataSet:
    def __init__(self, numc=int, tpc= "", idade=int, gen="", dep=int, edu="", civil="", sal="", cart="", 
                meses=int, tr=int, inat=int, contactos=int, lc=int, baltot=int, medcomp=int, mudtot=float, 
                tottrans=int, tottransct=int, mudtotct=float, utracio=float, nb1=float, nb2=float):
        self.numc = numc
        self.tpc = tpc
        self.idade = idade
        self.gen = gen
        self.dep = dep
        self.edu = edu
        self.civil = civil
        self.sal = sal
        self.cart = cart
        self.meses = meses
        self.tr = tr
        self.inat = inat
        self.contactos = contactos
        self.lc = lc
        self.baltot = baltot
        self.medcomp = medcomp
        self.mudtot = mudtot
        self.tottrans = tottrans
        self.tottransct = tottransct
        self.mudtotct = mudtotct
        self.utracio = utracio
        self.nb1 = nb1
        self.nb2 = nb2

# Ler ficheiro CSV e guardar os dados num array
def csv_handler(file_name):
    array = []
    with open(file_name, 'r') as csv_file:
        reader = csv.reader(csv_file)
    
        for row in reader:
            data = DataSet(row[0 ], row[1 ], row[2 ], row[3 ], row[4 ], row[5 ], 
                           row[6 ], row[7 ], row[8 ], row[9 ], row[10], row[11], 
                           row[12], row[13], row[14], row[15], row[16], row[17], 
                           row[18], row[19], row[20], row[21], row[22])
            array.append(data)

    return array

# Teste de Leitura do Array
array = csv_handler('BankChurners.csv')
for i in range(len(array)):
    print('Nr Cliente: ' + array[i].numc)
    print('Tipo Cliente: ' + array[i].tpc)
    print('Idade: ' + array[i].idade)
    print('Genero: ' + array[i].gen)
    print('Nr Dependentes: ' + array[i].dep)
    print('Nivel Educacao: ' + array[i].edu)
    print('Estado Civil: ' + array[i].civil)
    print('Intervalo Salarial: ' + array[i].sal)
    print('Tipo Cartao: ' + array[i].cart)
    print('Nr Meses Cliente: ' + array[i].meses)
    print('Total Relacao: ' + array[i].tr)
    print('Nr Meses inativo: ' + array[i].inat)
    print('Nr Contactos feitos: ' + array[i].contactos)
    print('Limite Cartao: ' + array[i].lc)
    print('Balanco Total: ' + array[i].baltot)
    print('Media Compra: ' + array[i].medcomp)
    print('Valor mudado (Q4-Q1): ' + array[i].mudtot)
    print('Valor Transferido Total: ' + array[i].tottrans)
    print('Valor Vezes Transferido: ' + array[i].tottransct)
    print('Valor Vezes Transferido (Q4-Q1): ' + array[i].mudtotct)
    print('Racio de Utilizacao: ' + array[i].utracio)
    print('Naive Bays 1: ' + array[i].nb1)
    print('Naive Bays 2: ' + array[i].nb2)
    print ('------------------')