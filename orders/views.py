from django.conf import settings
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.list import View
from django.core.mail import EmailMultiAlternatives
from email.mime.image import MIMEImage
from django.utils import timezone
import logging
from usps import USPSApi, Address

from orders.cart import *
from orders.cart import _cart_id
from orders.forms import ProfileForm

ANONYMOUS_PROFILE = 'anonymous_profile'
ANONYMOUS_USER = 99999

log = logging.getLogger(__name__)

class ShowCart(View):
    ''' View Shopping Cart '''
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
        if 'remove' in request.POST:
            remove_from_cart(request)
        if postdata['submit'] == 'Update':
            update_cart(request)
        return self.show(request)


class ShowWishList(View):
    ''' Show Want List '''
    tempate_name = 'orders/wish_list.html'

    def get(self, request):
        if request.user.is_authenticated:
            wish_list_items = WishList.objects.filter(user=request.user)
            context = {'wish_list_items': wish_list_items,
                       'needs_login': False}
            return render(request, self.tempate_name, context)
        else:
            return render(request, self.tempate_name, {'needs_login': True})

    def post(self, request):
        # if request.POST['remove'] == 'remove':
        issue = int(request.POST['item_id'])
        wish_list_item = WishList.objects.filter(issue__id=issue)
        print('got', len(wish_list_item), issue)
        wish_list_item.delete()
        if 'add_to_cart' in request.POST:
            p = get_object_or_404(Issue, pk=issue)
            cart_issues = get_cart_items(request)
            issue_in_cart = False
            for cart_issue in cart_issues:
                if cart_issue.product.catalog_id == issue:
                    issue_in_cart = True
                    # ToDo: Notify user that item is already in cart?
            if not issue_in_cart:
                ci = CartItem()
                ci.product = p
                ci.quantity = 1
                ci.cart_id = _cart_id(request)
                ci.save()
        return self.get(request)


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


# Wish List is AJAX call from main.js
@csrf_exempt
def wish_list_add(request):
    """ function that takes a POST request and adds a product instance to the current customer's wish list """
    if request.method == 'POST':
        postdata = request.POST.copy()
        issue_id = postdata.get('issue_id')
        user = request.user
        response_data = {}
        response_data['not_added'] = True
        if request.user.is_authenticated:
            p = get_object_or_404(Issue, id=issue_id)
            wish_item = WishList()
            wish_item.user = user
            wish_item.issue_id = issue_id
            wish_item.save()

            response_data['result'] = 'Add to wish list successful!'
            response_data['issue_id'] = issue_id
            response_data['product'] = str(p)
            response_data['not_added'] = False
        else:
            response_data['result'] = 'User not logged in'
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
        p1 = '060DE'
        p2 = 'EPW7093'
        if bound_form.is_valid():

            address = Address(
                name = "temporary",
                address_1 = bound_form.cleaned_data['address1'],
                address_2 = bound_form.cleaned_data['address2'],
                city=bound_form.cleaned_data['city'],
                state= bound_form.cleaned_data['state'],
                zipcode=bound_form.cleaned_data['zip'],
            )
            usps = USPSApi(p1+p2)
            try:
                validation = usps.validate_address(address)
                log.debug(validation.result)

                try:
                    error_message = validation.result['AddressValidateResponse']['Address']['Error']['Description']
                    error_message += ". Please correct or call us at (303)403-1840"
                    return render(request, self.template_name, {'form': bound_form, 'error_message': error_message})
                except:
                    address1 = validation.result['AddressValidateResponse']['Address']['Address1'].title()
                    address2 = validation.result['AddressValidateResponse']['Address']['Address2'].title()
                    city = validation.result['AddressValidateResponse']['Address']['City'].title()
                    if address1 == '-':
                        address1 = ''
                    if address2 == '-':
                        address2 = ''
                    zip4 = validation.result['AddressValidateResponse']['Address']['Zip4']
                    zip5 = validation.result['AddressValidateResponse']['Address']['Zip5']
                    new_zip = zip5 + '-' + zip4

                new_profile = bound_form.save(commit=False)
                new_profile.zip = new_zip
                new_profile.address1 = address1
                new_profile.address2 = address2
                new_profile.city = city
            except:
                new_profile = bound_form.save(commit=False)
                log.debug("address validation failedd")
            if request.user.is_authenticated:
                new_profile.user = request.user
                new_profile.save()
            else:
                # save anonymous user to session data
                request.session[ANONYMOUS_PROFILE] = serializers.serialize('json', [ new_profile, ])

            return redirect('review_order')
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


