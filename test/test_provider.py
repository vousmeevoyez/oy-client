from unittest.mock import Mock, patch
from decimal import Decimal
import pytest

from oy.provider import OyProvider
from oy.core.exceptions import FetchError, StatusCodeError
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
    assert response["recipient_bank"]
    assert response["recipient_account"]
    assert response["recipient_name"]
    assert response["timestamp"]


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
    assert response["trx_id"]
    assert response["partner_trx_id"]
    assert response["recipient_bank"]
    assert response["recipient_account"]
    assert response["amount"]
    # make sure amount is decimal
    assert type(response["amount"]) == int


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
    assert response["recipient_account"]
    assert response["recipient_name"]
    assert response["recipient_bank"]
    assert response["amount"]
    assert response["trx_id"]
    assert response["partner_trx_id"]
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
            "id": "12345b1-23be-45670-a123-5ca678f12b3e",
            "status": {"code": "000", "message": "Success"},
            "amount": 10000,
            "va_number": "123456789182827272",
            "bank_code": "002",
            "is_open": False,
            "is_single_use": False,
            "expiration_time": 1582783668175,
            "va_status": "WAITING_PAYMENT",
            "username_display": "va name",
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
    assert response["amount"] == 10000
    assert response["va_number"] == "123456789182827272"
    assert response["bank_code"] == "002"
    assert response["is_open"] is False
    assert response["is_single_use"] is False
    assert response["expiration_time"] == 1582783668175
    assert response["va_status"] == "WAITING_PAYMENT"
    assert response["username_display"] == "va name"


@patch("oy.core.remote_call.RemoteCall")
def test_get_va(mock_remote_call, setup_request, setup_response):
    # mock fetch method on remote call as the same one as mock response
    # respresantion
    mock_response = setup_response(
        response={
            "id": "12345b1-23be-45670-a123-5ca678f12b3e",
            "status": {"code": "000", "message": "Success"},
            "amount": 10000,
            "va_number": "123456789182827272",
            "bank_code": "002",
            "is_open": False,
            "is_single_use": False,
            "expiration_time": 1582783668175,
            "va_status": "WAITING_PAYMENT",
            "username_display": "va name",
            "amount_detected": 0,
            "partner_user_id": "123456",
        }
    )
    mock_remote_call.fetch.return_value = mock_response.to_representation()

    provider = OyProvider(
        request=setup_request,
        response=setup_response,
        remote_call=mock_remote_call,
        base_url="https://sandbox.oyindonesia.com/staging/partner",
    )

    response = provider.get_va_info("12345b1-23be-45670-a123-5ca678f12b3e")
    assert response["amount"] == 10000
    assert response["va_number"] == "123456789182827272"
    assert response["bank_code"] == "002"
    assert response["is_open"] is False
    assert response["is_single_use"] is False
    assert response["expiration_time"] == 1582783668175
    assert response["va_status"] == "WAITING_PAYMENT"
    assert response["username_display"] == "va name"
    assert response["amount_detected"] == 0
    assert response["partner_user_id"] == "123456"


@patch("oy.core.remote_call.RemoteCall")
def test_update_va(mock_remote_call, setup_request, setup_response):
    # mock fetch method on remote call as the same one as mock response
    # respresantion
    mock_response = setup_response(
        response={
            "id": "1414255-12121-21212121-212121",
            "status": {"code": "000", "message": "Success"},
            "amount": 50000,
            "va_number": "1001234000000000001",
            "bank_code": "002",
            "is_open": True,
            "is_single_use": False,
            "expiration_time": 1582802205412,
            "va_status": "WAITING_PAYMENT",
            "username_display": "vaname",
            "partner_user_id": "12345677",
        }
    )
    mock_remote_call.fetch.return_value = mock_response.to_representation()

    provider = OyProvider(
        request=setup_request,
        response=setup_response,
        remote_call=mock_remote_call,
        base_url="https://sandbox.oyindonesia.com/staging/partner",
    )

    response = provider.update_va(
        "1414255-12121-21212121-212121", 50000, True, False, 60, False
    )
    assert response["amount"] == 50000
    assert response["va_number"] == "1001234000000000001"
    assert response["bank_code"] == "002"
    assert response["is_open"] is True
    assert response["is_single_use"] is False
    assert response["expiration_time"] == 1582802205412
    assert response["va_status"] == "WAITING_PAYMENT"
    assert response["username_display"] == "vaname"
    assert response["partner_user_id"] == "12345677"


