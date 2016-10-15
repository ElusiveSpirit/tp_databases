from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator

from tp_databases.settings import (RESPONSE_CODE_USER_ALREADY_EXISTS,
                                   RESPONSE_MSG_USER_ALREADY_EXISTS)
from utils.views import BaseListView
from utils.utils import parse_json_or_error
from utils.http import (DataJSONResponse, api_params_require, api_get_require, api_post_require,
                        JSONResponse)
from forum.serializers import PostSerializer

from .serializers import (UserSerializer, UserDetailSerializer, UserFollowSerializer,
                          UserUpdateSerializer)
from .models import User

SORT_ORDERS = {
    'asc': 'name',
    'desc': '-name'
}


@api_post_require
def follow_user(request, type):
    """
    Follow or unfollow user
    """
    data = parse_json_or_error(request)
    serializer = UserFollowSerializer(data=data)
    if serializer.is_valid():
        if type == 'un':
            user = serializer.remove()
        else:
            user = serializer.save()
        serializer = UserDetailSerializer(user)
        return DataJSONResponse(serializer.data)
    else:
        raise PermissionDenied()


@method_decorator(api_params_require(param_list=['user']), name='get')
class UserFollowListView(BaseListView):
    since_param_name = 'since_id'
    since_field_name = 'pk'
    serializer_class = UserDetailSerializer

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, email=self.request.GET.get('user'))
        if kwargs['type'] == 'listFollowers':
            self.queryset = user.followers.all()
        else:
            self.queryset = user.following.all()
        return super(UserFollowListView, self).get(request, *args, **kwargs)


@method_decorator(api_params_require(param_list=['user']), name='get')
class UserPostListView(BaseListView):
    serializer_class = PostSerializer
    since_field_name = 'date'

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, email=self.request.GET.get('user'))
        self.queryset = user.post_set.all()
        return super(UserFollowListView, self).get(request, *args, **kwargs)


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


@api_post_require
def update_user(request):
    data = parse_json_or_error(request)
    serializer = UserUpdateSerializer(data=data)
    if serializer.is_valid():
        user = serializer.save()
        serializer = UserDetailSerializer(user)
        return DataJSONResponse(serializer.data)
    else:
        print(serializer.errors)
        raise PermissionDenied()


@api_get_require
@api_params_require(param_list=['user'])
def get_user(request):
    user = get_object_or_404(User, email=request.GET.get('user'))
    serializer = UserDetailSerializer(user)
    return DataJSONResponse(serializer.data)
