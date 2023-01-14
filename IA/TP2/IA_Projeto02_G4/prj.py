# Import libraries and classes required for this example:
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler 
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, confusion_matrix
from tabulate import tabulate

import pandas as pd 

def table_print(title,a):
    print(title)
    print(tabulate(a, headers = 'keys', tablefmt = 'psql'))

def mapear(input, columns):
    d = pd.DataFrame({})
    for c in columns:
        d.insert(len(d.columns),c,pd.Series(input[c].unique()))
    return d

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
    
# Import dataset:
url = "BankChurners.csv"
url_teste = "BankChurnersTestFiltrado.csv"
url_output = "BankChurnersTestOutput.csv"

# Convert dataset to a pandas dataframe:
dataset = pd.read_csv(url) 


colunas = dataset.columns.size

vars = dataset["Income_Category"].unique().tolist()
tabela_mapeamento = mapear(dataset, ["Education_Level", "Attrition_Flag","Gender",  "Marital_Status", "Income_Category", "Card_Category"])

table_print("Tabela de mapeamento",tabela_mapeamento)

dataset = tabela_normalizar(tabela_mapeamento,dataset)

#Remover o numero de clientes que nao e variaveis
numero_clientes = dataset.pop("CLIENTNUM")
colunas = colunas - 1

cat_move = dataset.pop("Income_Category")
colunas = colunas - 1
dataset.insert(len(dataset.columns),"Income_Category",cat_move)

# Use head() function to return the first 5 rows: 
dataset.head() 
# Assign values to the X and y variables:
X = dataset.iloc[:, :-1].values
y = dataset.iloc[:, len(dataset.columns)-1].values 

# Split dataset into random train and test subsets:
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=None) 

# Standardize features by removing mean and scaling to unit variance:
scaler = StandardScaler()
scaler.fit(X_train)

X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test) 

# Use the KNN classifier to fit data:
classifier = KNeighborsClassifier(n_neighbors=5)
classifier.fit(X_train, y_train) 

# Predict y data with classifier: 
y_predict = classifier.predict(X_test)

# Print results: 
#print(confusion_matrix(y_test, y_predict))
print("Analise estatica de classificacao do algoritmo: ")
print(classification_report(y_test, y_predict, target_names=vars)) 


dataset_teste = pd.read_csv(url_teste,delimiter=";")
dataset_teste = tabela_normalizar(tabela_mapeamento,dataset_teste)

X_teste = dataset_teste.iloc[:, :].values

y_teste_predict = classifier.predict(X_teste)

# todo mover
#dataset_teste.insert(len(dataset_teste.columns),"Income_Category",y_teste_predict)
#dataset_teste = tabela_normalizar(tabela_mapeamento,dataset_teste,tipo=False)
#income_predict_tmp = dataset.pop("Income_Category")

#dataset_teste.insert(len(dataset_teste.columns),"Income_Category",y)
#income_original_tmp = dataset.pop("Income_Category")

dataset_teste.insert(len(dataset_teste.columns),"Income_Category_predict",y_teste_predict)
dataset_teste.insert(len(dataset_teste.columns),"Income_Category_original",y)


table_print("Dataset Final", dataset_teste)
dataset_teste.to_csv(url_output)