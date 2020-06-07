from django.db import models

from accounting.models import CustomUser


class Classroom(models.Model):
    name = models.CharField(max_length=70, unique=True)
    description = models.TextField(default="No description")
    creator = models.ForeignKey(CustomUser, on_delete=models.PROTECT, related_name="created_classes")
    other_owners = models.ManyToManyField(CustomUser, related_name="owned_classes", blank=True)
    enrolled = models.ManyToManyField(CustomUser, related_name="joined_classes", blank=True)
    is_active = models.BooleanField(default=True)
    is_online = models.BooleanField(default=False)
