from django.conf.urls import url

from . import views

app_name = 'logs'
urlpatterns = [
    url(r'^$', views.LogIndexView.as_view(), name='index'),
    url(r'^new/$', views.LogNew.as_view(), name='new'),
    url(r'^(?P<pk>[0-9]+)/$', views.LogDetail.as_view(), name='detail'),
    url(r'^delete/(?P<pk>\d+)/$', views.LogDelete.as_view(), name='delete'),
    url(r'^update/(?P<pk>\d+)/$', views.LogUpdate.as_view(), name='update'),
]
