import networkx as nx 
import numpy as np 
import pandas as pd 

def readEdgeList(filename):

	df = pd.read_csv(filename) # create a dataframe from the passed in CSV file 

	if (len(df.columns)) != 2: # check that the filename includes only two columns; return error if != 2
		print ("Warning, the CSV passed to readEdgeList() does not have exactly two columns. Extra columns have been dropped.")
		df = df.drop(df.columns[2:len(df.columns)],axis=1) # drop columns after the first two 
		#  need axis = 1 to know to drop columns, not rows 
		# remember that dataframes are indexed from 0 

	return (df)

def degree(edgeList, in_or_out):

	if in_or_out == "in":
		return edgeList.ix[:,1].value_counts()
	elif in_or_out == "out":
		return edgeList.ix[:,0].value_counts()
	else:
		print ("Oops, degrees() needs the second argument to be either 'in' or 'out'.")

	return

def combineEdgeLists(edgeList1, edgeList2):
	
	return pd.merge(edgeList1,edgeList2,how='outer').drop_duplicates()

def pandasToNetworkX(edgeList):

	graph = nx.DiGraph()

	for i,j in edgeList.to_records(index=False):
		graph.add_edge(i,j)

	return (graph)

def randomCentralNode(inputDiGraph):

	eigenval = nx.eigenvector_centrality(inputDiGraph)

	total = sum(eigenval.values())

	for i in eigenval:
		eigenval[i]=eigenval[i]/float(total)

	return (np.random.choice(eigenval.keys(), p = eigenval.values()))