# %% [code]
# Importing the Essential Libraries, Metrics

# %% [code] {"execution":{"iopub.status.busy":"2022-10-31T23:10:00.352773Z","iopub.execute_input":"2022-10-31T23:10:00.353203Z","iopub.status.idle":"2022-10-31T23:10:00.363903Z","shell.execute_reply.started":"2022-10-31T23:10:00.353171Z","shell.execute_reply":"2022-10-31T23:10:00.362631Z"}}
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
from sklearn.preprocessing import scale, StandardScaler,LabelEncoder
from sklearn.model_selection import train_test_split, GridSearchCV,cross_val_score
from sklearn.metrics import confusion_matrix, accuracy_score, mean_squared_error, r2_score, roc_auc_score, roc_curve,classification_report
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
import warnings
warnings.filterwarnings("ignore")

# %% [markdown] {"execution":{"iopub.status.busy":"2022-10-31T23:10:00.366198Z","iopub.execute_input":"2022-10-31T23:10:00.366877Z","iopub.status.idle":"2022-10-31T23:10:00.377911Z","shell.execute_reply.started":"2022-10-31T23:10:00.366844Z","shell.execute_reply":"2022-10-31T23:10:00.377112Z"}}
# # Loading the Data

# %% [code] {"execution":{"iopub.status.busy":"2022-10-31T23:10:00.379142Z","iopub.execute_input":"2022-10-31T23:10:00.380109Z","iopub.status.idle":"2022-10-31T23:10:00.439215Z","shell.execute_reply.started":"2022-10-31T23:10:00.380076Z","shell.execute_reply":"2022-10-31T23:10:00.438072Z"}}
df = pd.read_csv("BankChurners.csv")

# %% [markdown]
# ## Feature Selection

# %% [code] {"execution":{"iopub.status.busy":"2022-10-31T23:10:00.441275Z","iopub.execute_input":"2022-10-31T23:10:00.441656Z","iopub.status.idle":"2022-10-31T23:10:00.4481Z","shell.execute_reply.started":"2022-10-31T23:10:00.441618Z","shell.execute_reply":"2022-10-31T23:10:00.446816Z"}}
cols_to_use = ["Attrition_Flag","Customer_Age","Gender","Dependent_count","Education_Level","Marital_Status","Income_Category","Card_Category","Credit_Limit"]

# %% [code] {"execution":{"iopub.status.busy":"2022-10-31T23:10:00.44959Z","iopub.execute_input":"2022-10-31T23:10:00.449919Z","iopub.status.idle":"2022-10-31T23:10:00.461147Z","shell.execute_reply.started":"2022-10-31T23:10:00.449889Z","shell.execute_reply":"2022-10-31T23:10:00.459956Z"}}
df = df[cols_to_use]

# %% [markdown]
# # Exploratory Data Analysis

# %% [markdown] {"execution":{"iopub.status.busy":"2022-10-31T23:11:12.825905Z","iopub.execute_input":"2022-10-31T23:11:12.826344Z","iopub.status.idle":"2022-10-31T23:11:12.833413Z","shell.execute_reply.started":"2022-10-31T23:11:12.82631Z","shell.execute_reply":"2022-10-31T23:11:12.831932Z"}}
# ***Taking a look at the first 5 rows of the dataset***

# %% [code] {"execution":{"iopub.status.busy":"2022-10-31T23:10:00.462703Z","iopub.execute_input":"2022-10-31T23:10:00.463087Z","iopub.status.idle":"2022-10-31T23:10:00.483726Z","shell.execute_reply.started":"2022-10-31T23:10:00.463057Z","shell.execute_reply":"2022-10-31T23:10:00.482625Z"}}
df.head()

# %% [markdown]
# **Checking the shape—i.e. size—of the data**

# %% [code] {"execution":{"iopub.status.busy":"2022-10-31T23:10:00.485271Z","iopub.execute_input":"2022-10-31T23:10:00.486386Z","iopub.status.idle":"2022-10-31T23:10:00.495529Z","shell.execute_reply.started":"2022-10-31T23:10:00.486351Z","shell.execute_reply":"2022-10-31T23:10:00.494649Z"}}
df.shape

# %% [markdown]
# **Learning the dtypes of columns' and how many non-null values are there in those columns**

