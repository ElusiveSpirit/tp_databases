from django.conf.urls import url

from . import views as v

urlpatterns = [
    url(r'^(?P<type>(listFollowers)|(listFollowing))/', v.get_user_followers_list),
    url(r'^(?P<type>(un)?)follow/', v.follow_user),
    url(r'^create/', v.create_user),
    url(r'^updateProfile/', v.update_profile),
    url(r'^details/', v.get_user),
]
