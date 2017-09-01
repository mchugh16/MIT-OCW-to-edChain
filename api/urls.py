from django.conf.urls import url
from django.contrib import admin

from api import views

urlpatterns = [
	url(r'^feed$', views.Index.as_view(), name='index'),
	url(r'^course/(?P<pk>\d+)$', views.CourseDetail.as_view(), name='course'),
	]

