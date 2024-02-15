from cohere import Client


class CohereClient:
    __client: Client

    def __init__(self, api_key: str) -> None:
        self.__client = Client(api_key=api_key)

    @property
    def client(self):
        return self.__client
