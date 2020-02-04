"""
    Oy Response
    __________________
"""
from oy.core.response import HTTPResponse
from oy.core.exceptions import (
    ResponseError,
    DuplicateRequestError
)


class OyResponse(HTTPResponse):
    @staticmethod
    def _validate_oy_status(response):
        """
            Validate oy status
            ________________
            Parameters:
                response :
                    response from oy server

            Return:
                response :
                    response from oy server

            Raised:
                FailedResponseError :
                    if response from oy server contain status code other than
                    accepted status code we raise this

        """
        status_code = response["status"]["code"]
        if status_code not in ["000", "101"]:
            raise ResponseError("STATUS_FAILED", original_exception=response["status"]["message"])
        return response

    @staticmethod
    def _trim_response(response):
        """
            trim oy response
            ________________
            Parameters:
                response :
                    response from oy server

            Return:
                trimmed_response :
                    trimmed response from oy server without status object
        """
        response.pop("status")
        return response

    def validate_data(self):
        """ validate oy status """
        try:
            # first validate status any response
            self._validate_oy_status(self.data)
            trimmed_response = self._trim_response(self.data)
            self.data = trimmed_response
        except ResponseError as error:
            raise ResponseError("RESPONSE_FAILED", error.original_exception)
