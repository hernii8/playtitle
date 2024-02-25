from typing import Any
import asyncio
from copy import deepcopy
from playtitle.domain.entities.artist import Artist
from playtitle.domain.entities.spotify_playlist import SpotifyPlaylist
from playtitle.domain.entities.spotify_song import SpotifySong
from playtitle.utils.rate_limited_batch_processing import rate_limited_batch_processing
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials

FETCH_SONGS_INTERVAL = 50
MAX_CONCURRENT_BATCHES = 10


class SpotifyClient:
    _client: Spotify

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        fetch_songs_limit=FETCH_SONGS_INTERVAL,
        max_concurrent_batches=MAX_CONCURRENT_BATCHES,
    ) -> None:
        self._client = Spotify(
            auth_manager=SpotifyClientCredentials(
                client_id=client_id, client_secret=client_secret
            )
        )
        self.__fetch_songs_limit = fetch_songs_limit
        self.__max_concurrent_batches = max_concurrent_batches

    async def get_playlist(self, playlist_id: str) -> SpotifyPlaylist:
        playlist_info = await asyncio.to_thread(self._client.playlist, playlist_id)
        songs = await self.__fetch_songs(playlist_info["tracks"], playlist_id)
        return SpotifyPlaylist(
            id=playlist_info["id"],
            name=playlist_info["name"],
            description=playlist_info["description"],
            uri=playlist_info["uri"],
            songs=songs,
        )

    async def __fetch_songs(
        self, response_tracks, playlist_id: str
    ) -> list[SpotifySong]:
        batches = [
            self.__fetch_songs_batch(
                playlist_id, offset=i, limit=self.__fetch_songs_limit
            )
            for i in range(0, response_tracks["total"], self.__fetch_songs_limit)
        ]
        responses = await rate_limited_batch_processing(
            batches, self.__max_concurrent_batches
        )

        return [
            self.__to_spotify_song({**song["track"], **audio_feature})
            for response_songs, response_audio_features in responses
            for song, audio_feature in zip(response_songs, response_audio_features)
            if song["track"]["episode"] is False
        ]

    async def __fetch_songs_batch(self, playlist_id, offset, limit):
        songs_response = await asyncio.to_thread(
            self._client.playlist_items,
            playlist_id=playlist_id,
            offset=offset,
            limit=limit,
        )
        songs = deepcopy(songs_response["items"])
        audio_features_response = await asyncio.to_thread(
            self._client.audio_features, [song["track"]["id"] for song in songs]
        )
        artist_ids = [
            artist["id"] for song in songs for artist in song["track"]["artists"]
        ]
        artist_batches = [
            artist_ids[i : i + limit] for i in range(0, len(artist_ids), limit)
        ]
        artists_response_tasks = await asyncio.gather(
            *[
                asyncio.to_thread(self._client.artists, artist_batches[i])
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
