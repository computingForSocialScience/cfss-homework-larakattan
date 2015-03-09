import sys
from artistNetworks import *
from analyzeNetworks import *
from fetchArtist import *

import requests 
import pandas as pd
import numpy as np 
import unicodecsv 
from io import open

if __name__ == '__main__':
    artist_names = sys.argv[1:]
    print ("input artists are ", artist_names)

def fetchRandomAlbum(artistID):

	req = requests.get("https://api.spotify.com/v1/artists/"+artistID+"/albums?album_type=album")
	albums = req.json()

	albums_list = []

	if len(albums['items'])==0: 
		print ("Oops, bad artist ID given to getRandomAlbum().")
		return ('')
	else:
		for i in range(len(albums['items'])):
			albums_list.append((albums['items'][i]['id'],albums['items'][i]['name']))

	return albums_list[np.random.choice(len(albums_list))]

def fetchRandomTrack(albumID):

	req = requests.get("https://api.spotify.com/v1/albums/"+albumID+"/tracks")
	tracks = req.json()

	if len(tracks)==0: return('')

	track_list = []

	for i in range(len(tracks['items'])):
		track_list.append(tracks['items'][i]['name'])

	return np.random.choice(track_list)

def fetchArtistName(artistID):

	req = requests.get("https://api.spotify.com/v1/artists/"+artistID)
	artist_info = req.json()

	return (artist_info['name'])


