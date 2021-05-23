import numpy as np
import pandas as pd
# import matplotlib.pyplot as plt
import psycopg2
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import normalize
from sklearn.decomposition import PCA
from flask import Flask
def cluster():

	connection = psycopg2.connect(user="postgres",
	                                  password="postgres",
	                                  host="172.17.0.2",
	                                  port="5432",
	                                  database="roadmakerDB")
	cursor = connection.cursor()
	sql_select_query = """SELECT latitude,longitude,hash FROM hash_location Where latitude!='not found'"""
	cursor.execute(sql_select_query)
	record = cursor.fetchall()


	X=record

	X_normalized=X

	# Converting the numpy array into a pandas DataFrame
	X_normalized = pd.DataFrame(X_normalized)
	X_normalized = X_normalized.drop(2, axis = 1)
	pca = PCA(n_components = 2)
	X_principal = X_normalized
	X_principal = pd.DataFrame(X_principal)
	X_principal.columns = ['Latitude', 'Longitude']
	# print(X_principal.head())
	# Numpy array of all the cluster labels assigned to each data point

	db_default = DBSCAN(eps = 0.0375, min_samples = 2).fit(X_principal)
	labels = db_default.labels_
	# print(labels)
	out={}
	img=[]
	for i in range(len(labels)):
		if(labels[i] in out):
			out[labels[i]] +=1
		else:
			out[labels[i]]=1
			img.append(record[i])
		# out.append([labels[i],X[i]])
	# print(record)
	# print(out)

	for k in out:
		# print(k,out[k])
		# print(img[k][2])
		# print(str(k), str(out[k]),str(img[k][2]))
		try:
			sql_update_query = """insert into public.accounts_clusters(cluster,frequency,image_hash,status,updated_image,lat,lon) values(%s,%s,%s,'NA','NA',%s,%s)"""
			cursor.execute(sql_update_query, (str(k), str(out[k]),str(img[k][2]),str(img[k][0]),str(img[k][1])))
			connection.commit()
		except (Exception, psycopg2.Error) as error:
			print("Error in update operation", error)
server = Flask(__name__)

@server.route("/")
def hello():
	cluster()
	return "Clustered"

if __name__ == "__main__":
	server.run(host='0.0.0.0')

# cluster_afterVerify()
#######################################################################################
# # Building the label to colour mapping
# colours = {}
# colours[0] = 'r'
# colours[1] = 'g'
# colours[2] = 'b'
# colours[-1] = 'k'

# # Building the colour vector for each data point
# cvec = [colours[label] for label in labels]

# # For the construction of the legend of the plot
# r = plt.scatter(X_principal['Latitude'], X_principal['Longitude'], color ='r');
# g = plt.scatter(X_principal['Latitude'], X_principal['Longitude'], color ='g');
# b = plt.scatter(X_principal['Latitude'], X_principal['Longitude'], color ='b');
# k = plt.scatter(X_principal['Latitude'], X_principal['Longitude'], color ='k');

# # Plotting Latitude on the X-Axis and Longitude on the Y-Axis
# # according to the colour vector defined
# plt.figure(figsize =(9, 9))
# plt.scatter(X_principal['Latitude'], X_principal['Longitude'], c = cvec)

# # Building the legend
# plt.legend((r, g, b, k), ('Label 0', 'Label 1', 'Label 2', 'Label -1'))

# plt.show()
#######################################################################################