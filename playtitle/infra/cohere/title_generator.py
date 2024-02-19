from dataclasses import dataclass
from playtitle.infra.cohere.client import CohereClient


@dataclass(frozen=True)
class CohereTitleGenerator:
    cohere_client: CohereClient

    def generate_title(self):
        return self.cohere_client.client.generate(
            prompt="""Craft a title for a playlist that embodies the genres of rock, indie and pop-rock, featuring the iconic sounds of Muse, Oasis and The Beatles. 
            Picture 50 tracks, each averaging 250ms in duration, with 25 decibels and 80bpm tempo. 
            These songs paint a vivid sonic landscape, blending low acoustic tones with medium danceable rhythms and high happy vibes. 
            What title captures the essence of this playlist's vibe? It's important that you respond with only the title, nothing else. Maximum 5 words.""",
            temperature=1,
        )
