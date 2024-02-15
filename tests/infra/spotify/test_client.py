import pytest
import json
from playtitle.infra.spotify.client import SpotifyClient


@pytest.fixture()
def restore_spotify_client():
    yield
    SpotifyClient.restore()


def test_client_singleton(restore_spotify_client):
    instance1 = SpotifyClient.get()
    instance2 = SpotifyClient.get()
    assert instance1 == instance2
