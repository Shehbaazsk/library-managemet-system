from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.views import exception_handler


class CustomValidationError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "A custom validation error occurred."

    def __init__(self, detail=None, status_code=None):
        if detail:
            self.detail = detail
        if status_code:
            self.status_code = status_code


def custom_exception_handler(exc, context):
    # Call the default DRF exception handler
    response = exception_handler(exc, context)

    if response is not None:
        if isinstance(exc, CustomValidationError):
            # Customize the error response format
            response.data = {
                'error': exc.detail
            }
            response.status_code = exc.status_code

    return response
