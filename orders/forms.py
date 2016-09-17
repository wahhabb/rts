from django import forms
from localflavor.us.forms import USPhoneNumberField, USStateSelect
from orders.models import UserProfile
import re


def strip_non_numbers(data):
    """ gets rid of all non-number characters """
    non_numbers = re.compile('\D')
    return non_numbers.sub('', data)


class ProfileForm(forms.ModelForm):
    """ checkout form class to collect user billing and shipping information for placing an order """

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        # override default attributes
        for field in self.fields:
            self.fields[field].widget.attrs['size'] = '30'
#        self.fields['state'].widget.attrs['size'] = '3'
        self.fields['zip'].widget.attrs['size'] = '6'
        self.fields['state'].widget.attrs['size'] = '1'

    class Meta:
        model = UserProfile
        exclude = ('user', )
        widgets = {
            'state': USStateSelect(),
        }

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        stripped_phone = strip_non_numbers(phone)
        if len(stripped_phone) < 10:
            raise forms.ValidationError('Enter a valid phone number with area code.(e.g. 555-555-5555)')
        return self.cleaned_data['phone']

