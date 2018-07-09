from django.conf.urls import url, include
from . import views

app_name='home'
urlpatterns = [
    url(r'^client-survey$', views.IndexView.as_view(), name='client_index'),
    url(r'^agency-survey$', views.IndexView.as_view(), name='agency_index'),
]
