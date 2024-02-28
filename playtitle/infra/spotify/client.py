import asyncio
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
            self.__fetch_songs_batch(playlist_id, offset=i)
            for i in range(0, response_tracks["total"], self.__fetch_songs_limit)
        ]
        responses = await rate_limited_batch_processing(
            batches, self.__max_concurrent_batches
        )

        return [
            self.__to_spotify_song(song)
            for response in responses
            for song in response
            if song["episode"] is False
        ]

    async def __fetch_songs_batch(self, playlist_id, offset):
        response_songs = await asyncio.to_thread(
            self._client.playlist_items,
            playlist_id=playlist_id,
            offset=offset,
            limit=self.__fetch_songs_limit,
        )
        response_audio_features = await asyncio.to_thread(
            self._client.audio_features,
            [song["track"]["id"] for song in response_songs["items"]],
        )
        artists_response = await self.__fetch_artists_from_songs_list(
            response_songs["items"]
        )

        for i, song in enumerate(response_songs["items"]):
            for j in (song_artists := song["track"]["artists"]):
                song_artists[j] = artists_response[i + j]

        return [
            {**song["track"], **audio_feature}
            for song, audio_feature in zip(
                response_songs["items"], response_audio_features
            )
        ]

    async def __fetch_artists_from_songs_list(self, songs_list):
        artist_ids = [
            artist["id"] for song in songs_list for artist in song["track"]["artists"]
        ]
        artist_batches = [
            asyncio.to_thread(
                self._client.artists, artist_ids[i : i + self.__fetch_songs_limit]
            )
            for i in range(0, len(artist_ids), self.__fetch_songs_limit)
        ]
        return [
            artist
            for response in await rate_limited_batch_processing(
                artist_batches, self.__max_concurrent_batches
            )
            for artist in response["artists"]
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
