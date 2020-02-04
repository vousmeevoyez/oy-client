"""
    Oy Request
    __________________
"""
import json
from oy.core.request import HTTPRequest


class OyRequest(HTTPRequest):
    """ Request Class for handling Oy Request """

    def __init__(self, username, api_key, timeout=30):
        super().__init__(timeout)
        self.username = username
        self.api_key = api_key

    def setup_header(self, **config):
        self._header["Content-Type"] = "application/json"
        self._header["Accept"] = "application/json"
        self._header["X-OY-Username"] = self.username
        self._header["X-Api-Key"] = self.api_key

    def to_representation(self):
        response = super().to_representation()
        # convert data into json
        response["data"] = json.dumps(response["data"])
        return response
