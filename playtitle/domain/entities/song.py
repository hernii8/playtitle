from dataclasses import dataclass


@dataclass(frozen=True)
class Song:
    id: str
    title: str
    duration_ms: int
    explicit: bool
    popularity: int
    uri: str

    @classmethod
    def from_dict(cls, d):
        return cls(**d)
