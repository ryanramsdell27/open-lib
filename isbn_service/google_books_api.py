import requests


class GoogleBooksAPI:
    def __init__(self, api_key):
        self.endpoint = 'https://www.googleapis.com/books/v1/volumes'
        self.api_key = api_key

    def lookup(self, isbn: str):
        params = {
            'q': isbn,
            'key': self.api_key
        }

        r = requests.get(self.endpoint, params=params)

        if r.status_code != 200:
            return None

        if r.json()["kind"] != "books#volumes":
            return None

        if r.json()["totalItems"] == 0:
            return None

        return r.json()["items"][0]