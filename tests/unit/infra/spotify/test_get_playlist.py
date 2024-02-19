from unittest.mock import MagicMock
from playtitle.infra.spotify.client import SpotifyClient
from spotipy import Spotify
import pytest


@pytest.fixture()
def spotipy_mock(mocker) -> MagicMock:
    spotipy_mock = mocker.Mock(spec=Spotify)
    mocker.patch(
        "playtitle.infra.spotify.client.Spotify",
        return_value=spotipy_mock,
    )
    mocker.patch(
        "playtitle.infra.spotify.client.SpotifyClientCredentials",
        return_value=mocker.Mock(),
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
            "valence": 0.5,
        },
        {
            "acousticness": 50,
            "danceability": 50,
            "energy": 50,
            "instrumentalness": 50,
            "liveness": 50,
            "loudness": 50,
            "tempo": 50,
            "valence": 0.5,
        },
    ]
    spotipy_mock.audio_features.return_value = sample_audio_features
    return spotipy_mock


def test_spotify_playlist_basic_fields(spotipy_mock: MagicMock) -> None:
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
    spotipy_mock.playlist.return_value = sample_response
    playlist = SpotifyClient("", "").get_playlist("")
    assert playlist.id == spotipy_mock.playlist.return_value["id"]
    assert playlist.name == spotipy_mock.playlist.return_value["name"]
    assert playlist.description == spotipy_mock.playlist.return_value["description"]
    assert playlist.uri == spotipy_mock.playlist.return_value["uri"]
    assert len(playlist.songs) == len(
        spotipy_mock.playlist.return_value["tracks"]["items"]
    )


def test_spotify_playlist_songs_over_limit(spotipy_mock: MagicMock) -> None:
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
    spotipy_mock.playlist.return_value = sample_response
    playlist = SpotifyClient("", "").get_playlist("")

    assert len(playlist.songs) == len(
        spotipy_mock.playlist.return_value["tracks"]["items"]
    )


def test_spotify_playlist_avoid_episodes(spotipy_mock: MagicMock) -> None:
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
    spotipy_mock.playlist.return_value = sample_response
    playlist = SpotifyClient("", "").get_playlist("")
    assert (
        len(playlist.songs)
        == len(spotipy_mock.playlist.return_value["tracks"]["items"]) - 1
    )
