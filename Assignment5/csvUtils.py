from io import open

def writeArtistsTable(artist_info_list):
    """Given a list of dictionries, each as returned from 
    fetchArtistInfo(), write a csv file 'artists.csv'.

    The csv file should have a header line that looks like this:
    ARTIST_ID,ARTIST_NAME,ARTIST_FOLLOWERS,ARTIST_POPULARITY
    """
    artists_file = open('artists.csv','w')

    artists_file.write(u'ARTIST_ID,ARTIST_NAME,ARTIST_FOLLOWERS,ARTIST_POPULARITY\n')

    for artist in range(len(artist_info_list)):
        artists_file.write(artist_info_list[artist]['id']+","+artist_info_list[artist]['name']+","+str(artist_info_list[artist]['followers'])+","+str(artist_info_list[artist]['popularity']))
        artists_file.write('\n')

    artists_file.close() 
      
def writeAlbumsTable(album_info_list):
    """
    Given list of dictionaries, each as returned
    from the function fetchAlbumInfo(), write a csv file
    'albums.csv'.

    The csv file should have a header line that looks like this:
    ARTIST_ID,ALBUM_ID,ALBUM_NAME,ALBUM_YEAR,ALBUM_POPULARITY
    """
    
    albums_file = open('albums.csv','w')

    albums_file.write(u'ARTIST_ID,ALBUM_ID,ALBUM_NAME,ALBUM_YEAR,ALBUM_POPULARITY\n')

    for album in range(len(album_info_list)):
        albums_file.write(album_info_list[album]['artist_id']+","+album_info_list[album]['album_id']+","+album_info_list[album]['name']+","+str(album_info_list[album]['year'])+","+str(album_info_list[album]['popularity']))
        albums_file.write('\n')

    albums_file.close() 