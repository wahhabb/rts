from django.contrib.messages import success
from django.shortcuts import render, redirect
from django.views.generic import View

from orders.cart import get_cart_items
from .forms import ContactForm
from django.conf import settings
from django.core.mail import send_mail


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
            # mail_sent = bound_form.send_mail()
            mail_sent = send_mail(
                bound_form.cleaned_data.get('subject'),
                'Message from: {}\n\n{}\n'.format(bound_form.cleaned_data.get('email'), bound_form.cleaned_data.get('text')),
                settings.DEFAULT_FROM_EMAIL,
                [settings.EMAIL_ACCT, 'wahhab@deepwebworks.com']
            )
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
