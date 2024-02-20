from dataclasses import dataclass

from playtitle.domain.entities.spotify_playlist import SpotifyPlaylist
from playtitle.infra.interfaces.llm_client import LLMClient


@dataclass(frozen=True)
class GenerateTitleForSpotifyPlaylist:
    playlist: SpotifyPlaylist
    client: LLMClient

    def exec(self):
        return self.client.generate_response(self.__build_prompt())

    def __build_prompt(self):
        average_values = self.playlist.get_average_values()
        return f"""Craft a title for a playlist that embodies the genres of {", ".join(average_values["top3_genres"])}, featuring the iconic sounds of {", ".join(average_values["top3_artists"])}. 
            Picture {average_values["total"]} tracks, each averaging {average_values["duration"]}ms in duration and {average_values["tempo"]}bpm tempo. 
            From 0 to 1, the playlist is {average_values["acousticness"]} acoustic, {average_values["danceability"]} danceable, {average_values["energy"]} energetic, {average_values["instrumentalness"]} instrumental and {average_values["happiness"]} happy.
            What title captures the essence of this playlist's vibe? It's important that you respond with only the title, nothing else. Maximum 5 words."""
