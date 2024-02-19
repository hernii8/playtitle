import json
from playtitle.infra.cohere.client import CohereClient


def test_client_init():
    with open("config/credentials.json") as file:
        credentials = json.load(file)
    cohere_client = CohereClient(
        api_key=credentials["cohere"]["api_key"]).client
    assert cohere_client.api_key is not None
