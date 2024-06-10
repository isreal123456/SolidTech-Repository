from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import IncomingProduct, Category, Product
from Sellers.models import Log


@receiver(post_save, sender=IncomingProduct)
def post_save_create_Order(sender, instance, created, **kwargs):
    if created:
        Log.objects.create(
            log=f'{instance.user} Received {instance.quantity} quantity of {instance.product.name}-{instance.product.category}'
        )


@receiver(post_save, sender=Product)
def post_save_create_product(sender, instance, created, **kwargs):
    if created:
        Log.objects.create(
            log=f'{instance.user} created a product {instance.name} under {instance.category}'
        )


@receiver(post_save, sender=Category)
def post_save_create_product(sender, instance, created, **kwargs):
    if created:
        if instance.parent == None:
            Log.objects.create(
                log=f'{instance.user} created a category {instance.name}'
            )
        else:
            Log.objects.create(
                log=f'{instance.user} created a subcategory {instance.name} under {instance.parent}'
            )
