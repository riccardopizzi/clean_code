import urllib
from src.utils.io import ApiConnector
from http.client import HTTPResponse


class RapidApiConnector(ApiConnector):
    def __init__(self, api_key):
        self._api_key = api_key
        self._base_url = "https://api-nba-v1.p.rapidapi.com"
        self._headers = {
            "x-rapidapi-host": "api-nba-v1.p.rapidapi.com",
            "x-rapidapi-key": self._api_key,
        }

    def read(self, path="", mode=None) -> HTTPResponse:
        url = "/".join([self._base_url, path])
        req = urllib.request.Request(url, headers=self._headers)
        response = urllib.request.urlopen(req)
        return response