# %% [code] {"execution":{"iopub.status.busy":"2022-10-31T23:10:00.497028Z","iopub.execute_input":"2022-10-31T23:10:00.497768Z","iopub.status.idle":"2022-10-31T23:10:00.517931Z","shell.execute_reply.started":"2022-10-31T23:10:00.497728Z","shell.execute_reply":"2022-10-31T23:10:00.516634Z"}}
df.info()

# %% [markdown]
# **Getting the statistical summary of dataset**

# %% [code] {"execution":{"iopub.status.busy":"2022-10-31T23:10:00.51956Z","iopub.execute_input":"2022-10-31T23:10:00.5199Z","iopub.status.idle":"2022-10-31T23:10:00.547865Z","shell.execute_reply.started":"2022-10-31T23:10:00.51987Z","shell.execute_reply":"2022-10-31T23:10:00.546971Z"}}
df.describe().T

# %% [markdown]
# **Checking for the missing values**

# %% [code] {"execution":{"iopub.status.busy":"2022-10-31T23:10:00.607529Z","iopub.execute_input":"2022-10-31T23:10:00.60873Z","iopub.status.idle":"2022-10-31T23:10:00.622147Z","shell.execute_reply.started":"2022-10-31T23:10:00.608685Z","shell.execute_reply":"2022-10-31T23:10:00.620995Z"}}
df.isna().sum()

# %% [markdown]
# **Checking for the duplicated values**

# %% [code] {"execution":{"iopub.status.busy":"2022-10-31T23:10:00.624559Z","iopub.execute_input":"2022-10-31T23:10:00.624977Z","iopub.status.idle":"2022-10-31T23:10:00.642459Z","shell.execute_reply.started":"2022-10-31T23:10:00.624938Z","shell.execute_reply":"2022-10-31T23:10:00.641294Z"}}
df.duplicated().sum()

# %% [code] {"execution":{"iopub.status.busy":"2022-10-31T23:10:00.643928Z","iopub.execute_input":"2022-10-31T23:10:00.644235Z","iopub.status.idle":"2022-10-31T23:10:00.658582Z","shell.execute_reply.started":"2022-10-31T23:10:00.644208Z","shell.execute_reply":"2022-10-31T23:10:00.657394Z"}}
df.drop_duplicates(inplace=True)

# %% [code] {"execution":{"iopub.status.busy":"2022-10-31T23:10:00.659526Z","iopub.execute_input":"2022-10-31T23:10:00.659884Z","iopub.status.idle":"2022-10-31T23:10:00.676515Z","shell.execute_reply.started":"2022-10-31T23:10:00.659854Z","shell.execute_reply":"2022-10-31T23:10:00.675512Z"}}
df.duplicated().sum()

# %% [markdown]
# # One-Hot Encoding and Train-Test Split

# %% [markdown]
# * **Encoding the categorical features in X dataset by using One-Hot Encoding method**
# * **Splitting the data into Train and Test chunks for better evaluation**

# %% [code] {"execution":{"iopub.status.busy":"2022-10-31T23:10:00.680217Z","iopub.execute_input":"2022-10-31T23:10:00.681014Z","iopub.status.idle":"2022-10-31T23:10:00.706883Z","shell.execute_reply.started":"2022-10-31T23:10:00.680967Z","shell.execute_reply":"2022-10-31T23:10:00.705844Z"}}
y = df["Attrition_Flag"]
X = df.drop("Attrition_Flag", axis =1)
X = pd.get_dummies(X, columns=["Education_Level","Marital_Status","Income_Category","Card_Category","Gender"])
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

# %% [code] {"execution":{"iopub.status.busy":"2022-10-31T23:10:00.708348Z","iopub.execute_input":"2022-10-31T23:10:00.708763Z","iopub.status.idle":"2022-10-31T23:10:00.728558Z","shell.execute_reply.started":"2022-10-31T23:10:00.708722Z","shell.execute_reply":"2022-10-31T23:10:00.727394Z"}}
X.head()

# %% [code] {"execution":{"iopub.status.busy":"2022-10-31T23:10:00.729944Z","iopub.execute_input":"2022-10-31T23:10:00.730258Z","iopub.status.idle":"2022-10-31T23:10:00.740712Z","shell.execute_reply.started":"2022-10-31T23:10:00.73023Z","shell.execute_reply":"2022-10-31T23:10:00.73971Z"}}
X_train.shape

# %% [code] {"execution":{"iopub.status.busy":"2022-10-31T23:10:00.741944Z","iopub.execute_input":"2022-10-31T23:10:00.742265Z","iopub.status.idle":"2022-10-31T23:10:00.751653Z","shell.execute_reply.started":"2022-10-31T23:10:00.742237Z","shell.execute_reply":"2022-10-31T23:10:00.750617Z"}}
X_test.shape

