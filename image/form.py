from django import forms

from image.models import Photo
from django.contrib.auth.models import User


class edit(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['location', 'bed', 'price']
