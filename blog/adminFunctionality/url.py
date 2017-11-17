from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.adminHomePage, name = 'signIn'),
    url(r'^admin', views.adminHomePage, name = 'signIn'),
    url(r'^shoppingcart', views.shoppingcart, name = 'shoppingcart')
]
