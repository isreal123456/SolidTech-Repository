from django import forms
from django.forms import HiddenInput, ModelForm, inlineformset_factory

from Sellers.models import OrderItem, Order


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ('name','num_of_product')



class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ('item','quantity',)

OrderItemFormset = inlineformset_factory(Order,OrderItem,form=OrderItemForm,extra=5)