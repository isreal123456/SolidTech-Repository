from django import forms

from Warehouse.models import IncomingProduct, BadProduct


class IncomingProductForm(forms.ModelForm):
    class Meta:
        model = IncomingProduct
        fields = ["product","quantity"]


class BadProductForm(forms.ModelForm):
    class Meta:
        model = BadProduct
        fields = ["product","quantity"]