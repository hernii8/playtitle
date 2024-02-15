import sys
import json
from playtitle.infra.spotify.client import SpotifyClient
from playtitle.infra.spotify.repository.playlist import SpotifyPlaylist
from playtitle.use_cases.get_all_songs import GetSongsFromPlaylist


with open("config/credentials.json") as file:
    credentials = json.load(file)
spotify_client = SpotifyClient(
    credentials["spotify"]["client_id"],
    credentials["spotify"]["client_secret"]
).client

if __name__ == "__main__":
    command = sys.argv[1]
    args = sys.argv[2:]
    if command == "playlist":
        playlist_id = args[0]
        playlist = SpotifyPlaylist(
            playlist_id=playlist_id, spotify_client=spotify_client)
        songs = GetSongsFromPlaylist(playlist).exec()
