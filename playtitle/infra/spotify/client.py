from typing import Any
from playtitle.domain.entities.playlist import Playlist
from playtitle.domain.entities.spotify_song import SpotifySong
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials

FETCH_SONGS_INTERVAL = 100


class SpotifyClient:
    __client: Spotify

    def __init__(self, client_id: str, client_secret: str) -> None:
        self.__client = Spotify(
            auth_manager=SpotifyClientCredentials(
                client_id=client_id, client_secret=client_secret
            )
        )

    @property
    def client(self):
        return self.__client

    def get_playlist(self, playlist_id: str):
        playlist_info = self.__fetch_info(playlist_id)
        songs = [
            self.__to_spotify_song(item)
            for item in playlist_info["songs"]
            if item["episode"] is False
        ]
        return Playlist(
            id=playlist_info["id"],
            name=playlist_info["name"],
            description=playlist_info["description"],
            uri=playlist_info["uri"],
            songs=songs,
        )

    def __fetch_info(self, playlist_id: str) -> dict[Any | str, Any]:
        response = self.client.playlist(playlist_id)
        return {
            **response,
            "songs": self.__fetch_songs(response["tracks"], playlist_id),
        }

    def __fetch_songs(self, response_tracks, playlist_id: str) -> list[SpotifySong]:
        tracks = response_tracks["items"]
        default_limit = response_tracks["limit"]
        audio_features = self.client.audio_features(
            [song["track"]["id"] for song in tracks]
        )
        if (total := response_tracks["total"]) > default_limit:
            for i in range(default_limit + 1, total, FETCH_SONGS_INTERVAL):
                songs_iteration = self.client.playlist_items(
                    playlist_id=playlist_id, offset=i, limit=FETCH_SONGS_INTERVAL
                )["items"]
                audio_features += self.client.audio_features(
                    [song["id"] for song in songs_iteration]
                )
                tracks += songs_iteration

        return [
            {**song["track"], **audio_feature}
            for song, audio_feature in zip(tracks, audio_features)
        ]

    def __to_spotify_song(self, spotify_song) -> SpotifySong:
        return SpotifySong(
            id=spotify_song["id"],
            title=spotify_song["name"],
            duration_ms=spotify_song["duration_ms"],
            uri=spotify_song["uri"],
            explicit=spotify_song["explicit"],
            popularity=spotify_song["popularity"],
            acousticness=spotify_song["acousticness"],
            danceability=spotify_song["danceability"],
            energy=spotify_song["energy"],
            instrumentalness=spotify_song["instrumentalness"],
            liveness=spotify_song["liveness"],
            loudness=spotify_song["loudness"],
            tempo=spotify_song["tempo"],
            happiness=spotify_song["valence"],
        )
