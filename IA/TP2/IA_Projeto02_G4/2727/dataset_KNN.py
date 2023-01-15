import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

url = "BankChurners.csv"

abalone = pd.read_csv(url) #, header=None

abalone.columns =["CLIENTNUM","Attrition_Flag","Customer_Age","Gender","Dependent_count","Education_Level","Marital_Status","Income_Category",
                "Card_Category","Months_on_book","Total_Relationship_Count","Months_Inactive_12_mon","Contacts_Count_12_mon","Credit_Limit",
                "Total_Revolving_Bal","Avg_Open_To_Buy","Total_Amt_Chng_Q4_Q1","Total_Trans_Amt","Total_Trans_Ct","Total_Ct_Chng_Q4_Q1",
                "Avg_Utilization_Ratio","Naive_Bayes_Classifier_Attrition_Flag_Card_Category_Contacts_Count_12_mon_Dependent_count_Education_Level_Months_Inactive_12_mon_1",
                "Naive_Bayes_Classifier_Attrition_Flag_Card_Category_Contacts_Count_12_mon_Dependent_count_Education_Level_Months_Inactive_12_mon_2"]

abalone = abalone.drop("Gender", axis=1)

#print(abalone)

#abalone["Avg_Utilization_Ratio"].hist(bins=15)
#plt.show()

#correlation_matrix = abalone.corr()
#correlation_matrix["Avg_Utilization_Ratio"]

a = np.array([5, 2])
b = np.array([6, 4])
np.linalg.norm(a - b)

X = abalone.drop("Avg_Utilization_Ratio", axis=1)
X = X.values
y = abalone["Avg_Utilization_Ratio"]
y = y.values

new_data_point = np.array(([10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,],
                          [10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,]))

distances = np.linalg.norm(X - new_data_point) #, axis=1

k = 3
nearest_neighbor_ids = distances.argsort()[:k]
print(nearest_neighbor_ids)