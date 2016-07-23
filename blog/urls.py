from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^create/$', views.create_post, name='create'),
	url(r'^list/$', views.list_posts, name='list'),
	url(r'^edit/(?P<pk>[0-9]+)/$', views.edit_post, name='edit'),
	url(r'^detail/(?P<pk>[0-9]+)/$', views.detail_post, name='detail'),
	url(r'^remove/(?P<pk>[0-9]+)/$', views.remove_post, name='remove'),

]
