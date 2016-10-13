from django.conf.urls import url, include

urlpatterns = [
    url(r'^db/api/user/', include('user.urls')),
]
