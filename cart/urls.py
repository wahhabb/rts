from django.conf.urls import include, url
from  cart.views import *

app_name = 'cart'

urlpatterns = [
    url(r'^$', show_cart, {'template_name': 'cart/cart.html'}, name='show_cart'),
    url(r'add/', add_to_cart, name='add_to_cart'),
]