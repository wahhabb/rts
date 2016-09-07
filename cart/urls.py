from django.conf.urls import include, url
from  cart.views import *

urlpatterns = [
    url(r'^$', ShowCart.as_view(), name='show_cart'),
    url(r'add/$', add_to_cart, name='add_to_cart'),
    url(r'profile/create/$', ProfileCreate.as_view(), name='profile_create'),
    url(r'profile/update/$', ProfileUpdate.as_view(), name='profile_update'),
    url(r'place-order/$', PlaceOrder.as_view(), name='place_order'),
]