# -*- coding: utf-8 -*-
from kay.utils import forms

class TouchForm(forms.Form):
    x = forms.IntegerField()
    y = forms.IntegerField()