@patch("oy.core.remote_call.RemoteCall")
def test_get_list_of_va(mock_remote_call, setup_request, setup_response):
    # mock fetch method on remote call as the same one as mock response
    # respresantion
    mock_response = setup_response(
        response={
            "total": 2,
            "data": [
                {
                    "id": "9a660428-3373-436b-b929-ef69698dd26f",
                    "amount": 12000.0000,
                    "va_number": "100536000000000006",
                    "bank_code": "002",
                    "is_open": True,
                    "is_single_use": False,
                    "expiration_time": 1582791896416,
                    "va_status": "EXPIRED",
                    "username_display": "username",
                    "amount_detected": 400000,
                    "partner_user_id": "12345",
                },
                {
                    "id": "de51383f-1557-409c-8542-dcb74ca76375",
                    "amount": 12000.0000,
                    "va_number": "100536000000000005",
                    "bank_code": "002",
                    "is_open": True,
                    "is_single_use": False,
                    "expiration_time": 1582790250609,
                    "va_status": "EXPIRED",
                    "username_display": "username",
                    "amount_detected": 500000,
                    "partner_user_id": "54321",
                },
            ],
            "status": {"code": "000", "message": "Success"},
        }
    )
    mock_remote_call.fetch.return_value = mock_response.to_representation()

    provider = OyProvider(
        request=setup_request,
        response=setup_response,
        remote_call=mock_remote_call,
        base_url="https://sandbox.oyindonesia.com/staging/partner",
    )

    response = provider.get_list_of_va()
    assert response["total"] == 2
    assert len(response["data"]) == 2


@patch("oy.core.remote_call.RemoteCall")
def test_get_list_of_va_transactions(mock_remote_call, setup_request, setup_response):
    # mock fetch method on remote call as the same one as mock response
    # respresantion
    mock_response = setup_response(
        response={
            "total": 2,
            "data": [
                {
                    "id": "9a660428-3373-436b-b929-ef69698dd26f",
                    "amount": 12000.0000,
                    "va_number": "100536000000000006",
                    "bank_code": "002",
                    "is_open": True,
                    "is_single_use": False,
                    "expiration_time": 1582791896416,
                    "va_status": "EXPIRED",
                    "username_display": "username",
                    "amount_detected": 400000,
                    "partner_user_id": "12345",
                },
                {
                    "id": "de51383f-1557-409c-8542-dcb74ca76375",
                    "amount": 12000.0000,
                    "va_number": "100536000000000005",
                    "bank_code": "002",
                    "is_open": True,
                    "is_single_use": False,
                    "expiration_time": 1582790250609,
                    "va_status": "EXPIRED",
                    "username_display": "username",
                    "amount_detected": 500000,
                    "partner_user_id": "54321",
                },
            ],
            "status": {"code": "000", "message": "Success"},
        }
    )
    mock_remote_call.fetch.return_value = mock_response.to_representation()

    provider = OyProvider(
        request=setup_request,
        response=setup_response,
        remote_call=mock_remote_call,
        base_url="https://sandbox.oyindonesia.com/staging/partner",
    )

    response = provider.get_list_of_va()
    assert response["total"] == 2
    assert len(response["data"]) == 2


@patch("oy.core.remote_call.RemoteCall")
def test_get_list_of_va_transactions(mock_remote_call, setup_request, setup_response):
    # mock fetch method on remote call as the same one as mock response
    # respresantion
    mock_response = setup_response(
response = {
    "id": "12345676788898",
    "status": {
        "code": "000",
        "message": "Success"
    },
    "data": [
        {
            "id": "d9c2963f-be14-4558-9380-5ba1db8ed156",
            "created": "2020-02-27 07:48:01",
            "name": "Static VA by username",
            "amount": 10000,
            "create_by": "Static VA by username",
            "last_update_by": "Static VA by username",
            "last_updated": 1582789681439,
            "admin_fee": 1000,
            "va_number": "123456000000000001"
        }
    ],
    "number_of_transaction": 1
}
    )
    mock_remote_call.fetch.return_value = mock_response.to_representation()

    provider = OyProvider(
        request=setup_request,
        response=setup_response,
        remote_call=mock_remote_call,
        base_url="https://sandbox.oyindonesia.com/staging/partner",
    )

    response = provider.get_list_of_va_transactions("12345676788898")
    assert response["number_of_transaction"] == 1
    assert len(response["data"]) == 1


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