class ShowOrderHistory(View):
    tempate_name = 'orders/order_history.html'

    def get(self, request):
        if request.user.is_authenticated:
            order_issues = IssueInOrder.objects.filter(order__user=request.user)
            order_issues = order_issues.order_by('-order_id')
            context = {
                        # 'orders': orders,
                       'order_issues': order_issues,
                       'needs_login': False}
            return render(request, self.tempate_name, context)
        else:
            return render(request, self.tempate_name, {'needs_login': True})


class OrderUpdate(View):
    tempate_name = 'orders/order_history.html'

    def get(self, request):
        # Cancel order
        cancel_no = self.request.GET.get('cancel')
        if cancel_no is not None:
            # cancel order by adding back to inventory and deleting Order and IssueInOrder records
            order_issues = IssueInOrder.objects.filter(order_id=cancel_no)
            for issue_in_order in order_issues:
                issue = issue_in_order.issue
                # if issue.sold_date is not None:
                #     issue.sold_date = None  # TODO: recover last sold date? Leave unchanged?
                issue.quantity += issue_in_order.quantity
                issue.save()
                issue_in_order.delete()
            Order.objects.get(id=cancel_no).delete()

        # Cancel item from order
        cancel_item = self.request.GET.get('cancel_item')
        if cancel_item is not None:
            issue_in_order = IssueInOrder.objects.get(id=cancel_item)
            issue = issue_in_order.issue
            if issue.sold_date is not None: # TODO: recover last sold date? Leave unchanged?
                issue.sold_date = None
            issue.quantity += issue_in_order.quantity
            issue.save()
            issue_in_order.delete()

        # Mark order as shipped
        show_shipped = self.request.GET.get('show_shipped')
        if show_shipped is not None:
            # Mark order as shipped
            order = Order.objects.get(id=show_shipped)
            order.date_shipped = timezone.now()
            order.save()

        # Mark order as paid
        paid = self.request.GET.get('paid')
        if paid is not None:
            # Mark order as paid in full
            order = Order.objects.get(id=paid)
            order.payment_received = True
            order.save()

        if request.user.is_staff:
            order_issues = IssueInOrder.objects.filter(order__date_shipped__isnull=True)
            order_issues = order_issues.order_by('-order_id')
            context = {
                       'order_issues': order_issues,
                       'needs_login': False,
                        'is_update': True,
            }
            return render(request, self.tempate_name, context)
        else:
            return render(request, self.tempate_name, {'needs_staff': True})


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
            return redirect('review_order')
        else:
            context = {
                'form': bound_form,
                'profile': profile,
            }
            return render(request, self.template_name, context)


