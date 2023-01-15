from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler 
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, confusion_matrix
from tabulate import tabulate
import pandas as pd 

#Exempo utilizado para base: https://www.activestate.com/resources/quick-reads/how-to-classify-data-in-python/

#Funcao para imprimir tabela na consola
def table_print(title,a):
    print(title)
    print(tabulate(a, headers = 'keys', tablefmt = 'psql'))

#Funcao para construir tabela de mapeamento int->string
def mapear(input, columns):
    d = pd.DataFrame({})
    for c in columns:
        d.insert(len(d.columns),c,pd.Series(input[c].unique()))
    return d

#Funcao para normalizar os valores de uma tabela
# Se Tipo = true -> Converte de string para inteiro (usando a tabela de mapeamento)
# Se Tipo = false -> Converte de inteiro para string (usando a tabela de mapeamento)
def tabela_normalizar(tabela_mapeamento, tabela, tipo=True):
    for c in tabela_mapeamento:
        if c in tabela.columns:
            for i, row in tabela_mapeamento.iterrows():
                campo = row[c]
                if campo != None:
                    if(tipo == True):
                        tabela[c] = tabela[c].replace(campo,i)
                    else:
                        tabela[c] = tabela[c].replace(i,campo)
    
    return tabela

#Funcao para normalizar campos que tem nomes diferentes da tabela de mapeamento (mas que usam o mapa de um campo existente)
# So funciona em mapeamentos de string para int
def tabela_normalizar_novoCampo(tabela_mapeamento,dataset,novoCampo, campoSupostoMapa):
        novo = dataset.pop(novoCampo)
        dataset.insert(len(dataset.columns),campoSupostoMapa,novo)
        dataset = tabela_normalizar(tabela_mapeamento,dataset,tipo=False)
        novo = dataset.pop(campoSupostoMapa)
        dataset.insert(len(dataset.columns),novoCampo,novo)
        return dataset

# Funcao para calcular a estatistica de campos previstos vs original
def estatistica_final(df,campoOriginal,campoEstimado):
    iguais = 0
    diferentes = 0
    for index, row in df.iterrows():
        if row[campoOriginal] == row[campoEstimado]:
            iguais = iguais + 1
        else:
            diferentes = diferentes + 1
    print("Absoluto:")
    print("\tIguais: " + str(iguais))
    print("\tdiferentes: " + str(diferentes))
    print("\tTotal: " + str(iguais+diferentes))
    print("Estatistico:")
    print("\tIguais: " + str(iguais/(iguais+diferentes) * 100) + " %")
    print("\tdiferentes: " + str(diferentes/(iguais+diferentes) * 100) + " %" )

# Inicio do programa:

# Import dataset:
# Dataset original
url = "BankChurners.csv"

# Ficheiro de output (resultado)
url_output = "BankChurnersTestOutput.csv"

campo_estimar = "Attrition_Flag"
variaveis_ignorar = ["CLIENTNUM",]

# Ler dataset original
dataset = pd.read_csv(url) 
colunas = dataset.columns.size

# Retirar o campo a estimar
vars = dataset[campo_estimar].unique().tolist()

# Lista de campos que precisam de ser convertidas de String para Int 
tabela_mapeamento = mapear(dataset, ["Education_Level", "Attrition_Flag","Gender",  "Marital_Status", "Income_Category", "Card_Category"])

# Tabela de mapeamento String -> Int
table_print("Tabela de mapeamento",tabela_mapeamento)

# Normalizar tabela original de Int para string
dataset = tabela_normalizar(tabela_mapeamento,dataset)

#Remover o numero de clientes que nao e variaveis
for x in variaveis_ignorar:
    dataset.pop(x)
    colunas = colunas - 1

# Retirar o campo a estimar do dataset que vai ser processado pelo algorimto
cat_move = dataset.pop(campo_estimar)
colunas = colunas - 1

# Mover campo a estimar para o final, para ser compativel com codigo do algoritmo
dataset.insert(len(dataset.columns),campo_estimar,cat_move)

# ------------------------------------------------------------------------------------------------------
# ----------INICIO--------------------------------------------------------------------------------------
# Execucao algortimo -> https://www.activestate.com/resources/quick-reads/how-to-classify-data-in-python/


# Usar a funcao head() para retornar as primeiras 5 linhas
dataset.head() 

# Atribuir os valores a X e a Y
X = dataset.iloc[:, :-1].values
y = dataset.iloc[:, len(dataset.columns)-1].values 

#Dividir o dataset em subdatasets de teste e de treino aleatorio
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=None) 

# Normalizar os recursos removendo a media e o escalonamento para a variacao da unidade
scaler = StandardScaler()
scaler.fit(X_train)

X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test) 

# Usar o classificador KNN para corresponder aos dados
classifier = KNeighborsClassifier(n_neighbors=5)
classifier.fit(X_train, y_train) 
 
# Previsão dos dados em Y com classificador
y_predict = classifier.predict(X_test)

# ------------------------------------------------------------------------------------------------------
# ----------FIM-----------------------------------------------------------------------------------------
# Execucao algortimo -> https://www.activestate.com/resources/quick-reads/how-to-classify-data-in-python/

# Output dos resultados 
print("Execucao do algoritmo: ")
print("Confusion Matrix: ")
print(confusion_matrix(y_test, y_predict))
print("Report de Classicacao: ")
print(classification_report(y_test, y_predict, target_names=vars)) 

# Iniciar um teste de previsao, com um csv que nao tenha 
dataset_teste = pd.read_csv(url)

# Filtrar campos que vao estimados e ignorados
for x in variaveis_ignorar:
    dataset_teste.pop(x)

# Retirar campo a estimar
dataset_teste.pop(campo_estimar)

# Normalizar valores da tabela a ser estimada
dataset_teste = tabela_normalizar(tabela_mapeamento,dataset_teste)

# Executar algortimo de previsao
X_teste = dataset_teste.iloc[:, :].values
y_teste_predict = classifier.predict(X_teste)

# Adicionar resultado, Campo previsto
dataset_teste.insert(len(dataset_teste.columns),campo_estimar+"_predict",y_teste_predict)
dataset_teste = tabela_normalizar_novoCampo(tabela_mapeamento,dataset_teste,campo_estimar+"_predict",campo_estimar)

# Adicionar resultado, Campo original
dataset_teste.insert(len(dataset_teste.columns),campo_estimar+"_original",y)
dataset_teste = tabela_normalizar_novoCampo(tabela_mapeamento,dataset_teste,campo_estimar+"_original",campo_estimar)

# Converter resultado de todas os campos para string
dataset_teste = tabela_normalizar(tabela_mapeamento,dataset_teste,tipo=False)

#table_print("Dataset Final", dataset_teste)

# Escrever o excel
dataset_teste.to_csv(url_output)

# Escrever estatistica de resultados
print("Estatistica final de resultados: ")
estatistica_final(dataset_teste,campo_estimar+"_predict",campo_estimar+"_original")