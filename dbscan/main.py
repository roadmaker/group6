import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import normalize
from sklearn.decomposition import PCA
X = pd.read_csv('./SalesJan2009.csv')

# Dropping the Transaction_date column from the data
X = X.drop('Transaction_date', axis = 1)

X = X.drop('Product', axis = 1)
X = X.drop('Price', axis = 1)
X = X.drop('Payment_Type', axis = 1)
X = X.drop('Name', axis = 1)
X = X.drop('City', axis = 1)
X = X.drop('State', axis = 1)
X = X.drop('Country', axis = 1)
X = X.drop('Account_Created', axis = 1)
X = X.drop('Last_Login', axis = 1)
X = X.drop('US Zip', axis = 1)
# Handling the missing values
X.fillna(method ='ffill', inplace = True)

print(X.head())

# # Scaling the data to bring all the attributes to a comparable level
# scaler = StandardScaler()
# X_scaled = scaler.fit_transform(X)

# # Normalizing the data so that
# # the data approximately follows a Gaussian distribution
# X_normalized = normalize(X_scaled)

# # Converting the numpy array into a pandas DataFrame
# X_normalized = pd.DataFrame(X_normalized)
# pca = PCA(n_components = 2)
# X_principal = pca.fit_transform(X_normalized)
# X_principal = pd.DataFrame(X_principal)
# X_principal.columns = ['P1', 'P2']
# print(X_principal.head())

X_principal = X

X_principal.columns = ['P1', 'P2']
print(X_principal)
# Numpy array of all the cluster labels assigned to each data point
db_default = DBSCAN(eps = 3.75, min_samples = 3).fit(X_principal)
labels = db_default.labels_

# db = DBSCAN(eps = 0.0375, min_samples = 50).fit(X_principal)
# labels1 = db.labels_
# labels.sort()
# print(set(labels))
labels1=labels