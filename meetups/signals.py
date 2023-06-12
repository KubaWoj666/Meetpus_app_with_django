from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from django.db.models.signals import post_migrate
from django.dispatch import receiver

from .models import Meetup

@receiver(post_migrate)
def create_creator_group(sender, **kwargs):
    if sender.name == 'meetups':  
        meetups_content_type = ContentType.objects.get_for_model(Meetup)

        permissions = [
            ('can_add_meetup', 'Can add meetup', meetups_content_type),
            ('can_update_meetup', 'Can update meetup', meetups_content_type),
            ('can_delete_meetup', 'Can delete meetup', meetups_content_type),
            ('can_add_location', 'Can add location', meetups_content_type),
            ('can_update_location', 'Can update location', meetups_content_type),
            ('can_delete_location', 'Can delete location', meetups_content_type),
            ('can_add_company', 'Can add company', meetups_content_type),
            ('can_update_company', 'Can update company', meetups_content_type),
            ('can_delete_company', 'Can delete company', meetups_content_type),
        ]

        group, created = Group.objects.get_or_create(name='creator')
        if created:
            for codename, name, content_type in permissions:
                permission = Permission.objects.create(
                    codename=codename,
                    name=name,
                    content_type=content_type,
                )
                group.permissions.add(permission)
  
