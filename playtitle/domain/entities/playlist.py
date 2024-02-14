from dataclasses import dataclass
from playtitle.domain.entities.song import Song


@dataclass(frozen=True)
class Playlist:
    id: str
    name: str
    description: str
    uri: str
    songs: list[Song]

    @classmethod
    def from_dict(cls, d):
        return cls(**d)
