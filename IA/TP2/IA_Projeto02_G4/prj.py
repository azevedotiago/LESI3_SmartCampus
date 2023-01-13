# Import libraries and classes required for this example:
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler 
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, confusion_matrix
from tabulate import tabulate

import pandas as pd 

def table_print(a):
    print(tabulate(a, headers = 'keys', tablefmt = 'psql'))

def normalizar(input, columns):
    d = pd.DataFrame({})
    for c in columns:
        d.insert(len(d.columns),c,pd.Series(input[c].unique()))
        
    table_print(d)      
    exit() 
    
    
# Import dataset:
url = "C:\LESI3_SmartCampus\IA\TP2\IA_Projeto02_G4\BankChurners.csv"

# Convert dataset to a pandas dataframe:
dataset = pd.read_csv(url) 

normalizar(dataset, ["Education_Level", "Attrition_Flag","Gender",  "Marital_Status", "Income_Category", "Card_Category"])
exit
cat_move = dataset.pop("Income_Category")
dataset.insert(len(dataset.columns),"Income_Category",cat_move)

# Use head() function to return the first 5 rows: 
dataset.head() 
# Assign values to the X and y variables:
X = dataset.iloc[:, :-1].values
y = dataset.iloc[:, len(dataset.columns)-1].values 

# Split dataset into random train and test subsets:
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20) 

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
print(confusion_matrix(y_test, y_predict))
print(classification_report(y_test, y_predict)) 