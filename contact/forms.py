from django import forms
from django.core.exceptions import ValidationError
from django.core.mail import BadHeaderError, mail_managers

class ContactForm(forms.Form):

    email = forms.EmailField(label='Your Email', required=True)
    subject = forms.CharField(max_length=100, required=True)
    text = forms.CharField(widget=forms.Textarea, label='Enter Message', required=True)

    def send_mail(self):
        email = self.cleaned_data.get('email')
        text = self.cleaned_data.get('text')
        subject = self.cleaned_data.get('subject')
        body = 'Message from: {}\n\n{}\n'.format(email, text)
        try:
            # shortcut for send_mail
            mail_managers('RTS Comics: {}'.format(subject), body)
        except BadHeaderError:
            self.add_error(
                None,
                ValidationError(
                    'Could Not Send Email.\n'
                    'Extra Headers not allowed'
                    'in email body.',
                    code='badheader'
                )
            )
            return False
        else:
            return True