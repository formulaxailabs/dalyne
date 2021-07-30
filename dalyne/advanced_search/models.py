from django.db import models
from core_module.models import User, Tenant
# Create your models here.


class RequestedDownloadModel(models.Model):
    tenant = models.ForeignKey(
        Tenant,
        null=True,
        blank=True,
        related_name="user_downloads",
        on_delete=models.CASCADE
    )
    downloaded_ids = models.JSONField(
        default=list,
        null=True,
        blank=True
    )
    remaining_points = models.IntegerField(
        null=True,
        blank=True
    )
    created_on = models.DateTimeField(
        auto_now_add=True,
        null=True,
        blank=True
    )
    modified_on = models.DateTimeField(
        auto_now=True,
        null=True,
        blank=True
    )