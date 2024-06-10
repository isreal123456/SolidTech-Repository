from django.contrib.auth.signals import user_logged_in,user_logged_out
from django.dispatch import receiver
from Sellers.models import Log


@receiver(user_logged_in)
def post_login(sender,user,request,**Kwargs):
    Log.objects.create(
        log=f'{user.username} logged in'
    )


@receiver(user_logged_out)
def post_login(sender,user,request,**Kwargs):
    Log.objects.create(
        log=f'{user.username} logged out'
    )
