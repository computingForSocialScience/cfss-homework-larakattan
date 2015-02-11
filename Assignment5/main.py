import sys
import requests
from fetchArtist import fetchArtistId, fetchArtistInfo
from fetchAlbums import fetchAlbumIds, fetchAlbumInfo
from csvUtils import writeArtistsTable, writeAlbumsTable
from barChart import plotBarChart, getBarChartData

if __name__ == '__main__':
    artist_names = sys.argv[1:]
    print ("input artists are ", artist_names)
    # YOUR CODE HERE
    
    artist_ids = []

    for i in range(len(artist_names)):
    	artist_ids.append(fetchArtistId(artist_names[i]))

    artist_info_list = []
    artist_album_list = {}

    for i in range(len(artist_ids)):
    	artist_info_list.append(fetchArtistInfo(artist_ids[i]))
    	artist_album_list[i]=fetchAlbumIds(artist_ids[i])

    writeArtistsTable(artist_info_list)

    album_info_list=[]

    for i in range(len(artist_album_list)):
    	for j in range(len(artist_album_list[i])):
    		album_info_list.append(fetchAlbumInfo(artist_album_list[i][j]))

    writeAlbumsTable(album_info_list)

    plotBarChart()

    print ("done")