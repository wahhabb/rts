"""rts URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import  admin
from django.contrib.auth import views as auth_views
#from django.core.urlresolvers import reverse_lazy
from django.urls import reverse_lazy
from django.contrib.auth.forms import AuthenticationForm
from registration.backends.simple.views import RegistrationView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.generic import TemplateView

from contact import urls as contact_urls
from imports.views import ImportExcelView, ShowSalesView
from orders.views import AccountUpdate
from comix.views import UnderConstructionPage

# Allow registration to return to page it came from
@method_decorator(csrf_protect, name="dispatch")
class MyRegistrationView(RegistrationView):
    def get_success_url(self, user):
        success_url = self.request.POST.get('next', '/')
        return success_url


urlpatterns = [
    # TEMPORARY: make site point to Under Construction
    # url(r'^.?', UnderConstructionPage.as_view(), name="under_contruction"),

    url(r'^admin/', admin.site.urls),

    url(r'^', include('comix.urls')),

    # url(r'^login/$', auth_views.login, {'template_name': 'user/login.html'}, name='login'),
    #
    # url(r'^logout/$', auth_views.logout, {'template_name': 'user/logout.html'}, name='logout'),

    url(r'^login/$', auth_views.LoginView.as_view(template_name='user/login.html'), name='login'),

    url(r'^logout/$', auth_views.LogoutView.as_view(template_name='user/logout.html'), name='logout'),

       # url(r'^password_change/$', auth_views.PasswordChange.as_view(template_name='registration/password_change.html'),
       #     name='password_change'),
       # url(r'^password_change/done/$', name='password_change_done'),


    url(r'^reset/$',
        auth_views.PasswordResetView.as_view(
            template_name='user/password_reset_form.html',
            email_template_name='user/password_reset_email.html',
            subject_template_name='user/password_reset_email_subject.txt',
            extra_context={'post_reset_redirect=reverse_lazy': 'pw_reset_sent'}),
        name='pw_reset_start'),
    url(r'^reset/sent/$',
        auth_views.PasswordResetDoneView.as_view(
            template_name='user/password_reset_sent.html'),
        name='password_reset_done'),
    url(r'^reset/'
        r'(?P<uidb64>[0-9A-Za-z_\-]+)/'
        r'(?P<token>[0-9A-Za-z]{1,13}'
        r'-[0-9A-Za-z]{1,20})/$',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='user/password_reset_confirm.html',
            extra_context={'post_reset_redirect': reverse_lazy('pw_reset_complete')}
        ),
        name='pw_reset_confirm'),
    url(r'reset/done/$',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='user/password_reset_complete.html',
            extra_context={'form': AuthenticationForm}
        ),
        name='pw_reset_complete'),

    url('^accounts/register', MyRegistrationView.as_view(), name='registration_register'),
    url(r'^accounts/', include('registration.backends.simple.urls')),

    url(r'^contact/', include(contact_urls,)),

    url(r'^my_account/$', AccountUpdate.as_view(), name='my_account'),

    url(r'^order/', include('orders.urls')),

    # url(r'^fixtest/$', TblComicsImportView.as_view(), name='publisher_fix'),

    url(r'^importexcel/$', ImportExcelView.as_view(), name='import_excel'),
    url(r'^showsales/$', ShowSalesView.as_view(), name='show_sales'),

    url(r'^robots.txt$', TemplateView.as_view(template_name="robots.txt", content_type="text/plain"), name="robots_file"),
    url(r'^sitemap.txt$', TemplateView.as_view(template_name='sitemap.txt', content_type='text/plain'), name="sitemap"),

]

