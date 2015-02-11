import requests
from datetime import datetime

def fetchAlbumIds(artist_id):
    """Using the Spotify API, take an artist ID and 
    returns a list of album IDs in a list
    """
    req = requests.get("https://api.spotify.com/v1/artists/"+artist_id+"/albums?album_type=album&market=US")
    albums = req.json()

    albums_list = []

    if not(artist_id):
    	print ("Oops: Bad artist_id passed to fetchAlbumIds().")
    	return ('')

    for i in range(len(albums['items'])):
    	albums_list.append(albums['items'][i]['id']) 

    return(albums_list)

def fetchAlbumInfo(album_id):
    """Using the Spotify API, take an album ID 
    and return a dictionary with keys 'artist_id', 'album_id' 'name', 'year', popularity'
    """
    
    req = requests.get("https://api.spotify.com/v1/albums/"+album_id)
    album_info = req.json()

    if not (album_id):
        print ("Oops: Bad album ID passed to fetchAlbumInfo().")
        return('')
    else:
        album_info_dict = {}
        album_info_dict['artist_id']=album_info['artists'][0]['name']
        album_info_dict['name']=album_info['name']
        album_info_dict['album_id']=album_id
        album_info_dict['year']=album_info['release_date'][0:4]
        album_info_dict['popularity']=album_info['popularity']
        
    return(album_info_dict)


