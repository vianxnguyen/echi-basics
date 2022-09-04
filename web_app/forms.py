from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

class CheckoutForm(forms.Form):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': "First Name",
        'class': 'form-control form-control-lg'
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': "Last Name",
        'class': 'form-control form-control-lg'
    }))
    email_address = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': "Email Address",
        'class': 'form-control form-control-lg'
    }))
    address_first = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': "Address Line 1",
        'class': 'form-control form-control-lg'
    }))
    address_second = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder': "Address Line 2 (Optional)",
        'class': 'form-control form-control-lg'
    }))
    country = CountryField(blank_label='(select country)').formfield(
        widget=CountrySelectWidget(attrs={
        'class': 'selectpicker country'
    }))
    city = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': "City",
        'class': 'form-control form-control-lg'
    }))
    state = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': "State / Region",
        'class': 'form-control form-control-lg'
    }))
    zip = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': "Zip",
        'class': 'form-control form-control-lg'
    }))

