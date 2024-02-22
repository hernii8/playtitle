from typing import Any
import asyncio
from playtitle.domain.entities.artist import Artist
from playtitle.domain.entities.spotify_playlist import SpotifyPlaylist
from playtitle.domain.entities.spotify_song import SpotifySong
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials

FETCH_SONGS_INTERVAL = 100
MAX_CONCURRENT_BATCHES = 3


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

    async def get_playlist(self, playlist_id: str) -> SpotifyPlaylist:
        playlist_info = await self.__fetch_info(playlist_id)
        songs = [
            self.__to_spotify_song(item)
            for item in playlist_info["songs"]
            if item["episode"] is False
        ]
        return SpotifyPlaylist(
            id=playlist_info["id"],
            name=playlist_info["name"],
            description=playlist_info["description"],
            uri=playlist_info["uri"],
            songs=songs,
        )

    async def __fetch_info(self, playlist_id: str) -> dict[Any | str, Any]:
        response = await asyncio.to_thread(self.client.playlist, playlist_id)
        songs = await self.__fetch_songs(response["tracks"], playlist_id)
        return {
            **response,
            "songs": songs,
        }

    async def __fetch_songs(
        self, response_tracks, playlist_id: str
    ) -> list[SpotifySong]:
        songs = []
        audio_features = []

        for i in range(0, response_tracks["total"], FETCH_SONGS_INTERVAL):
            songs_i, audio_features_i = await self.__fetch_songs_batch(
                playlist_id, offset=i, limit=FETCH_SONGS_INTERVAL
            )
            audio_features += audio_features_i
            songs += songs_i

        return [
            {**song["track"], **audio_feature}
            for song, audio_feature in zip(songs, audio_features)
        ]

    async def __fetch_songs_batch(self, playlist_id, offset, limit):
        songs = (
            await asyncio.to_thread(
                self.client.playlist_items,
                playlist_id=playlist_id,
                offset=offset,
                limit=limit,
            )
        )["items"]
        audio_features = await asyncio.to_thread(
            self.client.audio_features, [song["track"]["id"] for song in songs]
        )
        for song in songs:
            artist_ids = [artist["id"] for artist in song["track"]["artists"]]
            artists = (await asyncio.to_thread(self.client.artists, artist_ids))[
                "artists"
            ]
            song["track"]["artists"] = artists

        return (songs, audio_features)

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
            artists=[
                Artist(
                    name=artist["name"],
                    popularity=artist["popularity"],
                    follower_count=artist["followers"]["total"],
                    genres=artist["genres"],
                )
                for artist in spotify_song["artists"]
            ],
        )
