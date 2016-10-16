from django.conf.urls import url

from . import views as v

urlpatterns = [
    url(r'^create/', v.ForumCreateView.as_view()),
    url(r'^details/', v.ForumDetailView.as_view()),
]
