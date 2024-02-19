from playtitle.infra.cohere.client import CohereClient
import json


def test_cohere_client():
    with open("config/credentials.json") as file:
        credentials = json.load(file)
        api_key = credentials["cohere"]["api_key"]
    cohere = CohereClient(api_key=api_key)
    assert cohere.client.api_key == api_key
