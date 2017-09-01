from django.conf.urls import url
from django.contrib import admin

from ui import views

urlpatterns = [
	url(r'^$', views.Index.as_view(), name='index'),
	url(r'^coursehomepage$', views.CourseHomePage.as_view(), name='coursehomepage'),

]