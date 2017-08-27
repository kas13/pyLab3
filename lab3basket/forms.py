from django import forms
from .models import *


class BasketForm(forms.ModelForm):
    class Meta:
        model = BasketModel
        exclude = [""]
