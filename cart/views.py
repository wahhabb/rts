from django.shortcuts import render
from django.views.generic.list import View
from django.http import JsonResponse
from  cart.cart import *
from cart.cart import _cart_id
from django.views.decorators.csrf import csrf_exempt

class ShowCart(View):
    template_name = 'cart/cart.html'

    def show(self, request):
        cart_issues = get_cart_items(request)
        cart_item_count = cart_issues.count()
        subtotal = cart_subtotal(request)
        context = {'cart_item_count': cart_item_count,
                           'cart_items': cart_issues,
                           'cart_subtotal': subtotal,
                            'breaks': [3, 7, 11, 15, 19]}
        return render(
            request, self.template_name, context
        )
    def get(self, request):
        return self.show(request)

    def post(self, request):
        postdata = request.POST.copy()
        if postdata['submit'] == 'Remove':
            remove_from_cart(request)
        if postdata['submit'] == 'Update':
            update_cart(request)
        return self.show(request)


# Add to Cart is AJAX call from main.js
@csrf_exempt
def add_to_cart(request):
    """ function that takes a POST request and adds a product instance to the current customer's shopping cart """
    if request.method == 'POST':
        postdata = request.POST.copy()
        cat_id = postdata.get('catalog_id')
        quantity = postdata.get('quantity', 1)
        p = get_object_or_404(Issue, catalog_id=cat_id)
        cart_issues = get_cart_items(request)
        issue_in_cart = False
        for cart_issue in cart_issues:
            if cart_issue.product == cat_id:
                cart_issue.augment_quantity(quantity)
                issue_in_cart = True
        if not issue_in_cart:
            ci = CartItem()
            ci.product = p
            ci.quantity = quantity
            ci.cart_id = _cart_id(request)
            ci.save()

        response_data = {}
        response_data['result'] = 'Add to cart successful!'
        response_data['cat_id'] = cat_id
        response_data['product'] = str(p)
        response_data['cart_count'] = post.created.strftime('%B %d, %Y %I:%M %p')

        return JsonResponse(response_data)
    else:
        return JsonResponse({"nothing to see": "this shouldn't happen"})



