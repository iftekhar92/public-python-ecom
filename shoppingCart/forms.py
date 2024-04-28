from django import forms
from shoppingCart.models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ("full_name", "phone_number", "email", "pin_code", "full_address")
        widgets = {
            "full_name": forms.TextInput(attrs={"class": "form-control"}),
            "phone_number": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.TextInput(attrs={"class": "form-control"}),
            "pin_code": forms.TextInput(attrs={"class": "form-control"}),
            "full_address": forms.TextInput(attrs={"class": "form-control"}),
        }
