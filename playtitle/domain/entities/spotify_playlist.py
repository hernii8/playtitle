from playtitle.domain.entities.playlist import Playlist
from playtitle.domain.entities.spotify_song import SpotifySong
from statistics import mean


class SpotifyPlaylist(Playlist):
    songs: list[SpotifySong]

    def get_average_values(self):
        return {
            "total": len(self.songs),
            "top3_artists": [],
            "top3_genres": [],
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
