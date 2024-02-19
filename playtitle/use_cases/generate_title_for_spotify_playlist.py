from dataclasses import dataclass

from playtitle.domain.entities.spotify_playlist import SpotifyPlaylist
from playtitle.infra.interfaces.llm_client import LLMClient


@dataclass(frozen=True)
class GenerateTitleForSpotifyPlaylist:
    playlist: SpotifyPlaylist
    client: LLMClient

    def exec(self):
        return self.client.generate_response(self.__build_prompt)

    def __build_prompt(self):
        average_values = self.playlist.get_average_values()
        return f"""Craft a title for a playlist that embodies the genres of rock, indie and pop-rock, featuring the iconic sounds of Muse, Oasis and The Beatles. 
            Picture 50 tracks, each averaging 250ms in duration, with {average_values["loudness"]} decibels and {average_values["tempo"]}bpm tempo. 
            These songs paint a vivid sonic landscape, blending low acoustic tones with medium danceable rhythms and high happy vibes. 
            What title captures the essence of this playlist's vibe? It's important that you respond with only the title, nothing else. Maximum 5 words."""
