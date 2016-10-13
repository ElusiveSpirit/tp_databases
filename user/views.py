from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from django.http import Http404
from rest_framework.parsers import JSONParser

from tp_databases.settings import (RESPONSE_CODE_USER_ALREADY_EXISTS,
                                   RESPONSE_MSG_USER_ALREADY_EXISTS)
from utils.http import (DataJSONResponse, api_params_require, api_get_require, api_post_require,
                        JSONResponse)

from .serializers import UserSerializer
from .models import User

@api_post_require
def create_user(request):
    try:
        data = JSONParser().parse(request)
    except:
        raise PermissionDenied()

    try:
        User.objects.get(email=data.get('email'))
        return JSONResponse({
            'code': RESPONSE_CODE_USER_ALREADY_EXISTS,
            'response': RESPONSE_MSG_USER_ALREADY_EXISTS
        })
    except User.DoesNotExist:
        pass

    serializer = UserSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return DataJSONResponse(serializer.data)
    else:
        raise PermissionDenied()


@api_get_require
@api_params_require(param_list=['user'])
def get_user(request):
    user = get_object_or_404(User, email=request.GET.get('user'))
    serializer = UserSerializer(user)
    return DataJSONResponse(serializer.data)
