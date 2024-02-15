from dataclasses import dataclass
from playtitle.domain.entities.playlist import Playlist


@dataclass(frozen=True)
class GetSongsFromPlaylist:
    playlist: Playlist

    def exec(self):
        return self.playlist.songs
