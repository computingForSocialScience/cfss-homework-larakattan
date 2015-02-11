import sys
import requests
import csv

def fetchArtistId(name):
    """Using the Spotify API search method, take a string that is the artist's name, 
    and return a Spotify artist ID.
    """
    req = requests.get("https://api.spotify.com/v1/search?q="+name+"&type=artist")
    artist = req.json()

    if not (artist['artists']['items']):
        print ("Oops: Bad artist name passed to fetchArtistId().")
        return('')
    else:
        artist_id = artist['artists']['items'][0]['id']
        # print ("artist ID for", name, " is", artist_id)
    # print (req.json())
    return (artist_id)
    

def fetchArtistInfo(artist_id):
    """Using the Spotify API, takes a string representing the id and
`   returns a dictionary including the keys 'followers', 'genres', 
    'id', 'name', and 'popularity'.
    """
    req = requests.get("https://api.spotify.com/v1/artists/"+artist_id)
    artist_info = req.json()

    if not (artist_id):
        print ("Oops: Bad artist ID passed to fetchArtistInfo().")
        return('')
    else:
        artist_info_dict = {}
        artist_info_dict['followers']=artist_info['followers']['total']
        artist_info_dict['genres']=artist_info['genres']
        artist_info_dict['id']=artist_id
        artist_info_dict['name']=artist_info['name']
        artist_info_dict['popularity']=artist_info['popularity']
        # print (artist_info_dict)

    return(artist_info_dict)

    