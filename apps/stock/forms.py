from django import forms
from utils.forms import FormMixin

from .models import TransactionHour
from .models import PersonalGain
from .models import OfficialSharePrice


class TransactionHourForm(forms.ModelForm, FormMixin):
    class Meta:
        model = TransactionHour
        fields = (
            'start_time', 'end_time', 'is_maintain', 'maintain_desc', 'start_a', 'end_a', 'close_desc')


class PersonalGainForm(forms.ModelForm, FormMixin):
    class Meta:
        model = PersonalGain
        fields = ('valid_bet', 'grade_one', 'grade_two', 'grade_three', 'grade_four', 'grade_five')


class OfficialSharePriceForm(forms.ModelForm, FormMixin):
    class Meta:
        model = OfficialSharePrice
        fields = ('add_time', 'price')
