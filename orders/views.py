from django.conf import settings
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.list import View

from orders.cart import *
from orders.cart import _cart_id
from orders.forms import ProfileForm

ANONYMOUS_PROFILE = 'anonymous_profile'
ANONYMOUS_USER = 99999


class ShowCart(View):
    template_name = 'orders/cart.html'

    def show(self, request):
        cart_issues = get_cart_items(request)
        cart_item_count = cart_issues.count()
        subtotal = cart_subtotal(request)
        if request.user.is_authenticated:
            try:
                profile = UserProfile.objects.get(user=request.user)
                has_profile = True
            except ObjectDoesNotExist:
                has_profile = False
        else:
            json_profile = request.session.get(ANONYMOUS_PROFILE, '')
            if json_profile == ' ':
                has_profile = False
            else:
                has_profile = True
        context = {'cart_item_count': cart_item_count,
                           'cart_items': cart_issues,
                           'cart_subtotal': subtotal,
                            'breaks': [3, 7, 11, 15, 19],
                            'has_profile': has_profile,
                   }
        return render(
            request, self.template_name, context
        )
    def get(self, request):
        return self.show(request)

    def post(self, request):
        postdata = request.POST.copy()
        if postdata['remove'] == 'remove':
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
        not_added = False
        p = get_object_or_404(Issue, catalog_id=cat_id)
        cart_issues = get_cart_items(request)
        issue_in_cart = False
        for cart_issue in cart_issues:
            if cart_issue.product.catalog_id == cat_id:
                issue_in_cart = True
                if cart_issue.quantity + quantity > cart_issue.product.quantity:
                    not_added = True
                else:
                    cart_issue.augment_quantity(quantity)
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
        response_data['cart_count'] = cart_distinct_item_count(request)
        response_data['not_added'] = not_added

        return JsonResponse(response_data)
    else:
        return JsonResponse({"nothing to see": "this shouldn't happen"})

class ProfileCreate(View):
    form_class = ProfileForm
    template_name = 'orders/add_profile.html'

    def get(self, request):
        return render(request, self.template_name, {'form': self.form_class()})

    def post(self, request):
        bound_form = self.form_class(request.POST)
        if bound_form.is_valid():
            if request.user.is_authenticated:
                new_profile = bound_form.save(commit=False)
                new_profile.user = request.user
                new_profile.save()
                return redirect('place_order')
            else:
                # save anonymous user to session data
                new_profile = bound_form.save(commit=False)
                request.session[ANONYMOUS_PROFILE] = serializers.serialize('json', [ new_profile, ])
                return redirect('place_order')
        else:
            return render(request, self.template_name, {'form': bound_form})


def get_profile(self, request):
    if request.user.is_authenticated:
        profile = get_object_or_404(
            self.model,
            user=request.user
        )
    else:
        json_profile = request.session.get(ANONYMOUS_PROFILE, '')
        # ToDo: handle error?
        for obj in serializers.deserialize("json", json_profile):
            profile = obj.object
    return profile


class ProfileUpdate(View):
    form_class = ProfileForm
    template_name = 'orders/update_profile.html'
    model = UserProfile

    def get(self, request):
        try:
            profile = get_profile(self, request)
        except:
            return redirect('profile_create')
        context = {
            'form': self.form_class(instance=profile),
            'profile': profile
        }
        return render(request, self.template_name, context)

    def post(self, request):
        profile = get_profile(self, request)
        bound_form = self.form_class(request.POST, instance=profile)
        if bound_form.is_valid():
            if request.user.is_authenticated:
                new_profile = bound_form.save()
            else:
                # update session data
                new_profile = bound_form.save(commit=False)
                request.session[ANONYMOUS_PROFILE] = serializers.serialize('json', [new_profile, ])
            return redirect('place_order')
        else:
            context = {
                'form': bound_form,
                'profile': profile,
            }
            return render(request, self.template_name, context)


class PlaceOrder(View):
    template_name = 'orders/place_order.html'

    def get(self, request):
        cart_issues = get_cart_items(request)
        cart_item_count = cart_issues.count()
        subtotal = cart_subtotal(request)
        shipping = shipping_charge(request)
        if request.user.is_authenticated:
            try:
                profile = UserProfile.objects.get(user=request.user)
            except ObjectDoesNotExist:
                return redirect(ProfileCreate)
        else:
            json_profile = request.session.get(ANONYMOUS_PROFILE, '')
            if json_profile == ' ':
                return redirect(ProfileCreate)
            else:
                # deserialize into new object
                for obj in serializers.deserialize("json", json_profile):
                    profile = obj.object

        context = {'cart_item_count': cart_item_count,
                           'cart_items': cart_issues,
                           'cart_subtotal': subtotal,
                            'breaks': [3, 7, 11, 15, 19],
                            'profile': profile,
                            'shipping': shipping,
                            'paypal_url': settings.PAYPAL_URL,
                            'cart_total': subtotal + shipping,
                            'site_name': settings.SITE_URL,
                   }
        return render(
            request, self.template_name, context
        )

class CompleteOrder(View):
    template_name = 'orders/complete_order.html'

    def get(self, request):
        cart_issues = get_cart_items(request)
        subtotal = cart_subtotal(request)
        if request.user.is_authenticated:
            try:
                profile = UserProfile.objects.get(user=request.user)
            except ObjectDoesNotExist:
                return redirect(ProfileCreate)
        else:
            json_profile = request.session.get(ANONYMOUS_PROFILE, '')
            if json_profile == ' ':
                return redirect(ProfileCreate)
            else:
                # deserialize into new object
                for obj in serializers.deserialize("json", json_profile):
                    profile = obj.object
                    if  not request.user.is_authenticated:
                        profile.user = User.objects.get(pk=ANONYMOUS_USER)
        # 1. Create Order record from Profile, 2. Add items to order
        # 3. Delete cart items 4. Reduce item quantity or Mark items as sold
        order = Order.create(profile, cart_issues[0].cart_id, shipping_charge(request),
                             cart_subtotal(request) + shipping_charge(request))
        order.save()
        for issue in cart_issues:
            product = issue.product
            new_order_item = IssueInOrder.objects.create(
                order=order, issue=product, quantity=issue.quantity, sale_price = issue.price)
            new_order_item.save()
            issue.delete()
            # get product
            product.quantity -= new_order_item.quantity
            if product.quantity <= 0:
                product.sold_date = now()
                product.status = 'sold'
            product.save()

        context = {}
        return render(
            request, self.template_name, context
        )