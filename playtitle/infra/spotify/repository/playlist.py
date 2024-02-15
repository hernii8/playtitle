from dataclasses import dataclass
from typing import Any
from spotipy import Spotify
from playtitle.domain.entities.playlist import Playlist
from playtitle.domain.entities.song import Song


@dataclass(frozen=True)
class SpotifyPlaylist(Playlist):
    spotify_client: Spotify

    def __init__(self, playlist_id: str, spotify_client: Spotify) -> None:
        object.__setattr__(self, "spotify_client", spotify_client)
        playlist_info = self.__fetch_info(playlist_id)
        songs = [self.__to_song(
            item["track"]) for item in playlist_info["songs"] if item["track"]["episode"] is False]

        super().__init__(
            id=playlist_id,
            name=playlist_info["name"],
            description=playlist_info["description"],
            uri=playlist_info["uri"],
            songs=songs
        )

    def __fetch_info(self, playlist_id: str) -> dict[Any | str, Any]:
        response = self.spotify_client.playlist(playlist_id)
        return {
            **response,
            "songs": self.__fetch_songs(response["tracks"])
        }

    def __fetch_songs(self, response_tracks) -> list[Song]:
        songs = response_tracks["items"]
        default_limit = response_tracks["limit"]
        limit = 100
        if (total := response_tracks["total"]) > default_limit:
            for i in range(default_limit + 1, total, limit):
                songs += self.spotify_client.playlist_items(
                    playlist_id=self.id, offset=i)["items"]

        return songs

    def __to_song(self, spotify_song) -> Song:
        return Song(
            id=spotify_song["id"],
            title=spotify_song["name"],
            duration_ms=spotify_song["duration_ms"],
            uri=spotify_song["uri"],
            explicit=spotify_song["explicit"],
            popularity=spotify_song["popularity"]
        )
