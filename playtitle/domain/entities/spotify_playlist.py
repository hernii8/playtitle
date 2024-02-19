from playtitle.domain.entities.playlist import Playlist
from playtitle.domain.entities.spotify_song import SpotifySong
from statistics import mean


class SpotifyPlaylist(Playlist):
    songs: list[SpotifySong]

    def get_average_values(self):
        return {
            "acousticness": mean([song.acousticness for song in self.songs]),
            "danceability": mean([song.danceability for song in self.songs]),
            "energy": mean([song.energy for song in self.songs]),
            "instrumentalness": mean([song.instrumentalness for song in self.songs]),
            "liveness": mean([song.liveness for song in self.songs]),
            "loudness": mean([song.loudness for song in self.songs]),
            "tempo": mean([song.tempo for song in self.songs]),
            "happiness": mean([song.happiness for song in self.songs]),
        }
