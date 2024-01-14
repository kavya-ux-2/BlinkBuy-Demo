from django import forms
from django.contrib.auth.models import User
class Search(forms.Form):
    name=forms.CharField(widget =forms.TextInput(attrs={'placeholder': 'Search', 'class': 'form-control'}))