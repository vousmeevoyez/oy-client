"""
    Fixtures
"""
from unittest.mock import Mock
import pytest


@pytest.fixture
def setup_http_response():
    def _make_http_response(status_code, response=None):
        """ fixture to create http response """
        http_response = Mock(status_code=status_code)
        if response is not None:
            http_response.json.return_value = response
        return http_response

    return _make_http_response


@pytest.fixture
def setup_request():
    def _make_request(
        method="POST",
        url="https://sandbox.oyindonesia.com/staging/partner/api/inquiry",
        data={"recipient_bank": "014", "recipient_account": "1239812390"},
    ):
        mock_request = Mock()
        mock_request.to_representation.return_value = {
            "method": method,
            "url": url,
            "data": data,
        }
        return mock_request

    return _make_request


@pytest.fixture
def setup_response():
    def _make_response(response=None, exception=None):
        mock_response = Mock()

        mock_response_payload = response
        if response is None:
            mock_response_payload = {
                "status": {"code": "000", "message": "Success"},
                "recipient_bank": "014",
                "recipient_account": "1239812390",
                "recipient_name": "John Doe",
                "timestamp": "16-10-2019 09:55:31",
            }

        mock_response.to_representation.return_value = mock_response_payload
        return mock_response

    return _make_response
