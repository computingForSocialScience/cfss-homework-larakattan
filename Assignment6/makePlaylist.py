import sys
from artistNetworks import *
from analyzeNetworks import *
from fetchArtist import *
from tests import * 
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


artists_network = getEdgeList(fetchArtistId(artist_names[0]),2)

for artist in artist_names:
	artists_network = combineEdgeLists(artists_network,getEdgeList(fetchArtistId(artist),2))


full_network = pandasToNetworkX(artists_network)

playlist_artists = []

count = 1 
while count <= 30:
	playlist_artists.append(randomCentralNode(full_network))
	count+=1

playlist = []
randomAlbum = ''
randomTrack = ''
artist_name = ''

for artist in playlist_artists:
	randomAlbum = fetchRandomAlbum(artist)
	randomTrack = fetchRandomTrack(randomAlbum[0])
	artist_name = fetchArtistName(artist)
	playlist.append((artist_name,randomAlbum[1],randomTrack))

f = open('playlist.csv','w',encoding='utf-8')
f.write(u'Artist,Album,Track\n')

for i in range(len(playlist)):
	f.write(('"'+playlist[i][0]+'"'+','+'"'+playlist[i][1]+'"'+','+'"'+playlist[i][2]+'"'+'\n'))
f.close()