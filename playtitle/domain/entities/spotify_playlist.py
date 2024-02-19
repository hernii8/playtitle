from dataclasses import asdict
from playtitle.domain.entities.playlist import Playlist
from playtitle.domain.entities.spotify_song import SpotifySong
from statistics import mean
import collections


class SpotifyPlaylist(Playlist):
    songs: list[SpotifySong]

    def get_average_values(self):
        return {
            "total": len(self.songs),
            "top3_artists": self.__get_top3_artists(),
            "top3_genres": self.__get_top3_genres(),
            "duration": round(mean([song.duration_ms for song in self.songs]), 2),
            "acousticness": round(mean([song.acousticness for song in self.songs]), 2),
            "danceability": round(mean([song.danceability for song in self.songs]), 2),
            "energy": round(mean([song.energy for song in self.songs]), 2),
            "instrumentalness": round(
                mean([song.instrumentalness for song in self.songs]), 2
            ),
            "liveness": round(mean([song.liveness for song in self.songs]), 2),
            "loudness": round(mean([song.loudness for song in self.songs]), 2),
            "tempo": round(mean([song.tempo for song in self.songs]), 2),
            "happiness": round(mean([song.happiness for song in self.songs]), 2),
        }

    def __get_top3_artists(self):
        artists = [artist.name for song in self.songs for artist in song.artists]
        counter = collections.Counter(artists)
        return list(dict(counter.most_common(3)).keys())

    def __get_top3_genres(self):
        genres = [
            genre
            for song in self.songs
            for artist in song.artists
            for genre in artist.genres
        ]
        counter = collections.Counter(genres)
        return list(dict(counter.most_common(3)).keys())
