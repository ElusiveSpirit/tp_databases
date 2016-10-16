from django.views.generic.base import View
from django.http import Http404
from django.core.exceptions import SuspiciousOperation, PermissionDenied
from rest_framework.parsers import JSONParser

from .http import JSONResponse, DataJSONResponse
from tp_databases import settings as s


class BaseView(View):
    OBJECT_NOT_FOUND = Http404
    NOT_VALID = PermissionDenied
    INVALID_REQUEST = SuspiciousOperation

    serializer_class = None

    response_data = {}

    def get_response_data(self):
        """
        Returns data for response
        """
        return response_data

    def get(self, request, *args, **kwargs):
        return DataJSONResponse(self.get_response_data())

    def post(self, request, *args, **kwargs):
        return DataJSONResponse(self.get_response_data())

    def error(self, error=INVALID_REQUEST, msg=''):
        raise error(msg)


class UpdateView(BaseView):

    def post(self, request, *args, **kwargs):
        try:
            data = JSONParser().parse(request)
        except:
            self.error(BaseView.NOT_VALID)
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            return self.serializer_valid()
        else:
            return self.serializer_not_valid()

    def serializer_valid(self, serializer):

        return DataJSONResponse(self.get_response_data())

    def serializer_not_valid(self, serializer):
        self.error(BaseView.NOT_VALID)


class BaseListView(View):
    http_method_names = ['get']
    since_param_name = 'since'
    limit_param_name = 'limit'
    order_param_name = 'order'
    model = None
    queryset = None
    serializer_class = None
    order_field = None
    _ORDER_WAY_LIST = ['asc', 'desc']

    since = None
    since_field_name = None

    limit = None

    def get_since(self):
        """
        Returns kwarg for filter method
        """
        if self.since is not None:
            return self.since

        if (self.since_field_name is not None and
                self.since_param_name in self.request.GET):
            key = '{}__gt'.format(self.since_field_name)
            self.since = {
                key: self.request.GET[self.since_param_name]
            }
            return self.since

    def get_limit(self):
        """
        Get limit for elements
        """
        if self.limit is not None:
            return self.limit

        if self.limit_param_name in self.request.GET:
            try:
                self.limit = int(self.request.GET.get(self.limit_param_name))
            except TypeError:
                raise SuspiciousOperation()
            return self.limit

    def get_object_list(self):
        """
        Returns an object list
        """
        qs = self.get_filtered_queryset()
        if self.get_limit() is not None:
            return qs[:self.get_limit()]
        return qs

    def get_filtered_queryset(self):
        """
        Set order for queryset by default
        """
        qs = self.get_queryset()

        if self.get_since() is not None:
            qs = qs.filter(**self.get_since())

        if self.order_field is not None:
            order_field = self.order_field if self.order_field[0] != '-' else self.order_field[1:]
            if self.order_param_name in self.request.GET:
                if self.request.GET in self._ORDER_WAY_LIST:
                    if self.request.GET[self.order_param_name] == 'desc':
                        order_field = '-' + order_field
                else:
                    raise SuspiciousOperation()
            else:
                # DESC is default
                order_field = '-' + order_field
            qs = qs.order_by(order_field)
        return qs

    def get_queryset(self):
        """
        Just a queryset of model
        """
        if self.queryset is not None:
            return self.queryset
        return self.model.objects.all()

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.get_object_list(), many=True)
        return DataJSONResponse(serializer.data)

    def http_method_not_allowed(request, *args, **kwargs):
        """
        Return an error
        """
        return JSONResponse({
            'code': s.RESPONSE_CODE_INVALID_REQUEST,
            'response': 'Http method not allowed for this url'
        })
