from typing import Any
import asyncio
from copy import deepcopy
from playtitle.domain.entities.artist import Artist
from playtitle.domain.entities.spotify_playlist import SpotifyPlaylist
from playtitle.domain.entities.spotify_song import SpotifySong
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials

FETCH_SONGS_INTERVAL = 100
MAX_CONCURRENT_BATCHES = 3


class SpotifyClient:
    __client: Spotify

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        fetch_songs_limit=FETCH_SONGS_INTERVAL,
        max_concurrent_batches=MAX_CONCURRENT_BATCHES,
    ) -> None:
        self.__client = Spotify(
            auth_manager=SpotifyClientCredentials(
                client_id=client_id, client_secret=client_secret
            )
        )
        self.__fetch_songs_limit = fetch_songs_limit
        self.__max_concurrent_batches = max_concurrent_batches

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
        batches = [
            self.__fetch_songs_batch(
                playlist_id, offset=i, limit=self.__fetch_songs_limit
            )
            for i in range(0, response_tracks["total"], self.__fetch_songs_limit)
        ]
        for i in range(0, len(batches), self.__max_concurrent_batches):
            responses = await asyncio.gather(
                *batches[i : i + self.__max_concurrent_batches - 1]
            )
            for response in responses:
                songs_i, audio_features_i = response
                audio_features += audio_features_i
                songs += songs_i

        return [
            {**song["track"], **audio_feature}
            for song, audio_feature in zip(songs, audio_features)
        ]

    async def __fetch_songs_batch(self, playlist_id, offset, limit):
        songs_response = await asyncio.to_thread(
            self.client.playlist_items,
            playlist_id=playlist_id,
            offset=offset,
            limit=limit,
        )
        songs = deepcopy(songs_response["items"])
        audio_features_response = await asyncio.to_thread(
            self.client.audio_features, [song["track"]["id"] for song in songs]
        )
        artist_ids = [
            artist["id"] for song in songs for artist in song["track"]["artists"]
        ]
        artist_batches = [
            artist_ids[i : i + limit - 1] for i in range(0, len(artist_ids), limit)
        ]
        artists_response_tasks = await asyncio.gather(
            *[
                asyncio.to_thread(self.client.artists, artist_batches[i])
                for i in range(len(artist_batches))
            ]
        )
        artists_response = [
            artist for task in artists_response_tasks for artist in task["artists"]
        ]
        for songs_i in range(len(songs)):
            for artist_i in range(len(songs[songs_i]["track"]["artists"])):
                songs[songs_i]["track"]["artists"][artist_i] = artists_response[
                    songs_i + artist_i
                ]

        return (songs, audio_features_response)

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
