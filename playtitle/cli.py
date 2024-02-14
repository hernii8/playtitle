import json
import sys
from infra.spotify.client import SpotifyClient

with open("config/credentials.json") as file:
    credentials = json.load(file)
spotify = SpotifyClient().init(
    credentials["spotify"]["client_id"],
    credentials["spotify"]["client_secret"],
    credentials["spotify"]["callback_url"]
)

if __name__ == "__main__":
    command = sys.argv[1]
