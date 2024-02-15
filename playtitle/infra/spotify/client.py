from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials


class SpotifyClient:
    __client: Spotify

    def __init__(self, client_id: str, client_secret: str) -> None:
        self.__client = Spotify(auth_manager=SpotifyClientCredentials(
            client_id=client_id,
            client_secret=client_secret
        ))

    @property
    def client(self):
        return self.__client
