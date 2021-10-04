from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import ReadOnlyPasswordHashField, UserCreationForm
from .models import CustomerInfo


class SignUpUsers(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        labels = {'email': 'Email ID'}

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }


class AdditionalDetails(forms.ModelForm):
    class Meta:
        model = CustomerInfo
        fields = ['gender', 'locality', 'pincode', 'city', 'state', 'country']

        widgets = {
            'gender': forms.TextInput(attrs={'class': 'form-control'}),
            'locality': forms.TextInput(attrs={'class': 'form-control'}),
            'pincode': forms.NumberInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
        }
