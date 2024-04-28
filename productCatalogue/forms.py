from django import forms
from productCatalogue.models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields='__all__'