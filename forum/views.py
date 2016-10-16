from django.shortcuts import render

from utils.views import BaseListView, BaseView, UpdateView, DetailView

from .models import Forum
from .serializers import ForumSerializer, ForumDetailSerializer


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
