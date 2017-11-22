from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.login_register, name = 'signIn'),
    url(r'^home', views.adminHomePage, name = 'signIn'),
    url(r'^login_register', views.login_register, name = 'login'),
    url(r'^login_register_request/', views.login_register_request, name='login_register_request'),


]
