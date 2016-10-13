from django.shortcuts import get_object_or_404
from utils.http import JSONResponse, api_params_require, api_get_require
from tp_databases import settings as s

from .serializers import UserSerializer
from .models import User


@api_get_require
@api_params_require(param_list=['user'])
def get_user(request):
    user = get_object_or_404(User, email=request.GET.get('user'))
    serializer = UserSerializer(user)
    return JSONResponse({
        'code': s.RESPONSE_CODE_OK,
        'response': serializer.data
    })
