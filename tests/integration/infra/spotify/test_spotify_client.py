import pytest
import json
from typing import Generator, Any
from spotipy import Spotify
from playtitle.infra.spotify.client import SpotifyClient


@pytest.fixture()
def init_spotify_client() -> Generator[Spotify, Any, Any]:
    with open("config/credentials.json") as file:
        credentials = json.load(file)
    spotify_client = SpotifyClient(
        credentials["spotify"]["client_id"], credentials["spotify"]["client_secret"]
    )._client
    yield spotify_client


def test_client_init(init_spotify_client):
    assert init_spotify_client._session is not None
