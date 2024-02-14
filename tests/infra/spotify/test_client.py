import pytest
import json
from playtitle.infra.spotify.client import SpotifyClient


@pytest.fixture()
def init_spotify_client():
    with open("config/credentials.json") as file:
        credentials = json.load(file)
    SpotifyClient.init(
        credentials["spotify"]["client_id"],
        credentials["spotify"]["client_secret"])
    yield
    SpotifyClient.restore()


def test_client_singleton(init_spotify_client):
    instance1 = SpotifyClient.get()
    instance2 = SpotifyClient.get()
    assert instance1 == instance2