# %% [markdown]
# # Standardizing the Data
# 

# %% [code] {"execution":{"iopub.status.busy":"2022-10-31T23:10:00.753046Z","iopub.execute_input":"2022-10-31T23:10:00.753354Z","iopub.status.idle":"2022-10-31T23:10:00.761419Z","shell.execute_reply.started":"2022-10-31T23:10:00.753325Z","shell.execute_reply":"2022-10-31T23:10:00.760437Z"}}
scaler = StandardScaler()

# %% [code] {"execution":{"iopub.status.busy":"2022-10-31T23:10:00.762699Z","iopub.execute_input":"2022-10-31T23:10:00.763011Z","iopub.status.idle":"2022-10-31T23:10:00.780099Z","shell.execute_reply.started":"2022-10-31T23:10:00.762983Z","shell.execute_reply":"2022-10-31T23:10:00.778991Z"}}
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# %% [code] {"execution":{"iopub.status.busy":"2022-10-31T23:10:00.7815Z","iopub.execute_input":"2022-10-31T23:10:00.781911Z","iopub.status.idle":"2022-10-31T23:10:00.787072Z","shell.execute_reply.started":"2022-10-31T23:10:00.781871Z","shell.execute_reply":"2022-10-31T23:10:00.785888Z"}}
label = LabelEncoder()

# %% [code] {"execution":{"iopub.status.busy":"2022-10-31T23:10:00.788328Z","iopub.execute_input":"2022-10-31T23:10:00.788661Z","iopub.status.idle":"2022-10-31T23:10:00.800782Z","shell.execute_reply.started":"2022-10-31T23:10:00.788632Z","shell.execute_reply":"2022-10-31T23:10:00.799797Z"}}
y_train =  label.fit_transform(y_train)
y_test = label.transform(y_test)

# %% [markdown]
# # Machine Learning Models

# %% [markdown]
# # Logistic Regression

# %% [code] {"execution":{"iopub.status.busy":"2022-10-31T23:10:00.801779Z","iopub.execute_input":"2022-10-31T23:10:00.802104Z","iopub.status.idle":"2022-10-31T23:10:00.851109Z","shell.execute_reply.started":"2022-10-31T23:10:00.802075Z","shell.execute_reply":"2022-10-31T23:10:00.849954Z"}}
loj_model = LogisticRegression(solver="liblinear").fit(X_train,y_train)

# %% [code] {"execution":{"iopub.status.busy":"2022-10-31T23:10:00.856022Z","iopub.execute_input":"2022-10-31T23:10:00.856484Z","iopub.status.idle":"2022-10-31T23:10:00.868563Z","shell.execute_reply.started":"2022-10-31T23:10:00.856432Z","shell.execute_reply":"2022-10-31T23:10:00.867221Z"}}
y_pred = loj_model.predict(X_test)

# %% [code] {"execution":{"iopub.status.busy":"2022-10-31T23:10:00.870965Z","iopub.execute_input":"2022-10-31T23:10:00.871744Z","iopub.status.idle":"2022-10-31T23:10:00.882483Z","shell.execute_reply.started":"2022-10-31T23:10:00.871701Z","shell.execute_reply":"2022-10-31T23:10:00.881377Z"}}
accuracy_score(y_test,y_pred)

# %% [markdown]
# ## Model Tuning

# %% [code] {"execution":{"iopub.status.busy":"2022-10-31T23:10:00.884306Z","iopub.execute_input":"2022-10-31T23:10:00.885141Z","iopub.status.idle":"2022-10-31T23:10:00.954979Z","shell.execute_reply.started":"2022-10-31T23:10:00.885099Z","shell.execute_reply":"2022-10-31T23:10:00.953353Z"}}
loj_model = LogisticRegression(solver="liblinear").fit(X_train,y_train)

# %% [code] {"execution":{"iopub.status.busy":"2022-10-31T23:10:00.956893Z","iopub.execute_input":"2022-10-31T23:10:00.957559Z","iopub.status.idle":"2022-10-31T23:10:00.969148Z","shell.execute_reply.started":"2022-10-31T23:10:00.957516Z","shell.execute_reply":"2022-10-31T23:10:00.96726Z"}}
y_pred = loj_model.predict(X_test)

