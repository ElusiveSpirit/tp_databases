from django.conf.urls import url, include

urlpatterns = [
    url(r'^db/api/user/', include('user.urls')),
]

handler404 = 'utils.exceptions.handler_404'
handler400 = 'utils.exceptions.handler_400'
handler403 = 'utils.exceptions.handler_403'
handler500 = 'utils.exceptions.handler_500'
