from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.shortcuts import render

from utils.views import BaseListView, BaseView, UpdateView, DetailView
from utils.http import (api_params_require)

from .models import Forum
from .serializers import (ForumSerializer, ForumDetailSerializer, PostSerializer)


class ForumCreateView(UpdateView):
    serializer_class = ForumSerializer

    def serializer_valid(self, serializer):
        serializer.save()
        return super(ForumCreateView, self).serializer_valid(serializer)


class ForumDetailView(DetailView):
    serializer = ForumDetailSerializer
    model = Forum
    field_name = 'short_name'
    param_name = 'forum'

    def get_serializer_kwargs(self):
        kwargs = super(ForumDetailView, self).get_serializer_kwargs()
        if 'related' in self.request.GET:
            kwargs.update({
                'related': ['user']
            })
        return kwargs


@method_decorator(api_params_require(param_list=['forum']), name='get')
class ForumPostListView(BaseListView):
    serializer_class = PostSerializer
    since_field_name = 'date'

    def get(self, request, *args, **kwargs):
        forum = get_object_or_404(Forum, short_name=self.request.GET.get('forum'))
        self.queryset = forum.thread_list.first().post_set.all()
        return super(ForumPostListView, self).get(request, *args, **kwargs)

    def get_serializer_kwargs(self):
        kwargs = super(ForumPostListView, self).get_serializer_kwargs()
        if 'related' in self.request.GET:
            kwargs.update({
                'related': self.request.GET['related']
            })
        return kwargs
