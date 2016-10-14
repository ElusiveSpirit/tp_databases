from django.core.exceptions import PermissionDenied, SuspiciousOperation
from django.shortcuts import get_object_or_404

from tp_databases.settings import (RESPONSE_CODE_USER_ALREADY_EXISTS,
                                   RESPONSE_MSG_USER_ALREADY_EXISTS)
from utils.utils import parse_json_or_error
from utils.http import (DataJSONResponse, api_params_require, api_get_require, api_post_require,
                        JSONResponse)

from .serializers import UserSerializer, UserDetailSerializer, UserFollowSerializer
from .models import User

SORT_ORDERS = {
    'asc': 'name',
    'desc': '-name'
}


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


@api_get_require
@api_params_require(param_list=['user'])
def get_user_followers_list(request, type):
    user = get_object_or_404(User, email=request.GET.get('user'))
    if type == 'listFollowers':
        followers_list = user.followers.all()
    else:
        followers_list = user.following.all()

    if 'order' in request.GET:
        if request.GET.get('order') not in SORT_ORDERS:
            raise SuspiciousOperation()
        followers_list = followers_list.order_by(SORT_ORDERS[request.GET.get('order')])

    try:
        since_id = int(request.GET.get('since_id', 0))
        limit = int(request.GET.get('limit', -1))
        max_id = since_id + limit if limit != -1 else None
    except TypeError:
        raise SuspiciousOperation()

    serializer = UserDetailSerializer(followers_list[since_id:max_id], many=True)
    return DataJSONResponse(serializer.data)


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
