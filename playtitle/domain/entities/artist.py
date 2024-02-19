from dataclasses import dataclass


@dataclass(frozen=True)
class Artist:
    name: str
    popularity: int
    follower_count: int
    genres: list[str]
