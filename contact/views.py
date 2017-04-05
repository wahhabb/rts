from django.contrib.messages import success
from django.shortcuts import render, redirect
from django.views.generic import View

from orders.cart import get_cart_items
from .forms import ContactForm


# Create your views here.
class ContactView(View):
    form_class = ContactForm
    template_name = 'contact/contact_form.html'


    def get(self, request):
        cart_issues = get_cart_items(request)
        cart_item_count = cart_issues.count()
        user_email = ''
        if request.user.is_authenticated:
            user_email = request.user.email
        scan_item = self.request.GET.get('scan')

        return render(request,
                      self.template_name,
                      {'form': self.form_class(),
                       'user_email': user_email,
                       'cart_item_count': cart_item_count,
                       'scan_item': scan_item,
                       }
        )

    def post(self, request):
        bound_form = self.form_class(request.POST)
        if bound_form.is_valid():
            mail_sent = bound_form.send_mail()
            if mail_sent:
                # shortcut for add_message
                success(
                    request,
                    'Your message successfully sent.'
                )
                return redirect('issue_list')
        return render(request,
                      self.template_name,
                      {'form': bound_form}
        )
