from django.conf.urls import include, url
from  cart.views import *

urlpatterns = [
    url(r'^$', ShowCart.as_view(), name='show_cart'),
    url(r'add/', add_to_cart, name='add_to_cart'),
]