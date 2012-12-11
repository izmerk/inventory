from django import forms
from django.forms import ModelForm
from mozdns.mx.models import MX
from mozdns.forms import BaseForm


class MXForm(BaseForm):
    class Meta:
        model = MX
        exclude = ('fqdn',)
        widgets = {'views': forms.CheckboxSelectMultiple}

class FQDNMXForm(BaseForm):
    class Meta:
        model = MX
        exclude = ('label', 'domain')
        fields = ('fqdn', 'server', 'ttl', 'views', 'description')
        widgets = {'views': forms.CheckboxSelectMultiple}
