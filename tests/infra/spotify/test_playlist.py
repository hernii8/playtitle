from unittest.mock import MagicMock
import pytest
import spotipy
from playtitle.infra.spotify.repository.playlist import SpotifyPlaylist


@pytest.fixture()
def spotify_client_mock(mocker) -> MagicMock:
    client_mock = MagicMock(spec=spotipy.Spotify)
    mocker.patch('playtitle.infra.spotify.client.SpotifyClient.get',
                 return_value=client_mock)
    return client_mock


def test_spotify_playlist_basic_fields(spotify_client_mock: MagicMock) -> None:
    sample_response = {
        "id": "sample_id",
        "description": "",
        "uri": "",
        "name": "",
        "tracks": {
            "items": [
                {
                    "track": {
                        "id": "id",
                        "name": "Title",
                        "duration_ms": 100,
                        "explicit": False,
                        "popularity": 50,
                        "uri": "uri",
                        "episode": False
                    }
                }
            ],
            "limit": 20,
            "total": 1
        }
    }
    spotify_client_mock.playlist.return_value = sample_response
    playlist = SpotifyPlaylist(spotify_client_mock.playlist.return_value["id"])
    assert playlist.id == spotify_client_mock.playlist.return_value["id"]
    assert playlist.name == spotify_client_mock.playlist.return_value["name"]
    assert playlist.description == spotify_client_mock.playlist.return_value["description"]
    assert playlist.uri == spotify_client_mock.playlist.return_value["uri"]
    assert len(playlist.songs) == len(
        spotify_client_mock.playlist.return_value["tracks"]["items"])


def test_spotify_playlist_songs_over_limit(spotify_client_mock: MagicMock) -> None:
    sample_response = {
        "id": "sample_id",
        "description": "",
        "uri": "",
        "name": "",
        "tracks": {
            "items": [
                {
                    "track": {
                        "id": "id",
                        "name": "Title",
                        "duration_ms": 100,
                        "explicit": False,
                        "popularity": 50,
                        "uri": "uri",
                        "episode": False
                    }
                },
                {
                    "track": {
                        "id": "id",
                        "name": "Title",
                        "duration_ms": 100,
                        "explicit": False,
                        "popularity": 50,
                        "uri": "uri",
                        "episode": False
                    }
                }
            ],
            "limit": 1,
            "total": 1
        }
    }
    spotify_client_mock.playlist.return_value = sample_response
    playlist = SpotifyPlaylist(spotify_client_mock.playlist.return_value["id"])
    assert len(playlist.songs) == len(
        spotify_client_mock.playlist.return_value["tracks"]["items"])


def test_spotify_playlist_avoid_episodes(spotify_client_mock: MagicMock) -> None:
    sample_response = {
        "id": "sample_id",
        "description": "",
        "uri": "",
        "name": "",
        "tracks": {
            "items": [
                {
                    "track": {
                        "id": "id",
                        "name": "Title",
                        "duration_ms": 100,
                        "explicit": False,
                        "popularity": 50,
                        "uri": "uri",
                        "episode": True
                    }
                },
                {
                    "track": {
                        "id": "id",
                        "name": "Title",
                        "duration_ms": 100,
                        "explicit": False,
                        "popularity": 50,
                        "uri": "uri",
                        "episode": False
                    }
                }
            ],
            "limit": 1,
            "total": 1
        }
    }
    spotify_client_mock.playlist.return_value = sample_response
    playlist = SpotifyPlaylist(spotify_client_mock.playlist.return_value["id"])
    assert len(playlist.songs) == len(
        spotify_client_mock.playlist.return_value["tracks"]["items"]) - 1
