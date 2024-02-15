import sys
from playtitle.infra.spotify.repository.playlist import SpotifyPlaylist
from playtitle.use_cases.get_all_songs import GetSongsFromPlaylist


if __name__ == "__main__":
    command = sys.argv[1]
    args = sys.argv[2:]
    if command == "playlist":
        playlist_id = args[0]
        playlist = SpotifyPlaylist(playlist_id=playlist_id)
        songs = GetSongsFromPlaylist(playlist).exec()
