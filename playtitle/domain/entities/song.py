from dataclasses import dataclass
from playtitle.domain.entities.artist import Artist


@dataclass(frozen=True)
class Song:
    id: str
    title: str
    duration_ms: int
    explicit: bool
    popularity: int
    uri: str
    artist: Artist = None

    @classmethod
    def from_dict(cls, d):
        return cls(**d)
