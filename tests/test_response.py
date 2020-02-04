import pytest
from oy.response import OyResponse
from oy.core.exceptions import ResponseError


def test_to_representation_success(setup_http_response):
    """ simulate success response from oy """
    oy_response = {
        "status": {"code": "000", "message": "Success"},
        "recipient_bank": "014",
        "recipient_account": "1239812390",
        "recipient_name": "John Doe",
        "timestamp": "16-10-2019 09:55:31",
    }

    mock_http_response = setup_http_response(200, oy_response)

    http_request = OyResponse()
    http_request.set(mock_http_response)
    # make sure response doesnt contain status
    response = http_request.to_representation()
    assert response["recipient_bank"]
    assert response["recipient_account"]
    assert response["recipient_name"]
    assert response["timestamp"]

    # simulate oy return 101
    oy_response = {
        "status": {"code": "101", "message": "Request is Processed"},
        "amount": 100000,
        "timestamp": "03-02-2020 04:44:35",
        "recipient_bank": "009",
        "recipient_account": "3571113172",
        "trx_id": "65f3f8eb-f521-4222-bfd0-f68d5553d488",
        "partner_trx_id": "1580705076",
    }

    mock_http_response = setup_http_response(200, oy_response)

    http_request = OyResponse()
    http_request.set(mock_http_response)
    # make sure response doesnt contain status
    response = http_request.to_representation()
    assert response["recipient_bank"]
    assert response["recipient_account"]
    assert response["trx_id"]
    assert response["partner_trx_id"]
    assert response["timestamp"]


def test_to_representation_failed(setup_http_response):
    """ simulate all failed respons here """
    # simulate oy return 205
    oy_response = {"status": {"code": "205", "message": "Bank Code is not Found"}}

    mock_http_response = setup_http_response(200, oy_response)

    http_request = OyResponse()
    http_request.set(mock_http_response)
    # make sure response doesnt contain status
    with pytest.raises(ResponseError):
        http_request.to_representation()

    # simulate oy return 209
    oy_response = {"status": {"code": "209", "message": "Bank Account is not Found"}}

    mock_http_response = setup_http_response(200, oy_response)

    http_request = OyResponse()
    http_request.set(mock_http_response)
    # make sure response doesnt contain status
    with pytest.raises(ResponseError):
        http_request.to_representation()

    # simulate oy return 999
    oy_response = {"status": {"code": "999", "message": "Internal Server Error"}}

    mock_http_response = setup_http_response(200, oy_response)

    http_request = OyResponse()
    http_request.set(mock_http_response)
    # make sure response doesnt contain status
    with pytest.raises(ResponseError):
        http_request.to_representation()

    # simulate oy return 203
    oy_response = {"status": {"code": "203", "message": "Duplicate Partner Tx Id"}}

    mock_http_response = setup_http_response(200, oy_response)

    http_request = OyResponse()
    http_request.set(mock_http_response)
    # make sure response doesnt contain status
    with pytest.raises(ResponseError):
        http_request.to_representation()

    # simulate oy return 204
    oy_response = {"status": {"code": "204", "message": "Tx Id is not found"}}

    mock_http_response = setup_http_response(200, oy_response)

    http_request = OyResponse()
    http_request.set(mock_http_response)
    # make sure response doesnt contain status
    with pytest.raises(ResponseError):
        http_request.to_representation()

    # simulate oy return 201
    oy_response = {"status": {"code": "201", "message": "User is not found"}}

    mock_http_response = setup_http_response(200, oy_response)

    http_request = OyResponse()
    http_request.set(mock_http_response)
    # make sure response doesnt contain status
    with pytest.raises(ResponseError):
        http_request.to_representation()

    # simulate oy return 202
    oy_response = {"status": {"code": "201", "message": "User is not active"}}

    mock_http_response = setup_http_response(200, oy_response)

    http_request = OyResponse()
    http_request.set(mock_http_response)
    # make sure response doesnt contain status
    with pytest.raises(ResponseError):
        http_request.to_representation()
