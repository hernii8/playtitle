from playtitle.domain.entities.artist import Artist
import pytest
from typing import Any
from playtitle.domain.entities.song import Song


@pytest.fixture
def init_attributes() -> dict[str, Any]:
    return {
        "id": "id",
        "title": "Title",
        "duration_ms": 100,
        "explicit": False,
        "popularity": 50,
        "uri": "uri",
        "artists": [
            Artist(
                name="artist",
                popularity=10,
                follower_count=10000,
                genres=["Pop", "Jazz"],
            )
        ],
    }


def test_song_model_init(init_attributes: dict[str, Any]) -> None:
    song = Song(**init_attributes)
    for key, value in init_attributes.items():
        assert getattr(song, key) == value


def test_song_model_from_dict(init_attributes: dict[str, Any]) -> None:
    song = Song.from_dict(init_attributes)
    for key, value in init_attributes.items():
        assert getattr(song, key) == value


def test_song_idempotency(init_attributes: dict[str, Any]) -> None:
    song = Song.from_dict(init_attributes)
    song2 = Song.from_dict(init_attributes)
    assert song.__eq__(song2)
