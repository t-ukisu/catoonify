import logging
from rest_framework.views import exception_handler
from django.http import JsonResponse
from requests import ConnectionError

class ImageHandlingError(Exception):
    pass


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first
    import pdb; pdb.set_trace()
    response = exception_handler(exc, context)

    # checks if the raised exception is of the type you want to handle
    if isinstance(exc, ConnectionError):
        # defines custom response data
        err_data = {'MSG_HEADER': 'some custom error messaging'}

        # logs detail data from the exception being handled
        logging.error(f"Original error detail and callstack: {exc}")
        # returns a JsonResponse
        return JsonResponse(err_data, safe=False, status=503)

    elif isinstance(exc, ImageHandlingError):
        err_data = {'MSG_HEADER': f'Internal Server Error during image processing: {exc}'}

        # logs detail data from the exception being handled
        logging.error(f"Original error detail and callstack: {exc}")
        # returns a JsonResponse
        return JsonResponse(err_data, safe=False, status=503)

    # returns response as handled normally by the framework
    return response

