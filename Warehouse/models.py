from django.db import models
from mptt.models import MPTTModel,TreeForeignKey
from django.contrib.auth import get_user_model
user=get_user_model()


# Create your models here.
class Category(MPTTModel):
    user = models.ForeignKey(user,on_delete=models.DO_NOTHING)
    parent = TreeForeignKey('self',related_name='children',on_delete=models.CASCADE,blank=True,null=True,db_constraint=False)
    name = models.CharField(blank=False, help_text="eg RGB",max_length=1000000)

    def __str__(self):
        if self.parent == None:
            return f'{self.name}'
        else:
            return f'{self.name}-{self.parent}'


    def get_products(self):
        descendants = self.get_descendants(include_self=True)
        products = Product.objects.filter(category__in=descendants)
        return products

    class MPTTMeta:
        order_insertion_by = ['name']


class Product(models.Model):
    user = models.ForeignKey(user,on_delete=models.DO_NOTHING)
    name = models.CharField(blank=False, help_text="eg coke",max_length=10000000)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="category",db_constraint=False)
    price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    bad_product_quantity = models.PositiveIntegerField(default=0)
    availability = models.BooleanField(default=False)

    def __str__(self):
        if self.category.parent == None:
            return f'{self.name}-{self.category}'
        else:
            return f'{self.name}-{self.category}'


class IncomingProduct(models.Model):
    user= models.ForeignKey(user, on_delete=models.DO_NOTHING)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,db_constraint=False)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.product.name}-{self.product.category}'


class BadProduct(models.Model):
    user= models.ForeignKey(user, on_delete=models.DO_NOTHING)
    product = models.ForeignKey(Product,on_delete=models.CASCADE,db_constraint=False)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.product.name}-{self.product.category}'

# Create your models here.
