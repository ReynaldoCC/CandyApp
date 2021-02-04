from django import forms

from .models import Notify


class NotifyForm(forms.ModelForm):

    class Meta:
        model = Notify
        fields = ["main_text", "user", "level", ]

