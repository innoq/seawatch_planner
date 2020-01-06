from django.db.models.signals import post_save
from django.dispatch import receiver

from missions.models import Assignment, DefaultAssignment, Mission


@receiver(post_save, sender=Mission)
def createAssignmentsFromDefaultAssignments(sender, instance, created, **kwargs):
    if created:
        default_assignments = DefaultAssignment.objects.filter(ship=instance.ship)
        for default_assignment in default_assignments:
            for i in range(0, default_assignment.quantity):
                Assignment(mission=instance, position=default_assignment.position).save()


@receiver(post_save, sender=Assignment)
def createAssignmentsFromDefaultAssignments(sender, instance, created, **kwargs):
    if not created:
        if instance.tracker.has_changed('user'):
            Assignment.objects.filter(pk=instance.pk).update(confirmed=False)
            Assignment.objects.filter(pk=instance.pk).update(email_sent=False)
