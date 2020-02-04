"""
    Provider
    _________________
"""

# base exceptions
from oy.core.exceptions import (
    BaseError,
    StatusCodeError,
    InvalidResponseError,
    ResponseError,
    FetchError
)
from oy.exceptions import ProviderError


class BaseProvider:
    """ Base Provider """

    def __init__(self, request, response, remote_call, base_url=None, port=None):
        # generate request response
        self._request_contract = request
        self._response_contract = response
        self._remote_call = remote_call
        # build url
        self.base_url = base_url
        self.port = port

    @property
    def request_contract(self):
        return self._request_contract

    @request_contract.setter
    def request_contract(self, contract):
        self._request_contract = contract

    @property
    def response_contract(self):
        return self._response_contract

    @response_contract.setter
    def response_contract(self, contract):
        self._response_contract = contract

    def build_url(self, requested_url):
        """
            provider method to build right url to be requested
            if base_url + port is provided we generate:
                base_url+port+requested_url

            if !base_url + !port is provided we generate:
                requested_url
        """
        url = requested_url
        if self.base_url is not None:
            url = self.base_url + requested_url
            if self.port is not None:
                # if we connect to specific port we need to add it as path to
                url = self.base_url + ":" + self.port + requested_url
        return url

    def prepare_request(self, **kwargs):
        """ prepare parameter and extract it into right request """
        self.request_contract.url = self.build_url(kwargs["url"])
        self.request_contract.method = kwargs["method"]
        self.request_contract.payload = kwargs["payload"]

    def call(self):
        """ wrapper function to encapsulate request & response contract!"""
        try:
            response = self._remote_call.fetch(
                self.request_contract, self.response_contract
            )
        except FetchError as error:
            raise ProviderError(error.message, error.original_exception)
        except StatusCodeError as error:
            raise ProviderError(error.message, error.original_exception)
        except ResponseError as error:
            raise ProviderError(error.message, error.original_exception)
        except InvalidResponseError as error:
            raise ProviderError(error.message, error.original_exception)
        # end try
        return response

    def execute(self, **kwargs):
        self.prepare_request(**kwargs)
        return self.call()
