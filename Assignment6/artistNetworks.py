import requests
import pandas as pd
import numpy as np
from fetchArtist import *

def getRelatedArtists(artistID):
	'''done'''

	req = requests.get("https://api.spotify.com/v1/artists/"+artistID+"/related-artists")
	related = req.json()

	related_artists = []

	for i in range(len(related['artists'])):
		related_artists.append(related['artists'][i]['id'])

	return(related_artists) 


def getDepthEdges(artistID, depth):
	'''return a list of tuples representing the directed pairs of related
	artists. Search 'depth' number of iterations into the network.'''
	
	if depth <= 0: # there has to be some depth, otherwise can't create network
		# print("Oops, passed a negative depth to getDepthEdges()")
		return ('')

	related_artists = getRelatedArtists(artistID)
	
	edges = [] # where we'll hold all edges that we'll eventually return
	next_iteration_artists = []

	for artist in related_artists: # first iteration
		edges.append((artistID,artist)) # need a set of artists to begin 

	counter = 1

	while counter < depth:

		for artist in related_artists:
			sub_related_artists = getRelatedArtists(artist)
			for sub_artist in sub_related_artists:
				edges.append((artist,sub_artist))
				next_iteration_artists.append(sub_artist)

		related_artists = next_iteration_artists
		next_iteration_artists = []
		counter+=1 

	return list(set(edges))

def getEdgeList(artistID, depth):
	'''load getDepthEdges into a pandas dataFrame'''

	edges_array = np.asarray(getDepthEdges(artistID,depth)) #use numpy to create an array

	return (pd.DataFrame(edges_array)) # turn the numpy array into a pandas dataframe 

def writeEdgeList(artistID, depth, filename):

	getEdgeList(artistID,depth).to_csv(filename,index=False)

	return 