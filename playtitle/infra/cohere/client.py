from cohere import Client
from playtitle.infra.interfaces.llm_client import LLMClient


class CohereClient(LLMClient):
    __client: Client

    def __init__(self, api_key: str) -> None:
        self.__client = Client(api_key=api_key)

    @property
    def client(self):
        return self.__client

    def generate_response(self, prompt: str):
        return self.client.generate(prompt)
