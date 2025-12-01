"""
Custom exception handler for DRF
"""
from rest_framework.views import exception_handler
from rest_framework import status


def custom_exception_handler(exc, context):
    """
    Custom exception handler that returns response in envelope format
    {success, data, message, error_code?}
    """
    # Call DRF's default exception handler first
    response = exception_handler(exc, context)

    if response is not None:
        # Customize response format
        custom_response = {
            'success': False,
            'message': str(exc),
            'data': None,
        }

        # Add error details if available
        if hasattr(exc, 'detail'):
            if isinstance(exc.detail, dict):
                custom_response['errors'] = exc.detail
            elif isinstance(exc.detail, list):
                custom_response['errors'] = exc.detail
            else:
                custom_response['message'] = str(exc.detail)

        # Add error code for specific exceptions
        if hasattr(exc, 'default_code'):
            custom_response['error_code'] = exc.default_code

        response.data = custom_response

    return response
