import pandas as pd
from sklearn.cluster import KMeans

print("### Months_Inactive_12_mon")

# Carregar os dados
data = pd.read_csv("BankChurners.csv")

#Selecao dos dados para clustering e filtragem por colunas pretendidas
features = ["CLIENTNUM","Customer_Age","Dependent_count","Months_on_book","Total_Relationship_Count","Months_Inactive_12_mon","Contacts_Count_12_mon","Credit_Limit","Total_Revolving_Bal","Avg_Open_To_Buy","Total_Amt_Chng_Q4_Q1","Total_Trans_Amt","Total_Trans_Ct","Total_Ct_Chng_Q4_Q1","Avg_Utilization_Ratio","Naive_Bayes_Classifier_Attrition_Flag_Card_Category_Contacts_Count_12_mon_Dependent_count_Education_Level_Months_Inactive_12_mon_1","Naive_Bayes_Classifier_Attrition_Flag_Card_Category_Contacts_Count_12_mon_Dependent_count_Education_Level_Months_Inactive_12_mon_2"]
print("### FEATURES")
print(features)

X = data[features]
print("### X")
print(X)

print("### KMEANS")

# Treinar modelo K-Means
kmeans = KMeans(n_clusters=2,n_init=1)
kmeans.fit(X)
print(kmeans)

# Atribuir etiquetas do cluster aos dados 
data["cluster"] = kmeans.labels_
print("### Data")
print(data)

# Contabilizar o numero de clientes em cada cluster
cluster_counts = data.groupby("cluster")["Months_Inactive_12_mon"].sum()
print("### Cluster Counts")
print(cluster_counts) 

# Prever clientes baseado no cluster com mais clientes
if cluster_counts[0] > cluster_counts[1]:
    y_pred = 0
else:
    y_pred = 1

# Avaliar precisao
accuracy = (data["Months_Inactive_12_mon"] == y_pred).mean()
print("Accuracy:", accuracy)