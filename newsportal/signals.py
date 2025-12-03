from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

user = get_user_model()

@receiver(post_save, sender=user)
def crate_user_to_common(sender, instance, created, **kwargs):
    if created:
        group = Group.objects.get(name='common')
        instance.groups.add(group)