# %% [code] {"execution":{"iopub.status.busy":"2022-10-31T23:10:00.971164Z","iopub.execute_input":"2022-10-31T23:10:00.971997Z","iopub.status.idle":"2022-10-31T23:10:01.157631Z","shell.execute_reply.started":"2022-10-31T23:10:00.971943Z","shell.execute_reply":"2022-10-31T23:10:01.156508Z"}}
cross_val_score(loj_model,X_test,y_test,cv=10).mean()

# %% [markdown]
# # KNN

# %% [code] {"execution":{"iopub.status.busy":"2022-10-31T23:10:01.159296Z","iopub.execute_input":"2022-10-31T23:10:01.159728Z","iopub.status.idle":"2022-10-31T23:10:01.167465Z","shell.execute_reply.started":"2022-10-31T23:10:01.159694Z","shell.execute_reply":"2022-10-31T23:10:01.166384Z"}}
knn_model = KNeighborsClassifier().fit(X_train,y_train)

# %% [code] {"execution":{"iopub.status.busy":"2022-10-31T23:18:21.755356Z","iopub.execute_input":"2022-10-31T23:18:21.755778Z","iopub.status.idle":"2022-10-31T23:18:22.331104Z","shell.execute_reply.started":"2022-10-31T23:18:21.755746Z","shell.execute_reply":"2022-10-31T23:18:22.329975Z"}}
y_pred = knn_model.predict(X_test)

# %% [code] {"execution":{"iopub.status.busy":"2022-10-31T23:10:01.672353Z","iopub.status.idle":"2022-10-31T23:10:01.67274Z","shell.execute_reply.started":"2022-10-31T23:10:01.67254Z","shell.execute_reply":"2022-10-31T23:10:01.672557Z"}}
accuracy_score(y_test,y_pred)

# %% [markdown]
# ## Model Tuning

# %% [code] {"execution":{"iopub.status.busy":"2022-10-31T23:10:01.6744Z","iopub.status.idle":"2022-10-31T23:10:01.675241Z","shell.execute_reply.started":"2022-10-31T23:10:01.675038Z","shell.execute_reply":"2022-10-31T23:10:01.675059Z"}}
knn = KNeighborsClassifier()

# %% [code] {"execution":{"iopub.status.busy":"2022-10-31T23:10:01.676416Z","iopub.status.idle":"2022-10-31T23:10:01.677758Z","shell.execute_reply.started":"2022-10-31T23:10:01.677413Z","shell.execute_reply":"2022-10-31T23:10:01.677446Z"}}
knn_params = {"n_neighbors": np.arange(1,50)}

# %% [code] {"execution":{"iopub.status.busy":"2022-10-31T23:10:01.679027Z","iopub.status.idle":"2022-10-31T23:10:01.6799Z","shell.execute_reply.started":"2022-10-31T23:10:01.679608Z","shell.execute_reply":"2022-10-31T23:10:01.679637Z"}}
knn_cv_model = GridSearchCV(knn,knn_params, cv=10).fit(X_train,y_train)

# %% [code] {"execution":{"iopub.status.busy":"2022-10-31T23:10:01.681596Z","iopub.status.idle":"2022-10-31T23:10:01.682388Z","shell.execute_reply.started":"2022-10-31T23:10:01.682081Z","shell.execute_reply":"2022-10-31T23:10:01.682108Z"}}
knn_cv_model.best_score_

# %% [code] {"execution":{"iopub.status.busy":"2022-10-31T23:10:01.68352Z","iopub.status.idle":"2022-10-31T23:10:01.684327Z","shell.execute_reply.started":"2022-10-31T23:10:01.68412Z","shell.execute_reply":"2022-10-31T23:10:01.684141Z"}}
knn_cv_model.best_params_

# %% [code] {"execution":{"iopub.status.busy":"2022-10-31T23:10:01.685624Z","iopub.status.idle":"2022-10-31T23:10:01.685982Z","shell.execute_reply.started":"2022-10-31T23:10:01.685804Z","shell.execute_reply":"2022-10-31T23:10:01.685822Z"}}
knn_tuned =  KNeighborsClassifier(n_neighbors=20).fit(X_train,y_train)

# %% [code] {"execution":{"iopub.status.busy":"2022-10-31T23:10:01.687978Z","iopub.status.idle":"2022-10-31T23:10:01.688803Z","shell.execute_reply.started":"2022-10-31T23:10:01.68848Z","shell.execute_reply":"2022-10-31T23:10:01.68851Z"}}
y_pred = knn_model.predict(X_test)

