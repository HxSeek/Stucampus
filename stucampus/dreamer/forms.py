from django import forms
from django.forms import RadioSelect

from stucampus.dreamer.models import Application


class AppForm(forms.ModelForm):

    sex = forms.ChoiceField(choices=Application.SEX, widget=RadioSelect())

    class Meta:
        model = Application
        exclude = ('apply_date')
