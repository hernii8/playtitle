from dataclasses import dataclass
from playtitle.domain.entities.song import Song


@dataclass(frozen=True)
class SpotifySong(Song):
    acousticness: float | None = None
    danceability: float | None = None
    energy: float | None = None
    instrumentalness: float | None = None
    liveness:float | None = None
    loudness: float | None = None
    tempo: float | None = None