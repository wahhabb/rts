from django.shortcuts import  get_object_or_404
from orders.models import *
import decimal, random


CART_ID_SESSION_KEY = 'cart_id'


def _cart_id(request):
    """ get the current user's cart id, sets new one if blank;
    Note: the syntax below matches the text, but an alternative,
    clearer way of checking for a cart ID would be the following:

    if not CART_ID_SESSION_KEY in request.session:

    """
    if request.session.get(CART_ID_SESSION_KEY, '') == '':
        request.session[CART_ID_SESSION_KEY] = _generate_cart_id()
    return request.session[CART_ID_SESSION_KEY]


def _generate_cart_id():
    """ function for generating random cart ID values """
    cart_id = ''
    characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890!@#$%^&*()'
    cart_id_length = 50
    for y in range(cart_id_length):
        cart_id += characters[random.randint(0, len(characters) - 1)]
    return cart_id


def get_cart_items(request):
    """ return all items from the current user's cart """
    return CartItem.objects.filter(cart_id=_cart_id(request))


def get_cart_issues(request):
    items = list(get_cart_items(request))
    return [item.product for item in items]


def get_single_item(request, item_id):
    return get_object_or_404(CartItem, id=item_id, cart_id=_cart_id(request))


def get_wish_list_issues(request):
    if request.user.is_authenticated:
        items = WishList.objects.filter(user=request.user)
        return [item.issue for item in items]
    return []


# update quantity for single item
def update_cart(request):
    """ function takes a POST request that updates the quantity for single product instance in the
    current customer's shopping cart

    """
    postdata = request.POST.copy()
    item_id = postdata['item_id']
    quantity = postdata['quantity']
    cart_item = get_single_item(request, item_id)
    if cart_item:
        if int(quantity) > 0:
            cart_item.quantity = int(quantity)
            cart_item.save()
        else:
            remove_from_cart(request)


# remove a single item from cart
def remove_from_cart(request):
    """ function that takes a POST request removes a single product instance from the current customer's
    shopping cart
    """
    postdata = request.POST.copy()
    item_id = postdata['item_id']
    cart_item = get_single_item(request, item_id)
    if cart_item:
        cart_item.delete()


def cart_subtotal(request):
    """ gets the subtotal for the current shopping cart """
    cart_total = decimal.Decimal('0.00')
    cart_products = get_cart_items(request)
    for cart_item in cart_products:
        cart_total += cart_item.product.price * cart_item.quantity
    return cart_total

def shipping_charge(request):
    # ToDo: Calculate!
    ship_total = decimal.Decimal('6.75')
    cart_products = get_cart_items(request)
    for cart_item in cart_products:
        ship_total += decimal.Decimal(0.25)
        if cart_item.product.catalog_id == 'PJ-1-4':    # check for Photo-Journals
            return decimal.Decimal(16)
        if cart_item.product.catalog_id in ['PJ-1&2', 'PJ-3&4']:
            return decimal.Decimal(10)
        if cart_item.product.catalog_id in ['PJ-1', 'PJ-2', 'PJ-3', 'PJ-4']:
            return decimal.Decimal(7)
    return ship_total

# returns the total number of items in the user's cart
def cart_distinct_item_count(request):
    return get_cart_items(request).count()


def is_empty(request):
    return cart_distinct_item_count(request) == 0


def empty_cart(request):
    """ empties the shopping cart of the current customer """
    user_cart = get_cart_items(request)
    user_cart.delete()


def remove_old_cart_items():
    """ 1. calculate date of 90 days ago (or session lifespan)
    2. create a list of cart IDs that haven't been modified
    3. delete those CartItem instances

    """
#   ToDo: Trigger this
    print
    "Removing old carts"
    remove_before = datetime.now() + timedelta(days=-settings.SESSION_COOKIE_DAYS)
    cart_ids = []
    old_items = CartItem.objects.values('cart_id').annotate(last_change=Max('date_added')).filter(
        last_change__lt=remove_before).order_by()
    for item in old_items:
        cart_ids.append(item['cart_id'])
    to_remove = CartItem.objects.filter(cart_id__in=cart_ids)
    to_remove.delete()
    print
    str(len(cart_ids)) + " carts were removed"
