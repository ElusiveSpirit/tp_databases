from django.conf.urls import url

from . import views as v

urlpatterns = [
    url(r'^create/', v.create_user),
    url(r'^details/', v.get_user),
]
