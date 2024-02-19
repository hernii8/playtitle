from playtitle.domain.entities.artist import Artist
from playtitle.domain.entities.spotify_playlist import SpotifyPlaylist
from playtitle.domain.entities.spotify_song import SpotifySong
import pytest


@pytest.fixture()
def spotify_songs():
    return [
        SpotifySong(
            id="1",
            title="Song 1",
            duration_ms=180000,
            explicit=True,
            popularity=80,
            uri="spotify:track:uri_1",
            acousticness=0.5,
            danceability=0.7,
            energy=0.8,
            instrumentalness=0.2,
            liveness=0.6,
            loudness=50.0,
            tempo=120.0,
            happiness=0.1,
            artists=[
                Artist(
                    name="artist",
                    popularity=10,
                    follower_count=10000,
                    genres=["Pop", "Jazz"],
                )
            ],
        ),
        SpotifySong(
            id="id 2",
            title="Song 2",
            duration_ms=180000,
            explicit=True,
            popularity=20,
            uri="spotify:track:uri_2",
            acousticness=0.5,
            danceability=0.1,
            energy=0.2,
            instrumentalness=0.3,
            liveness=0.9,
            loudness=20.0,
            tempo=120.0,
            happiness=0.9,
            artists=[
                Artist(
                    name="artist",
                    popularity=10,
                    follower_count=10000,
                    genres=["Pop", "Jazz"],
                )
            ],
        ),
    ]


def test_get_average_values(spotify_songs):
    playlist = SpotifyPlaylist(
        id="", name="", description="", uri="", songs=spotify_songs
    )
    averages = playlist.get_average_values()
    assert averages["acousticness"] == (
        (spotify_songs[0].acousticness + spotify_songs[1].acousticness) / 2
    )
