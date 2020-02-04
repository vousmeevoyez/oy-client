"""
    Oy client builder
"""
from oy.request import OyRequest
from oy.response import OyResponse
from oy.provider import OyProvider
from oy.core.remote_call import RemoteCall


def build_client(base_url, username, api_key):
    """" combine request response and remote call into provider """
    # we need to build request
    request = OyRequest(username, api_key)
    response = OyResponse()
    remote_call = RemoteCall()
    client = OyProvider(
        base_url=base_url,
        request=request,
        response=response,
        remote_call=remote_call,
    )
    return client