class ReviewOrder(View):
    template_name = 'orders/review_order.html'

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
                if not request.user.is_authenticated:
                    profile.user = User.objects.get(pk=ANONYMOUS_USER)
        do_not_ship = (profile.state in ['HI', 'AK', 'PR', 'AS', 'GU', 'MP', 'VI'])

        context = {'cart_item_count': cart_item_count,
                           'cart_items': cart_issues,
                           'cart_subtotal': subtotal,
                            'profile': profile,
                            'shipping': shipping,
                            'paypal_url': settings.PAYPAL_URL,
                            'paypal_email': settings.PAYPAL_EMAIL,
                            'cart_total': subtotal + shipping,
                            'site_name': settings.SITE_URL,
                            'go_to_paypal': 0,
                            'do_not_ship': do_not_ship,
                   }
        return render(
            request, self.template_name, context
        )

    def post(self, request):
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
                if not request.user.is_authenticated:
                    profile.user = User.objects.get(pk=ANONYMOUS_USER)
        # 1. Create Order record from Profile, 2. Add items to order
        # 3. Delete cart items 4. Reduce item quantity or Mark items as sold
        # Note that payment_received is set to False

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
        subject = 'RTSComics: Order being placed'
        from_email = 'orders@rtscomics.com'
        to_list = ['info@rtscomics.com']
        text_content = 'Use an email program that reads HTML!'
        msg = EmailMultiAlternatives(subject, text_content, from_email, to_list)
        html_content = '<!DOCTYPE html><body><h3>Ordered By</h3><p>' + profile.first_name + \
                       ' ' + profile.last_name + '</p>'
        html_content += '<h4>Address:</h4><p>' + profile.address1 + '<br>' + profile.address2 + '</p>'
        html_content += '<p>' + profile.city + ', ' + profile.state + ' ' + profile.zip + '</p>'
        html_content += '<h3>Order Items:</h3>'

        for item in cart_issues:
            html_content += '<p>' + str(item.product) + '<br>Qty: ' + str(item.quantity) + \
                            ' Unit Price: ' + str(item.price) + '</p>'

            if settings.DEBUG:
                f = 'comix/static/thumbnails/' + item.product.images.all()[0].file_name
            else:
                f = settings.STATIC_ROOT + '/thumbnails/' + item.product.images.all()[0].file_name
            fp = open(f, 'rb')
            msg_img = MIMEImage(fp.read())
            fp.close()
            msg_img.add_header('Content-ID', '<{}>'.format(item.product.images.all()[0].file_name))
            msg.attach(msg_img)
            html_content += '<p><img src="cid:' + \
                            item.product.images.all()[0].file_name + '" /></p>'
        html_content += '</body>'
        msg.attach_alternative(html_content, "text/html")
        msg.mixed_subtype = 'related'
        msg.send(fail_silently=False)
        context = {'cart_item_count': cart_item_count,
                           'cart_items': cart_issues,
                           'cart_subtotal': subtotal,
                            'profile': profile,
                            'shipping': shipping,
                            'paypal_url': settings.PAYPAL_URL,
                            'paypal_email': settings.PAYPAL_EMAIL,
                            'cart_total': subtotal + shipping,
                            'site_name': settings.SITE_URL,
                            'go_to_paypal': 1,
                   }
        return render(
            request, self.template_name, context
        )


class CompleteOrder(View):
    template_name = 'orders/complete_order.html'

    def get(self, request):
        cart_issues = get_cart_items(request)
        if len(cart_issues) == 0:   # Don't process if no order to process
            return render(
                request, self.template_name, {}
            )

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

        subject = 'RTSComics: Order was saved'
        from_email = 'info@rtscomics.com'
        to_list = ['info@rtscomics.com']
        text_content = 'Use an email program that reads HTML!'
        msg = EmailMultiAlternatives(subject, text_content, from_email, to_list)
        html_content = '<!DOCTYPE html><body><h3>Ordered By</h3><p>' + profile.first_name + \
                       ' ' + profile.last_name + '</p>'
        html_content += '<h4>Address:</h4><p>' + profile.address1 + '<br>' + profile.address2 + '</p>'
        html_content += '<p>' + profile.city + ', ' + profile.state + ' ' + profile.zip + '</p>'
        html_content += '<h3>Order Items:</h3>'

        for item in cart_issues:
            html_content += '<p>' + str(item.product) + '<br>Qty: ' + str(item.quantity) + \
                            ' Unit Price: ' + str(item.price) + '</p>'
            if settings.DEBUG:
                f = 'comix/static/thumbnails/' + item.product.images.all()[0].file_name
            else:
                f = settings.STATIC_ROOT + '/thumbnails/' + item.product.images.all()[0].file_name
            fp = open(f, 'rb')
            msg_img = MIMEImage(fp.read())
            fp.close()
            msg_img.add_header('Content-ID', '<{}>'.format(item.product.images.all()[0].file_name))
            msg.attach(msg_img)
            html_content += '<p><img src="cid:' + \
                            item.product.images.all()[0].file_name + '" /></p>'
        html_content += '</body>'
        msg.attach_alternative(html_content, "text/html")
        msg.mixed_subtype = 'related'
        msg.send(fail_silently=False)

        return render(
            request, self.template_name, {}
        )


class AccountUpdate(View):
    form_class = ProfileForm
    template_name = 'orders/my_account.html'
    model = UserProfile

    def get(self, request):
        if request.user.is_authenticated:
            profile = get_profile(self, request)
            context = {
                'form': self.form_class(instance=profile),
                'profile': profile,
                'needs_login': False,
            }
            return render(request, self.template_name, context)
        else:
            context = {
                'needs_login': True,
            }
            return render(request, self.template_name, context)

    def post(self, request):
        profile = get_profile(self, request)
        bound_form = self.form_class(request.POST, instance=profile)
        if bound_form.is_valid():
            bound_form.save()
            updated = True
        context = {
            'form': bound_form,
            'profile': profile,
            'updated': updated,
            'posting': True,
        }
        return render(request, self.template_name, context)


