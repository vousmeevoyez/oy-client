"""
    Test Client Fetch
"""
import pytest
from unittest.mock import Mock, patch
from requests.exceptions import Timeout, SSLError, ConnectionError

from oy.core.remote_call import RemoteCall
from oy.core.request import HTTPRequest
from oy.core.response import HTTPResponse
from oy.core.exceptions import FetchError, InvalidResponseError


def test_fetch(setup_request, setup_response):
    # prepare request
    mock_request = setup_request()
    mock_response = setup_response()

    response = RemoteCall().fetch(mock_request, mock_response)
    assert response


@patch("requests.request")
def test_fetch_timeout_error(mock_requests, setup_request, setup_response):
    # prepare request
    mock_request = setup_request()
    mock_response = setup_response()

    mock_requests.side_effect = Timeout
    with pytest.raises(FetchError):
        RemoteCall().fetch(mock_request, mock_response)


@patch("requests.request")
def test_fetch_ssl_error(mock_requests, setup_request, setup_response):
    # prepare request
    mock_request = setup_request()
    mock_response = setup_response()

    mock_requests.side_effect = SSLError
    with pytest.raises(FetchError):
        RemoteCall().fetch(mock_request, mock_response)


@patch("requests.request")
def test_fetch_connection_error(mock_requests, setup_request, setup_response):
    # prepare request
    mock_request = setup_request()
    mock_response = setup_response()

    mock_requests.side_effect = ConnectionError
    with pytest.raises(FetchError):
        RemoteCall().fetch(mock_request, mock_response)
