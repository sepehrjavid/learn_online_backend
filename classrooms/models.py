from django.db import models

from accounting.models import CustomUser


class Classroom(models.Model):
    name = models.CharField(max_length=70)
    creator = models.ForeignKey(CustomUser, on_delete=models.PROTECT, related_name="created_classes")
    owners = models.ManyToManyField(CustomUser, related_name="owned_classes")
    enrolled = models.ManyToManyField(CustomUser, related_name="joined_classes")
    is_active = models.BooleanField(default=True)