# %% [code] {"execution":{"iopub.status.busy":"2022-10-31T23:10:01.690041Z","iopub.status.idle":"2022-10-31T23:10:01.691243Z","shell.execute_reply.started":"2022-10-31T23:10:01.690937Z","shell.execute_reply":"2022-10-31T23:10:01.690964Z"}}
accuracy_score(y_test,y_pred)

# %% [markdown]
# # SVM

# %% [code] {"execution":{"iopub.status.busy":"2022-10-31T23:10:01.692468Z","iopub.status.idle":"2022-10-31T23:10:01.693608Z","shell.execute_reply.started":"2022-10-31T23:10:01.693294Z","shell.execute_reply":"2022-10-31T23:10:01.693322Z"}}
svm_model = SVC(kernel="linear").fit(X_train,y_train)

# %% [code] {"execution":{"iopub.status.busy":"2022-10-31T23:10:01.694853Z","iopub.status.idle":"2022-10-31T23:10:01.695904Z","shell.execute_reply.started":"2022-10-31T23:10:01.695603Z","shell.execute_reply":"2022-10-31T23:10:01.695632Z"}}
y_pred = svm_model.predict(X_test)

# %% [code] {"execution":{"iopub.status.busy":"2022-10-31T23:10:01.697485Z","iopub.status.idle":"2022-10-31T23:10:01.697865Z","shell.execute_reply.started":"2022-10-31T23:10:01.697687Z","shell.execute_reply":"2022-10-31T23:10:01.697704Z"}}
accuracy_score(y_test,y_pred)

# %% [markdown]
# ## Model Tuning

# %% [code] {"execution":{"iopub.status.busy":"2022-10-31T23:10:01.699543Z","iopub.status.idle":"2022-10-31T23:10:01.700359Z","shell.execute_reply.started":"2022-10-31T23:10:01.700072Z","shell.execute_reply":"2022-10-31T23:10:01.7001Z"}}
svm = SVC()

# %% [code] {"execution":{"iopub.status.busy":"2022-10-31T23:10:01.701605Z","iopub.status.idle":"2022-10-31T23:10:01.702693Z","shell.execute_reply.started":"2022-10-31T23:10:01.70238Z","shell.execute_reply":"2022-10-31T23:10:01.702408Z"}}
svm_params  = { "C": np.arange(1,10),
               "kernel":["linear","rbf"]}

# %% [code] {"execution":{"iopub.status.busy":"2022-10-31T23:10:01.70393Z","iopub.status.idle":"2022-10-31T23:10:01.704973Z","shell.execute_reply.started":"2022-10-31T23:10:01.70476Z","shell.execute_reply":"2022-10-31T23:10:01.704783Z"}}
svm_cv_model = GridSearchCV(svm,svm_params,cv=10, n_jobs=-1, verbose=2).fit(X_train,y_train)

# %% [code] {"execution":{"iopub.status.busy":"2022-10-31T23:10:01.706187Z","iopub.status.idle":"2022-10-31T23:10:01.706689Z","shell.execute_reply.started":"2022-10-31T23:10:01.706389Z","shell.execute_reply":"2022-10-31T23:10:01.706408Z"}}
svm_cv_model.best_params_

# %% [code] {"execution":{"iopub.status.busy":"2022-10-31T23:10:01.708768Z","iopub.status.idle":"2022-10-31T23:10:01.709181Z","shell.execute_reply.started":"2022-10-31T23:10:01.708985Z","shell.execute_reply":"2022-10-31T23:10:01.709005Z"}}
svm_tuned  = SVC(C=1, kernel='linear').fit(X_train,y_train)

# %% [code] {"execution":{"iopub.status.busy":"2022-10-31T23:10:01.711691Z","iopub.status.idle":"2022-10-31T23:10:01.71274Z","shell.execute_reply.started":"2022-10-31T23:10:01.71246Z","shell.execute_reply":"2022-10-31T23:10:01.712498Z"}}
y_pred = svm_tuned.predict(X_test)

# %% [code] {"execution":{"iopub.status.busy":"2022-10-31T23:10:01.714125Z","iopub.status.idle":"2022-10-31T23:10:01.714966Z","shell.execute_reply.started":"2022-10-31T23:10:01.714754Z","shell.execute_reply":"2022-10-31T23:10:01.714776Z"}}
accuracy_score(y_test,y_pred)

# %% [code]