from django import forms
from utils.forms import FormMixin


class MemberInfoForms(forms.Form, FormMixin):
    username = forms.CharField(max_length=128, required=False)
    category = forms.CharField(required=False)
    amount = forms.CharField(required=False)
    add_date = forms.DateField(required=False)
