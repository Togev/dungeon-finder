from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models.signals import post_migrate, m2m_changed
from django.dispatch import receiver
from django.apps import apps
from django.contrib.auth.models import Group, Permission

User = get_user_model()

ADMIN_GROUP_NAMES = {'Full Admin', 'Staff Admin'}

#   Triggers once migrations are made, creates admin groups

@receiver(post_migrate)
def create_admin_groups(sender, **kwargs):
    if sender.name != 'common':
        return

    full_admin, _ = Group.objects.get_or_create(name='Full Admin')
    full_admin.permissions.set(Permission.objects.all())

    staff_admin, _ = Group.objects.get_or_create(name='Staff Admin')

    app_labels = getattr(settings, "PROJECT_APPS", [])
    actions = ['view', 'change']

    codenames = set()
    for label in app_labels:
        try:
            models = apps.get_app_config(label).get_models()
        except LookupError:
            continue
        for model in models:
            for action in actions:
                codenames.add(f"{action}_{model._meta.model_name}")

    perms = Permission.objects.filter(codename__in=codenames)
    staff_admin.permissions.set(perms)


@receiver(m2m_changed, sender=User.groups.through)
def update_is_staff_on_group_change(sender, instance, action, pk_set, **kwargs):
    if action in ['post_add', 'post_remove', 'post_clear']:
        if instance.is_superuser:
            if not instance.is_staff:
                instance.is_staff = True
                instance.save()
            return

        user_group_names = set(instance.groups.values_list('name', flat=True))
        should_be_staff = bool(user_group_names & ADMIN_GROUP_NAMES)
        if instance.is_staff != should_be_staff:
            instance.is_staff = should_be_staff
            instance.save()