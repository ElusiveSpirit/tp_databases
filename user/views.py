from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

from tp_databases.settings import (RESPONSE_CODE_USER_ALREADY_EXISTS,
                                   RESPONSE_MSG_USER_ALREADY_EXISTS)
from utils.utils import parse_json_or_error
from utils.http import (DataJSONResponse, api_params_require, api_get_require, api_post_require,
                        JSONResponse)

from .serializers import UserSerializer, UserDetailSerializer, UserFollowSerializer
from .models import User


@api_post_require
def follow_user(request):
    data = parse_json_or_error(request)
    serializer = UserFollowSerializer(data=data)
    if serializer.is_valid():
        user = serializer.save()
        serializer = UserDetailSerializer(user)
        return DataJSONResponse(serializer.data)
    else:
        raise PermissionDenied()


@api_post_require
def create_user(request):
    data = parse_json_or_error(request)

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
    serializer = UserDetailSerializer(user)
    return DataJSONResponse(serializer.data)
