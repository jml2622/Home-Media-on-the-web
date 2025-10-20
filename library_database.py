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
    _tablename__ = 'songs'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    length: Mapped[str]
    album: Mapped["albums"] = relationship(back_populates="songs")
    artist: Mapped[str]
    playcount:Mapped[int]
    file_path:Mapped[str]
    genre:Mapped[str]
    artwork_path:Mapped[str] = mapped_column(nullable=True)
    artist:Mapped["Artist"] = relationship(back_populates="songs")
    artist_id: Mapped[int] = relationship(ForeignKey("artist.id"))
    album_id: Mapped[int] = mapped_column(ForeignKey("artists.id"),nullable=True)
class Albums(Base):
    _tablename__ = 'albums'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    track_num: Mapped[str] = mapped_column(nullable=True)
    genre:Mapped[str]
    songs: Mapped[list["Song"]] = relationship(back_populates="album")
    artist:Mapped["Artist"] = relationship(back_populates="albums")
    artist_id: Mapped[int] = relationship(ForeignKey("artist.id"))

class Artists(Base):
    _tablename__ = 'artists'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    albums:  Mapped[list["Album"]] = relationship(back_populates="artist")
    songs: Mapped[list["Song"]] = relationship(backpopulates = "artist")


def add_song(title, length, album, artist, playcount, track_num,file_path, artwork_path,genre ):
    with Session as session:
            artist_object = get_or_create_artist(session,artist)
#check if the song is a single, if it is just add it to the datbase
            if album == "single":
                new_song = Songs(title,length,album = Null,artist = artist_object,playcount = 0,tracknum = Null,file_path=file_path)
                session.add(new_song)
                session.commit()
                
            else:
                album_object = get_or_create_album(session,album)
                new_song = Songs(title,length,album = album_object,artist=artist_object,playcount=playcount,tracknum = track_num, filepath = file_path,artworkpath = artwork_path,genre = genre)
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