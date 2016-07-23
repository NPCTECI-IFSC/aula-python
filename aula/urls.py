from django.conf.urls import url, include
from django.contrib import admin
from . import views
from blog.views import login_view, logout_view

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^admin/', admin.site.urls),
	url(r'^login/$', login_view, name='login'),
	url(r'^logout/$', logout_view, name='logout'),
	url(r'^post/', include('blog.urls', namespace='blog')),
]
