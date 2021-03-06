from tp_databases import settings as s

from .http import JSONResponse

ERROR_404_TEMPLATE_NAME = '404.html'
ERROR_403_TEMPLATE_NAME = '403.html'
ERROR_400_TEMPLATE_NAME = '400.html'
ERROR_500_TEMPLATE_NAME = '500.html'


def handler_400(request, exception, template_name=ERROR_404_TEMPLATE_NAME):
    """For wrong request

    Raised by SuspiciousOperation
    """
    return JSONResponse({
        'code': s.RESPONSE_CODE_INVALID_REQUEST,
        'response': s.RESPONSE_MSG_INVALID_REQUEST
    })


def handler_403(request, exception, template_name=ERROR_404_TEMPLATE_NAME):
    """Wrong params

    Raised by PermissionDenied
    """
    print(exception)
    return JSONResponse({
        'code': s.RESPONSE_CODE_NOT_VALID,
        'response': s.RESPONSE_MSG_NOT_VALID
    })


def handler_404(request, exception, template_name=ERROR_404_TEMPLATE_NAME):
    """Not found
    Raised by Http404
    """
    return JSONResponse({
        'code': s.RESPONSE_CODE_OBJECT_NOT_FOUND,
        'response': s.RESPONSE_MSG_OBJECT_NOT_FOUND
    })


def handler_500(request, template_name=ERROR_404_TEMPLATE_NAME):
    """
    Server error
    """
    return JSONResponse({
        'code': s.RESPONSE_CODE_UNEXPECTED_ERROR,
        'response': s.RESPONSE_MSG_UNEXPECTED_ERROR
    })
