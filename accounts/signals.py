from .models import *
from django.contrib.auth.models import *
from django.dispatch import receiver
from django.db.models.signals import post_save


@receiver(post_save, sender=User)
def complete_user_creations(instance, created, sender, **kwargs):
    if created:
        group = Group.objects.get(name='customer')
        instance.groups.add(group)

        Customer.objects.create(user=instance, name=instance.username)
        print("Profile Created!")
