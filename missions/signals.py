from django.db.models.signals import post_save
from django.dispatch import receiver

from missions.models import Mission, DefaultAssignment, Assignment


@receiver(post_save, sender=Mission)
def createAssignmentsFromDefaultAssignments(sender, instance, **kwargs):
    if not Assignment.objects.filter(mission=instance).exists():
        default_assignments = DefaultAssignment.objects.filter(ship=instance.ship)
        for default_assignment in default_assignments:
            for i in range(0, default_assignment.quantity):
                Assignment(mission=instance, position=default_assignment.position).save()
