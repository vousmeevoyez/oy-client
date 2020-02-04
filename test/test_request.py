from oy.request import OyRequest


def test_to_representation():
    http_request = OyRequest("username", "api-key")
    http_request.url = "https://sandbox.oyindonesia.com/staging/partner/api/inquiry"
    http_request.payload = {"recipient_bank": "014", "recipient_account": "1239812390"}
    http_request.method = "POST"

    request = http_request.to_representation()
    assert (
        request["url"] == "https://sandbox.oyindonesia.com/staging/partner/api/inquiry"
    )
    assert request["method"] == "POST"
    assert request["data"]
    # make sure header have username key content type and accept
    assert request["headers"]["Content-Type"]
    assert request["headers"]["Accept"]
    assert request["headers"]["X-OY-Username"]
    assert request["headers"]["X-Api-Key"]
    assert request["timeout"]
