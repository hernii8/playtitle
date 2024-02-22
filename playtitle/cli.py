import sys
import json
import asyncio
from playtitle.infra.cohere.client import CohereClient
from playtitle.infra.spotify.client import SpotifyClient
from playtitle.use_cases.generate_title_for_spotify_playlist import (
    GenerateTitleForSpotifyPlaylist,
)


async def main():
    with open("config/credentials.json") as file:
        credentials = json.load(file)
    spotify_client = SpotifyClient(
        credentials["spotify"]["client_id"], credentials["spotify"]["client_secret"]
    )
    cohere_client = CohereClient(credentials["cohere"]["api_key"])
    command = sys.argv[1]
    args = sys.argv[2:]
    if command == "playlist":
        playlist_id = args[0]
        playlist = await spotify_client.get_playlist(playlist_id=playlist_id)
        title = GenerateTitleForSpotifyPlaylist(
            client=cohere_client, playlist=playlist
        ).exec()
        print(title)


if __name__ == "__main__":
    asyncio.run(main())
