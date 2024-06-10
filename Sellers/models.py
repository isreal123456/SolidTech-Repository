from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse_lazy, reverse

from Warehouse.models import Product

user = get_user_model()

class Log(models.Model):
    log = models.CharField(max_length=10000000)
    date_created = models.DateTimeField(auto_now_add=True)

class Order(models.Model):
    seller = models.ForeignKey(user,on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=1000000)
    num_of_product = models.IntegerField(max_length=100000)
    created_at = models.DateField(auto_now_add=True)
    completed = models.BooleanField(default=False, )
    status = models.CharField(max_length=200,blank=True,null=True)

    def get_absolute_url(self):
        return reverse("blog:post_detail", kwargs={"pk": self.pk})

    def __str__(self):
        return self.name

    @property
    def get_order_items(self):
        orderItems = OrderItem.objects.filter(order_id=self.pk)
        return orderItems



    @property
    def total_price(self):
        order_items = OrderItem.objects.filter(order_id=self.id)
        cost = 0
        for order_item in order_items:
            cost += order_item.cost
        return cost


class OrderItem(models.Model):
    seller = models.ForeignKey(user, on_delete=models.DO_NOTHING)
    order = models.ForeignKey(Order,on_delete=models.CASCADE,null=True)
    item = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{(self.order)} - {self.item}'

    @property
    def cost(self):
        return self.item.price * self.quantity
    
    def get_order_items(self):
        orderItems = OrderItem.objects.filter(order_id=self.pk)
        return orderItems


# Create your models here.
