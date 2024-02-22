from unittest.mock import MagicMock
from playtitle.infra.spotify.client import SpotifyClient
import pytest


@pytest.fixture()
def spotipy_mock(mocker) -> MagicMock:
    spotipy_mock = mocker.Mock()
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


@pytest.mark.asyncio
async def test_spotify_playlist_basic_fields(spotipy_mock: MagicMock) -> None:
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
                        "artists": [
                            {
                                "id": "1",
                                "name": "artist",
                                "popularity": 10,
                                "followers": {"total": 10000},
                                "genres": ["Pop", "Jazz"],
                            }
                        ],
                    }
                }
            ],
            "limit": 20,
            "total": 1,
        },
    }
    spotipy_mock.playlist.return_value = sample_response
    spotipy_mock.playlist_items.return_value = sample_response["tracks"]
    spotipy_mock.artists.return_value = {
        "artists": sample_response["tracks"]["items"][0]["track"]["artists"]
    }

    playlist = await SpotifyClient("", "").get_playlist("")
    assert playlist.id == spotipy_mock.playlist.return_value["id"]
    assert playlist.name == spotipy_mock.playlist.return_value["name"]
    assert playlist.description == spotipy_mock.playlist.return_value["description"]
    assert playlist.uri == spotipy_mock.playlist.return_value["uri"]
    assert len(playlist.songs) == len(
        spotipy_mock.playlist.return_value["tracks"]["items"]
    )
    assert len(playlist.songs[0].artists) == len(
        spotipy_mock.playlist.return_value["tracks"]["items"][0]["track"]["artists"]
    )


@pytest.mark.asyncio
async def test_spotify_playlist_songs_over_limit(spotipy_mock: MagicMock) -> None:
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
                        "artists": [
                            {
                                "id": "1",
                                "name": "artist",
                                "popularity": 10,
                                "followers": {"total": 10000},
                                "genres": ["Pop", "Jazz"],
                            }
                        ],
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
                        "artists": [
                            {
                                "id": "2",
                                "name": "artist",
                                "popularity": 10,
                                "followers": {"total": 10000},
                                "genres": ["Pop", "Jazz"],
                            }
                        ],
                    }
                },
            ],
            "limit": 1,
            "total": 1,
        },
    }
    spotipy_mock.playlist.return_value = sample_response
    spotipy_mock.playlist_items.return_value = sample_response["tracks"]
    spotipy_mock.artists.side_effect = [
        {"artists": sample_response["tracks"]["items"][0]["track"]["artists"]},
        {"artists": sample_response["tracks"]["items"][1]["track"]["artists"]},
    ]
    playlist = await SpotifyClient("", "", fetch_songs_limit=1).get_playlist("")

    assert len(playlist.songs) == len(
        spotipy_mock.playlist.return_value["tracks"]["items"]
    )
    assert len(playlist.songs[0].artists) == len(
        spotipy_mock.playlist.return_value["tracks"]["items"][0]["track"]["artists"]
    )


@pytest.mark.asyncio
async def test_spotify_playlist_avoid_episodes(spotipy_mock: MagicMock) -> None:
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
                        "artists": [
                            {
                                "id": "1",
                                "name": "artist",
                                "popularity": 10,
                                "followers": {"total": 10000},
                                "genres": ["Pop", "Jazz"],
                            }
                        ],
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
                        "artists": [
                            {
                                "id": "2",
                                "name": "artist",
                                "popularity": 10,
                                "followers": {"total": 10000},
                                "genres": ["Pop", "Jazz"],
                            }
                        ],
                    }
                },
            ],
            "limit": 1,
            "total": 1,
        },
    }
    spotipy_mock.playlist.return_value = sample_response
    spotipy_mock.playlist_items.return_value = sample_response["tracks"]
    spotipy_mock.artists.return_value = {
        "artists": sample_response["tracks"]["items"][0]["track"]["artists"]
        + sample_response["tracks"]["items"][1]["track"]["artists"]
    }
    playlist = await SpotifyClient("", "").get_playlist("")
    assert (
        len(playlist.songs)
        == len(spotipy_mock.playlist.return_value["tracks"]["items"]) - 1
    )
