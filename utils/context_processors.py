from Sellers.models import Log
from Warehouse.models import Category
from mptt.templatetags.mptt_tags import full_tree_for_model

def navbar_categories(request):
    categories = Category.objects.all()
    category = Category.objects.filter(parent=None)
    log = Log.objects.all().order_by('-id')[:5]
    return {'navbar_categories':categories,'category':category,'log':log}