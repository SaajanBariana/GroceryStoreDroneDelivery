from django.conf.urls import url
from . import views

urlpatterns = [
       url(r'^$', views.index, name = 'index'),
       url(r'^index', views.index, name = 'index'),
       url(r'^Saajan', views.hiSaajan, name = 'saajan'),
       url(r'^tracking_home', views.tracking_home, name='tracking_home'),
       url(r'^tracking', views.tracking, name='tracking'),
       url(r'^get_tracking_by_user_id', views.get_tracking_by_user_id, name='get_tracking_by_user_id'),
       url(r'^contact_us', views.contact_us, name='contact_us'),
       url(r'^login_register', views.login_register, name='login_register'),
       url(r'^profile', views.profile, name = 'profile'),
       url(r'^login_register_request/', views.login_register_request, name='login_register_request'),
       url(r'^navigation_bar/', views.navigation_bar, name=' navigation_bar'),
       url(r'^creditcard', views.creditcard, name='creditcard'),
       url(r'^confirmation', views.confirmation, name='confirmation'),
       url(r'^search', views.search, name = 'search_result'),
       url(r'^shoppingcart', views.shoppingcart, name='shoppingcart.html'),
       url(r'^profile', views.profile, name='profile'),
       url(r'(.*)/', views.handle404, name ='404 Error'),
       url(r'^update_delivery', views.update_delivery, name='update_delivery'),
]
