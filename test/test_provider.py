from unittest.mock import Mock, patch
from decimal import Decimal
import pytest

from oy.provider import OyProvider
from oy.core.exceptions import (
    FetchError,
    StatusCodeError
)
from oy.exceptions import ProviderError


@patch("oy.core.remote_call.RemoteCall")
def test_inquiry_account_success(mock_remote_call, setup_request, setup_response):
    # mock fetch method on remote call as the same one as mock response
    # respresantion
    mock_response = setup_response(
        response={
            "status": {"code": "000", "message": "Success"},
            "recipient_bank": "014",
            "recipient_account": "1239812390",
            "recipient_name": "John Doe",
            "timestamp": "16-10-2019 09:55:31",
        }
    )
    mock_remote_call.fetch.return_value = mock_response.to_representation()

    provider = OyProvider(
        request=setup_request,
        response=setup_response,
        remote_call=mock_remote_call,
        base_url="https://sandbox.oyindonesia.com/staging/partner",
    )

    response = provider.inquiry_account("014", "1239812390")
    assert response["name"]
    assert response["account_no"]
    assert response["bank_code"]


@patch("oy.core.remote_call.RemoteCall")
def test_disburse(mock_remote_call, setup_request, setup_response):
    # mock fetch method on remote call as the same one as mock response
    # respresantion
    mock_response = setup_response(
        response={
            "status": {"code": "101", "message": "Request is Processed"},
            "amount": 125000,
            "recipient_bank": "014",
            "recipient_account": "1239812390",
            "trx_id": "ABC-456",
            "partner_trx_id": "1234-asdf",
            "timestamp": "16-10-2019 10:23:42",
        }
    )
    mock_remote_call.fetch.return_value = mock_response.to_representation()

    provider = OyProvider(
        request=setup_request,
        response=setup_response,
        remote_call=mock_remote_call,
        base_url="https://sandbox.oyindonesia.com/staging/partner",
    )

    response = provider.disburse("014", "1239812390", 125000)
    assert response["trx_reference"]
    assert response["bank_code"]
    assert response["account_no"]
    assert response["amount"]
    # make sure amount is decimal
    assert type(response["amount"]) == Decimal


@patch("oy.core.remote_call.RemoteCall")
def test_disburse_status(mock_remote_call, setup_request, setup_response):
    # mock fetch method on remote call as the same one as mock response
    # respresantion
    mock_response = setup_response(
        response={
            "status": {"code": "000", "message": "Success"},
            "amount": 125000,
            "recipient_name": "John Doe",
            "recipient_bank": "008",
            "recipient_account": "1234567890",
            "trx_id": "ABC-456",
            "partner_trx_id": "1234-asde",
            "timestamp": "16-10-2020 10:34:23",
            "created_date": "24-01-2020 06:48:08",
            "last_updated_date": "24-01-2020 06:48:39",
        }
    )
    mock_remote_call.fetch.return_value = mock_response.to_representation()

    provider = OyProvider(
        request=setup_request,
        response=setup_response,
        remote_call=mock_remote_call,
        base_url="https://sandbox.oyindonesia.com/staging/partner",
    )

    response = provider.disburse_status("1234-asde")
    assert response["account_no"]
    assert response["amount"]
    assert response["bank_code"]
    assert response["name"]
    assert response["trx_id"]
    assert response["trx_reference"]
    assert response["timestamp"]
    assert response["created_date"]
    assert response["last_updated_date"]


@patch("oy.core.remote_call.RemoteCall")
def test_get_balance(mock_remote_call, setup_request, setup_response):
    # mock fetch method on remote call as the same one as mock response
    # respresantion
    mock_response = setup_response(
        response={
            "status": {"code": "000", "message": "Success"},
            "balance": 125000,
            "timestamp": "10-12-2019 12:15:37",
        }
    )
    mock_remote_call.fetch.return_value = mock_response.to_representation()

    provider = OyProvider(
        request=setup_request,
        response=setup_response,
        remote_call=mock_remote_call,
        base_url="https://sandbox.oyindonesia.com/staging/partner",
    )

    response = provider.get_balance()
    assert response["balance"]


@patch("oy.core.remote_call.RemoteCall")
def test_generate_va(mock_remote_call, setup_request, setup_response):
    # mock fetch method on remote call as the same one as mock response
    # respresantion
    mock_response = setup_response(
        response={
            "status": {"code": "000", "message": "Success"},
            "amount": 500000,
            "vaNumber": "100536000000000001",
        }
    )
    mock_remote_call.fetch.return_value = mock_response.to_representation()

    provider = OyProvider(
        request=setup_request,
        response=setup_response,
        remote_call=mock_remote_call,
        base_url="https://sandbox.oyindonesia.com/staging/partner",
    )

    response = provider.generate_va("002", "500000", "oy00000001")
    assert response["amount"] == 500000
    assert response["va_no"] == "100536000000000001"


@patch("oy.core.remote_call.RemoteCall")
def test_inquiry_account_error(mock_remote_call, setup_request, setup_response):
    """ simulate inquiry account receive status error """
    mock_remote_call.fetch.side_effect = StatusCodeError

    provider = OyProvider(
        request=setup_request,
        response=setup_response,
        remote_call=mock_remote_call,
        base_url="https://sandbox.oyindonesia.com/staging/partner",
    )

    with pytest.raises(ProviderError):
        provider.inquiry_account("014", "1239812390")
