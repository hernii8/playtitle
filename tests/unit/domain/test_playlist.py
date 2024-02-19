import pytest
from typing import Any
from playtitle.domain.entities.playlist import Playlist
from playtitle.domain.entities.song import Song


@pytest.fixture
def init_attributes() -> dict[str, Any]:
    return {
        "id": "id",
        "name": "name",
        "description": "description",
        "uri": "uri",
        "songs": [Song("id", "title", 0, False, 50, "uri")],
    }


def test_playlist_model_init(init_attributes: dict[str, Any]) -> None:
    playlist = Playlist(**init_attributes)
    for key, value in init_attributes.items():
        assert getattr(playlist, key) == value


def test_playlist_model_from_dict(init_attributes: dict[str, Any]) -> None:
    playlist = Playlist.from_dict(init_attributes)
    for key, value in init_attributes.items():
        assert getattr(playlist, key) == value


def test_playlist_idempotency(init_attributes: dict[str, Any]) -> None:
    playlist = Playlist.from_dict(init_attributes)
    playlist2 = Playlist.from_dict(init_attributes)
    assert playlist.__eq__(playlist2)
