from django.db.models.signals import post_save
from django.dispatch import receiver

from missions.models import Assignment


@receiver(post_save, sender=Assignment)
def createAssignmentsFromDefaultAssignments(sender, instance, created, **kwargs):
    if not created:
        if instance.tracker.has_changed('user'):
            Assignment.objects.filter(pk=instance.pk).update(confirmed=False)
            Assignment.objects.filter(pk=instance.pk).update(email_sent=False)

