from flask import Flask, render_template, request, redirect, url_for
import pymysql
from fetchArtist import *
from fetchAlbums import *
from artistNetworks import *
from makePlaylist import *
import random 

dbname="kattan"
host="mcmahan.zapto.org"
user="kattan"
passwd="blip54#"
port= 8889
db=pymysql.connect(db=dbname, host=host, user=user,passwd=passwd, port=port, charset='utf8')

cur = db.cursor()

app = Flask(__name__)


@app.route('/')
def make_index_resp():
    # this function just renders templates/index.html when
    # someone goes to http://127.0.0.1:5000/
    return(render_template('index.html'))


@app.route('/playlists/')
def make_playlists_resp():
    cur.execute('''SELECT * FROM playlists;''')
    playlists = cur.fetchall()
    return render_template('playlists.html',playlists=playlists)


@app.route('/playlist/<playlistId>')
def make_playlist_resp(playlistId):
    cur.execute('''SELECT * FROM songs WHERE playlistId = %s;''',playlistId)
    songs = cur.fetchall()
    return render_template('playlist.html',songs=songs)


@app.route('/addPlaylist/',methods=['GET','POST'])
def add_playlist():
    if request.method == 'GET':
        # This code executes when someone visits the page.
        return(render_template('addPlaylist.html'))
    elif request.method == 'POST':
        # this code executes when someone fills out the form
        artistName = request.form['artistName']
        # YOUR CODE HERE
        createNewPlaylist(artistName)
        return(redirect("/playlists/"))


# if the playlist and songs tables don't already exist, create them
mysql_playlist = '''CREATE TABLE IF NOT EXISTS playlists (id INTEGER PRIMARY KEY AUTO_INCREMENT, rootArtist VARCHAR(130));'''

mysql_songs = '''CREATE TABLE IF NOT EXISTS songs (playlistId int, songOrder int, artistName VARCHAR(150), albumName VARCHAR(150), trackName VARCHAR(150));'''

# pass the SQL statements to the database
cur.execute(mysql_playlist)
cur.execute(mysql_songs)


def createNewPlaylist(artistName):

    artistID = fetchArtistId(artistName)

    if artistID == '':
        print ("error, bad artist name passed to createNewPlaylist")
        return # if the artist name passed to the playlist isn't in the API, leave the function

    # add the user-provided artist into the playlist. The playlist ID is auto-incremented 
    # and created by our earlier SQL code 
    add_to_playlist = '''INSERT INTO playlists (rootArtist) VALUES (%s);''' 
    cur.execute(add_to_playlist,artistName)

    # using previously written functions, get the network of artists related
    # to the user-provided artist
    artist_edges = getDepthEdges(artistID,2)
    
    # the playlist ID is auto-incremented; since this ID needs to go to the songs table, 
    # find out what the just-generated ID was and save it
    playlist_ID = cur.lastrowid

    # a list to hold our playlist until it's added to the database
    playlist = []

    count = 1 
    while count <= 30: 
    # need 30 random related artists to put into the playlist 
        
        # pick a random tuple from the list of edges, then randomly pick which side of the tuple
        # to add to the playlist 
        random_artist_ID = random.choice(artist_edges)[random.randint(0,1)]
        
        # use previously written functions to get the name of the artist that goes with the 
        # randomly chosen ID
        artist_name = fetchArtistName(random_artist_ID)

        #get random album from this artist
        random_album = fetchRandomAlbum(random_artist_ID)

        # had issues with artists coming back with no albums
        # check if the random album is empty
        # if there's no album, don't increment the counter and start over again with a different random artist
        if random_album=='':
            continue 

        # fetchRandomAlbum() returns a tuple: first item is the ID, second item is the name 
        album_name = random_album[1]
        track_name = fetchRandomTrack(random_album[0])
        
        # set song order to the counter
        song_order = count

        # add this song to the playlist
        playlist.append((playlist_ID,song_order,artist_name,album_name,track_name))

        count+=1

    # SQL commands to add the playlist list into the approparite table in the database
    sql_add_playlist = '''INSERT INTO songs (playlistId, songOrder, artistName, albumName, trackName) VALUES (%s, %s,%s,%s,%s);'''
    cur.executemany(sql_add_playlist,playlist)
    
    # print the songs table to test 
    cur.execute('''SELECT * FROM songs;''')
    sql_result = cur.fetchall()
    print (sql_result)

# test creating a new playlist 
createNewPlaylist("Bowie")
createNewPlaylist("Taylor Swift")


if __name__ == '__main__':
    app.debug=False
    app.run()
