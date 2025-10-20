import sqlalchemy as sq
from sqlalchemy import *
from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, sessionmaker, declarative_base, relationship

sqlite_file = "music-database.db"
sqlite_url = f"sqlite:///{sqlite_file}"
db = sq.create_engine(sqlite_url, echo=True)
Session = sessionmaker(bind=db)
Base = declarative_base()



class Songs(Base):
    __tablename__ = 'songs'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    length: Mapped[str]
    album: Mapped["albums"] = relationship(backpopulates="songs")
    artist: Mapped[str]
    playcount:Mapped[int]
    file_path:Mapped[str]
    genre:Mapped[str]
    playlists:Mapped[list] = mapped_column(nullable = True)
    last_played:Mapped[DateTime] = mapped_column(nullable=True)
    year:Mapped[int]
    artwork_path:Mapped[str] = mapped_column(nullable=True)
    artist:Mapped["Artist"] = relationship(backpopulates="songs")
    artist_id: Mapped[int] = relationship(ForeignKey("artist.id"))
    album_id: Mapped[int] = mapped_column(ForeignKey("artists.id"),nullable=True)
class Albums(Base):
    __tablename__ = 'albums'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    track_num: Mapped[str] = mapped_column(nullable=True)
    genre:Mapped[str]
    songs: Mapped[list["Song"]] = relationship(backpopulates="album")
    artist:Mapped["Artist"] = relationship(backpopulates="albums")
    artist_id: Mapped[int] = relationship(ForeignKey("artist.id"))

class Artists(Base):
    __tablename__ = 'artists'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    albums:  Mapped[list["Album"]] = relationship(backpopulates="artist")
    songs: Mapped[list["Song"]] = relationship(backpopulates = "artist")
    icon_path: Mapped[str] = mapped_column(nullable = True)

class Playlists(Base):
    __tablename__='playlists'
    id:Mapped[int] = mapped_column(primary_key=True)
    name:Mapped[str]
    songs: Mapped[list] = mapped_column
    icon_path: Mapped[str]


def add_song(title, length, album, artist, track_num,file_path,year artwork_path,genre ):
    with Session as session:
            artist_object = get_or_create_artist(session,artist)
#check if the song is a single, if it is just add it to the datbase
            if album == "single":
                new_song = Songs(title,length,album = Null,artist = artist_object,playcount = 0,tracknum = Null,file_path=file_path,genre=genre,playlists=Null,last_played = Null,year = year,artwork_path = artwork_path)
                session.add(new_song)
                session.commit()
                
            else:
                album_object = get_or_create_album(session,album)
                new_song = Songs(title,length,album = album_object,artist=artist_object,playcount=playcount,tracknum = track_num, filepath = file_path,artworkpath = artwork_path,genre = genre,playlists=Null,last_played = Null,year = year)
                session.add(new_song)
                session.commit()


def get_or_create_album(session, album,album_artist,genre):
    album_search = session.query(Albums).filter(
        Albums.title == album,
        Albums.artist == album_artist)
    if album == True:
        return album_search
    else: 
        track_num = null 
        new_album = Albums(album,album_artist,track_num,genre)
        return new_album 
    

def get_or_create_artist(session, artist_name):
    artists_query=session.query(Artists).filter(Artists.name == artist_name)
 #check if the artist exists
    if artists_query:
         return artists_query

    else:
        #if the artist doesnt exist create the artist 
        new_artist = Artists(name = artist)
        session.add(new_artist)
        session.commit()
        return new_artist