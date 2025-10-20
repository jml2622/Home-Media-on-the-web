from flask import Flask,render_template
from models import *
from datetime import datetime
import random
app = Flask(__name__)

@app.route('/')
#Fetch a list of all songs, album and artists names on startup
def list_songs():
    session = Session()
    song_list = session.query(Songs).order_by(Songs.title).all()
    session.close() 
    return render_template('Homepage.html', song_list=song_list)
def list_albums():
    session = Session()
    album_list = session.query(Albums).order_by(Albums.title).all()
    session.close() 
    return render_template('Homepage.html', album_list=album_list)
def list_albums():
    session = Session()
    album_list = session.query(Albums).order_by(Albums.title).all()
    session.close() 
    return render_template('Homepage.html', album_list=album_list)
def list_artists():
    session = Session()
    artists_list = session.query(Artists).order_by(Artists.name).all()
    session.close() 
    return render_template('Homepage.html', artists_list=artists_list)

#change playcount and playdate everytime a song is played 
@app.route('/songs/<int:id>',methods=['POST'])
def play_song(song_id):
    session = Session()
    song_to_update = session.query(Songs).get(song_id)
    file_to_play = session.query(Songs.file_path).get(song_id)
    current_playcount = session.query(Songs).filter(id = song_id)
    song_to_update.last_played = datetime.UTCnow()
    song_to_update.playcount +=1
    session.commit()
    session.close()
    return(file_to_play)
    #need to choose page to redirect user to !!!!!

def get_icon(song_id,album_id,artist_id,type):
    session = Session()
    if len(song_id) == 0:
         path = (f"/media/{artist_id}/{album_id}.txt")
    else:
        path = (f"/media/{artist_id}/{album_id}/{song_id}.txt")

    
def get_slideshow_item(session):
    slideshow_data = {}
    #get the most recently played song 
    slideshow_data['recent_song'] = session.query(Songs).order_by(desc(Songs.last_played))
    #get a random unplayed album 
    played_albums = select(Songs.album_id).where(Songs.playcount >0).distinct().scalar_subquery()
    unplayed_albums = session.scalars(select(Albums).where(Albums.id.not_in)(played_albums)).all()
    slideshow_data['unplayed_album'] = random.choice(unplayed_albums)
    #get the most played artist
    most_played_artist = (
        select(Artists,func.sum(Songs.playcount).label('total_plays'))
        .join(Songs, Artists.id == Songs.artist_id)
        .group_by(Artists.id)
        .order_by(desc('total_plays'))
    )
    result = session.execute(most_played_artist).first()
    slideshow_data['top artist'] = result[0]
    all_playlists = session.query(Playlist).all()
    slideshow_data['random_playlist'] = random.choice(all_playlists) if all_playlists else None

@app.route("/artist/<str:name>")
def artist_search(query):
    session = Session()
    artist = session.query(Artists).filter(Artists.name)

@app.route('/')
def homepage():
   session  =Session()
   slideshow_data =  get_slideshow_item()

   slideshow_items = [          {
            'title': 'Recently Played',
            'subtitle': slideshow_data['recent_song'].title if slideshow_data['recent_song'] else 'Play a song!',
            'image_path': slideshow_data['recent_song'].artwork_path if slideshow_data['recent_song'] else 'default.jpg'
        },
        {
            'title': 'Discover Unplayed',
            # Assuming your Album model has an artwork_path attribute
            'image_path': slideshow_data['random_album'].artwork_path if slideshow_data['random_album'] else 'default.jpg'
        },
        {
            'title': 'Most Played Artist',
            # Assuming your Artist model has an image_path attribute
            'image_path': slideshow_data['top_artist'].image_path if slideshow_data['top_artist'] else 'default.jpg'
        },
        {
            'title': 'Random Playlist',
            # Assuming your Playlist model has an artwork_path attribute
            'image_path': slideshow_data['random_playlist'].artwork_path if slideshow_data['random_playlist'] else 'default.jpg'
        }
    ]
    session.close()

    return render_template('Homepage.html',slideshow_items=slideshow_items)