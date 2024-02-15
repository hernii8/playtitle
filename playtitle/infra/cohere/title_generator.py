from dataclasses import dataclass
from playtitle.infra.cohere.client import CohereClient

PROMPT = """Give me one title for a Spotify rock playlist that has this attributes:
- Main genre is rock
- Average popularity of the songs is 80 (from 0 to 100)
- There are 52 songs, 20 of them are explicit.
- The total duration of the playlist is 10000ms, the average duration of a song is 1923ms.
Give me only the title, nothing else. Maximum 10 words."""


@dataclass(frozen=True)
class CohereTitleGenerator:
    cohere_client: CohereClient

    def generate_title(self):
        return self.cohere_client.client.generate(
            prompt=PROMPT
        )
