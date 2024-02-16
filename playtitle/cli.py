import sys
import json
from playtitle.infra.cohere.client import CohereClient
from playtitle.infra.cohere.title_generator import CohereTitleGenerator
from playtitle.infra.spotify.client import SpotifyClient
from playtitle.infra.spotify.repository.playlist import SpotifyPlaylist
from playtitle.use_cases.get_all_songs import GetSongsFromPlaylist


with open("config/credentials.json") as file:
    credentials = json.load(file)
spotify_client = SpotifyClient(
    credentials["spotify"]["client_id"], credentials["spotify"]["client_secret"]
)
cohere_client = CohereClient(credentials["cohere"]["api_key"])

if __name__ == "__main__":
    command = sys.argv[1]
    args = sys.argv[2:]
    if command == "playlist":
        playlist_id = args[0]
        playlist = SpotifyPlaylist(
            playlist_id=playlist_id, spotify_client=spotify_client
        )
        songs = GetSongsFromPlaylist(playlist).exec()
        title = CohereTitleGenerator(cohere_client=cohere_client).generate_title()
