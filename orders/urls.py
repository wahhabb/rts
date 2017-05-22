from django.conf.urls import include, url
from  orders.views import *

urlpatterns = [
    url(r'^cart/$', ShowCart.as_view(), name='show_cart'),
    url(r'add/$', add_to_cart, name='add_to_cart'),
    url(r'^to_wish_list/$', wish_list_add, name='wish_list_add'),
    url(r'wish-list/$', ShowWishList.as_view(), name='wish_list'),
    url(r'profile/create/$', ProfileCreate.as_view(), name='profile_create'),
    url(r'profile/update/$', ProfileUpdate.as_view(), name='profile_update'),
    url(r'review/$', ReviewOrder.as_view(), name='review_order'),
    url(r'thanks', CompleteOrder.as_view(), name='complete_order'),
    url(r'order_history', ShowOrderHistory.as_view(), name='order_history'),
    url(r'order_update', OrderUpdate.as_view(), name='order_update'),
]