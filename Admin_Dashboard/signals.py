from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from account.models import CustomUser

@receiver(post_save, sender=CustomUser)
def add_moderator_to_group(sender, instance, created, **kwargs):
    if instance.is_moderator:
        group, _ = Group.objects.get_or_create(name='Moderator')
        instance.groups.add(group)
