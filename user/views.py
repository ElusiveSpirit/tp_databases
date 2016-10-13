from utils.http import JSONResponse, api_params_require, api_get_require
from tp_databases import settings as s

from .serializers import UserSerializer
from .models import User


@api_get_require
@api_params_require(param_list=['user'])
def get_user(request):
    try:
        user = User.objects.get(email=request.GET.get('user'))
    except User.DoesNotExist:
        return JSONResponse({
            'code': s.RESPONSE_CODE_OBJECT_NOT_FOUND,
            'response': s.RESPONSE_MSG_OBJECT_NOT_FOUND
        })
    serializer = UserSerializer(user)
    return JSONResponse({
        'code': s.RESPONSE_CODE_OK,
        'response': serializer.data
    })
