import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


class SpotifyClient:
    __client = None

    def __init__(self) -> None:
        raise RuntimeError(
            "SpotifyClient can't be instanciated. Use init() method.")

    @classmethod
    def init(cls, client_id: str, client_secret: str) -> spotipy.Spotify:
        if cls.__client is not None:
            raise RuntimeError(
                "Class already initializated. Use get() method.")

        cls.__client = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
            client_id=client_id,
            client_secret=client_secret
        ))

        return cls.__client

    @classmethod
    def get(cls) -> spotipy.Spotify:
        if cls.__client is None:
            raise RuntimeError("Client not initializated. Use init() method.")

        return cls.__client

    @classmethod
    def restore(cls) -> spotipy.Spotify:
        cls.__client = None
