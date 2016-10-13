from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer

from tp_databases import settings as s


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


def api_params_require(param_list, method='GET'):
    def decor_wrapper(func):
        def wrapper(request, *args, **kwargs):
            is_valid = True
            if method == 'GET':
                is_valid = all((request.GET.get(p) for p in param_list))
            elif method == 'POST':
                is_valid = all((request.GET.get(p) for p in param_list))

            if not is_valid:
                return JSONResponse({
                    'code': s.RESPONSE_CODE_INVALID_REQUEST,
                    'response': s.RESPONSE_MSG_INVALID_REQUEST
                })
            return func(request, *args, **kwargs)
        return wrapper
    return decor_wrapper


def api_get_require(func):
    def wrapper(request, *args, **kwargs):
        if request.method != 'GET':
            return JSONResponse({
                'code': s.RESPONSE_CODE_INVALID_REQUEST,
                'response': s.RESPONSE_MSG_INVALID_REQUEST
            })
        return func(request, *args, **kwargs)
    return wrapper
