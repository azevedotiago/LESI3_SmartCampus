import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score

#Loading and cleaning the data
data = pd.read_csv("BankChurners.csv")
data = data.dropna() # drop rows with missing values
data = pd.get_dummies(data) # convert categorical variables to one-hot encoded variables

#Exploratory Data Analysis
#import matplotlib.pyplot as plt
#data.hist(bins=50, figsize=(20,15))
#plt.show()

#Applying k-means clustering
kmeans = KMeans(n_clusters=3, random_state=0).fit(data)
data["cluster"] = kmeans.labels_

#Applying association rule mining (you can use apyori library)
from apyori import apriori
transactions = data.groupby(["cluster"]).agg(lambda x: x.tolist())["CLIENTNUM"]
rules = apriori(transactions, min_support=0.3, min_confidence=0.8)

#Building and training the Naive Bayes classifier
x = data.drop(columns=["CLIENTNUM", "Months_Inactive_12_mon"])
y = data["Months_Inactive_12_mon"]

classifier = GaussianNB()
classifier.fit(x, y)

#Making predictions
predictions = classifier.predict(x)
print("\n### PREDICTIONS:")
print(predictions)

#Evaluating the model
accuracy = accuracy_score(y, predictions)
print("Accuracy: ", accuracy)

