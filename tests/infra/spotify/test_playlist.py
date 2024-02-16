from unittest.mock import MagicMock
import pytest
import spotipy
from playtitle.infra.spotify.repository.playlist import SpotifyPlaylist


@pytest.fixture()
def spotify_client_mock(mocker) -> MagicMock:
    spotify_client_mock = MagicMock(spec=spotipy.Spotify)
    client_mock = MagicMock()
    spotify_client_mock.client = client_mock
    mocker.patch(
        "playtitle.infra.spotify.client.SpotifyClient", return_value=spotify_client_mock
    )
    sample_audio_features = [
        {
            "acousticness": 50,
            "danceability": 50,
            "energy": 50,
            "instrumentalness": 50,
            "liveness": 50,
            "loudness": 50,
            "tempo": 50,
        },
        {
            "acousticness": 50,
            "danceability": 50,
            "energy": 50,
            "instrumentalness": 50,
            "liveness": 50,
            "loudness": 50,
            "tempo": 50,
        },
    ]
    spotify_client_mock.client.audio_features.return_value = sample_audio_features
    return spotify_client_mock


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
                        "episode": False,
                    }
                }
            ],
            "limit": 20,
            "total": 1,
        },
    }
    spotify_client_mock.client.playlist.return_value = sample_response
    playlist = SpotifyPlaylist(
        spotify_client_mock.client.playlist.return_value["id"], spotify_client_mock
    )
    assert playlist.id == spotify_client_mock.client.playlist.return_value["id"]
    assert playlist.name == spotify_client_mock.client.playlist.return_value["name"]
    assert (
        playlist.description
        == spotify_client_mock.client.playlist.return_value["description"]
    )
    assert playlist.uri == spotify_client_mock.client.playlist.return_value["uri"]
    assert len(playlist.songs) == len(
        spotify_client_mock.client.playlist.return_value["tracks"]["items"]
    )


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
                        "episode": False,
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
                        "episode": False,
                    }
                },
            ],
            "limit": 1,
            "total": 1,
        },
    }
    spotify_client_mock.client.playlist.return_value = sample_response
    playlist = SpotifyPlaylist(
        spotify_client_mock.client.playlist.return_value["id"], spotify_client_mock
    )

    assert len(playlist.songs) == len(
        spotify_client_mock.client.playlist.return_value["tracks"]["items"]
    )


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
                        "episode": True,
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
                        "episode": False,
                    }
                },
            ],
            "limit": 1,
            "total": 1,
        },
    }
    spotify_client_mock.client.playlist.return_value = sample_response
    playlist = SpotifyPlaylist(
        spotify_client_mock.client.playlist.return_value["id"], spotify_client_mock
    )
    assert (
        len(playlist.songs)
        == len(spotify_client_mock.client.playlist.return_value["tracks"]["items"]) - 1
    )
