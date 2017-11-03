from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name = 'index'),
    url(r'^index', views.index, name = 'index'),
    url(r'^Saajan', views.hiSaajan, name = 'saajan'),
    url(r'^tracking_home', views.tracking_home, name='tracking_home'),
    url(r'^tracking', views.tracking, name='tracking'),
    url(r'^contact_us', views.contact_us, name='contact_us'),
    url(r'^login_register', views.login_register, name='login_register'),
    url(r'^login_register_request/$', views.login_register_request, name='login_register_request'),
    url(r'^creditcard/', views.creditcard, name='creditcard'),
    url(r'^confirmation', views.confirmation, name='confirmation'),
]
