"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^home/', include('home.url')),
    url(r'^tracking_home', include('home.url')),
    url(r'^tracking/', include('home.url')),
    url(r'^get_tracking_by_user_id', include('home.url')),
    url(r'^contact_us/', include('home.url')),
    url(r'^login_register/', include('home.url')),
    url(r'^login_register_request/', include('home.url')),
    url(r'^navigation_bar/', include('home.url')),
    url(r'^creditcard', include('home.url')),
    url(r'^confirmation', include('home.url')),
    url(r'^shoppingcart/', include('home.url')),
    url(r'^search', include('home.url')),
    url(r'^admin/', include('adminFunctionality.url')),
    url(r'^', include('home.url')),
    url(r'^update_delivery', include('home.url')),
]
