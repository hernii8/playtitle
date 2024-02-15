from unittest.mock import MagicMock
import pytest

from playtitle.domain.entities.song import Song
from playtitle.infra.spotify.repository.playlist import SpotifyPlaylist
from playtitle.use_cases.get_all_songs import GetSongsFromPlaylist


@pytest.fixture
def songs_mock() -> list:
    song1 = Song(id="1", title="1", duration_ms=100,
                 explicit=True, popularity=50, uri="")
    song2 = Song(id="2", title="2", duration_ms=20,
                 explicit=True, popularity=10, uri="")
    song3 = Song(id="3", title="3", duration_ms=200,
                 explicit=False, popularity=30, uri="")
    song4 = Song(id="4", title="4", duration_ms=300,
                 explicit=True, popularity=80, uri="")

    return [
        song1, song2, song3, song4
    ]


def test_song_list_without_parameters(mocker, songs_mock) -> None:
    mock = MagicMock()
    mock.songs = songs_mock
    mocker.patch('playtitle.infra.spotify.repository.playlist.SpotifyPlaylist.__new__',
                 return_value=mock)
    songs = GetSongsFromPlaylist(SpotifyPlaylist("")).exec()
    assert len(songs_mock) == len(songs)
    assert songs_mock[0].id == songs[0].id
