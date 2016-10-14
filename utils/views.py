from django.views.generic.base import View
from django.core.exceptions import SuspiciousOperation

from .http import JSONResponse, DataJSONResponse
from tp_databases import settings as s

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
    max = None

    def get_since(self):
        """
        Get first number of element
        """
        if self.since is not None:
            return self.since
        try:
            self.since = int(self.request.GET.get(self.since_param_name, 0))
        except TypeError:
            raise SuspiciousOperation()
        return self.since

    def get_max(self):
        """
        Get last number of element
        """
        if self.max is not None:
            return self.max
        try:
            limit = int(self.request.GET.get(self.limit_param_name, -1))
            self.max = self.get_since() + limit if limit != -1 else None
        except TypeError:
            raise SuspiciousOperation()
        return self.max

    def get_object_list(self):
        """
        Returns an object list
        """
        qs = self.get_filtered_queryset()
        if self.get_max() is not None:
            return qs[self.get_since():self.get_max()]
        return qs[self.get_since():]

    def get_filtered_queryset(self):
        """
        Set order for queryset by default
        """
        qs = self.get_queryset()

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
