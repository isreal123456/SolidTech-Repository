from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from .models import Order,OrderItem,Log





@receiver(post_save,sender=Order)
def post_save_create_Order(sender,instance,created,**kwargs):
    if created:
        Log.objects.create(
            log=f'{instance.seller} Created a Pending Order'
        )



@receiver(post_save,sender=OrderItem)
def post_save_create_orderItem(sender,instance,created,**kwargs):
    if created:
        Log.objects.create(
            log=f'{instance.seller} Sold {instance.quantity} {instance.item} to {instance.order}'
        )
        if instance.order.completed == True:
            Log.objects.create(
                log=f'{instance.seller} Completed an Order and made a profit of #{instance.order.total_price}'
            )


