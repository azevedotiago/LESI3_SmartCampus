import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
from apyori import apriori

# Carregamento de dados
data = pd.read_csv("BankChurners.csv")
data = data.dropna() # eliminar registos com dados incompletos
data = pd.get_dummies(data) # Conversao de variaveis 

# Explorar analise de dados 
data.hist(bins=50, figsize=(20,15))
plt.show()

# Aplicar o clustering de K-Means
kmeans = KMeans(n_clusters=3, random_state=0).fit(data)
data["cluster"] = kmeans.labels_

# Aplicar as regras de associacao para tratamento dos dados com base no metodo Apriori
transactions = data.groupby(["cluster"]).agg(lambda x: x.tolist())["CLIENTNUM"]
rules = apriori(transactions, min_support=0.3, min_confidence=0.8)

# Construir e treinar o classificador Naive Bayes
x = data.drop(columns=["CLIENTNUM", "Months_Inactive_12_mon"])
y = data["Months_Inactive_12_mon"]

classifier = GaussianNB()
classifier.fit(x, y)

# Fazer previsoes 
predictions = classifier.predict(x)
print("\n### PREDICTIONS:")
print(predictions)

# Precisao da avalicao do modelo
accuracy = accuracy_score(y, predictions)
print("Accuracy: ", accuracy)